# This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
# Copyright © Nastaran Saffaryazdi 2020
#
# Octopus Sensing is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
#  either version 3 of the License, or (at your option) any later version.
#
# Octopus Sensing is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Octopus Sensing.
# If not, see <https://www.gnu.org/licenses/>.

import os
import platform
import threading
import datetime
import csv
import math
import struct
import serial
from typing import List, Optional
import time
import socket

from octopus_sensing.devices.monitored_device import MonitoredDevice
from octopus_sensing.common.message_creators import MessageType
from octopus_sensing.common.message import Message
from octopus_sensing.devices.common import SavingModeEnum

HOST = '127.0.0.1'
PORT = 50007

class SkinosStreaming(MonitoredDevice):

    def __init__(self,
                 sampling_rate: int=128,
                 saving_mode: int=SavingModeEnum.CONTINIOUS_SAVING_MODE,
                 **kwargs):
        super().__init__(**kwargs)

        self._saving_mode = saving_mode
        self._stream_data: List[float] = []
        self._sampling_rate = sampling_rate
        self._inintialize_connection()
        self._trigger: Optional[str] = None
        self._break_loop = False
        self.output_path = self._make_output_path()
        self._state = ""
        self._client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _make_output_path(self):
        output_path = os.path.join(self.output_path, self.name)
        os.makedirs(output_path, exist_ok=True)
        return output_path

    def _inintialize_connection(self):
        '''
        Initializing connection with Simmer3 device
        '''
        os_type = platform.system()
        if os_type == "Windows":
            self._serial = serial.Serial("Com12", 115200)
        else:
            self._serial = serial.Serial("/dev/ttyUSB0", 19200, timeout=0.1)
        self._serial.flushInput()
        print("port opening, done.")

    def _wait_for_ack(self):
        ddata = ""
        ack = struct.pack('B', 0xff)
        while ddata != ack:
            ddata = self._serial.read(1)

    def _run(self):
        '''
        Listening to the message queue and manage messages
        '''
        loop_thread = threading.Thread(target=self._stream_loop)
        loop_thread.start()

        while True:
            message = self.message_queue.get()
            if message is None:
                continue
            if message.type == MessageType.START:
                if self._state == "START":
                    print("Skinos streaming has already recorded the START triger")
                else:
                    print("Skinos start")
                    self._experiment_id = message.experiment_id
                    self.__set_trigger(message)
                    self._state = "START"
            elif message.type == MessageType.STOP:
                if self._state == "STOP":
                    print("Skinos streaming has already recorded the STOP triger")
                else:
                    if self._saving_mode == SavingModeEnum.SEPARATED_SAVING_MODE:
                        self._experiment_id = message.experiment_id
                        file_name = \
                            "{0}/{1}-{2}-{3}.csv".format(self.output_path,
                                                        self.name,
                                                        self._experiment_id,
                                                        message.stimulus_id)
                        self._save_to_file(file_name)
                    else:
                        print("Skinos stop")
                        self._experiment_id = message.experiment_id
                        self.__set_trigger(message)
                    self._state = "STOP"
            elif message.type == MessageType.TERMINATE:
                if self._saving_mode == SavingModeEnum.CONTINIOUS_SAVING_MODE:
                    file_name = \
                        "{0}/{1}-{2}.csv".format(self.output_path,
                                                 self.name,
                                                 self._experiment_id)
                    self._save_to_file(file_name)
                break

        self._break_loop = True
        loop_thread.join()

    def __set_trigger(self, message: Message):
        '''
        Takes a message and set the trigger using its data

        Parameters
        -----------
        message: Message
                 a message object
        '''
        self._trigger = \
            "{0}-{1}-{2}".format(message.type,
                                 message.experiment_id,
                                 str(message.stimulus_id).zfill(2))

    def _stream_loop(self):
        '''
        Reads incoming data
        '''
        initial_flag = False
        framesize = 15

        try:
            while True:
                time.sleep(0.1)

                result = self._serial.read_until(b':', 16)

                if self._break_loop:
                    self._stop_skinos()
                    break
                
                ch1 = result[0:3]
                ch2 = result[4:7]
                ch3 = result[8:11]
                ch4 = result[12:15]

                (timestamp) = datetime.datetime.now()

                if initial_flag is False:
                    ch1_str = '000000'
                    ch2_str = '000000'
                    ch3_str = '000000'
                    ch4_str = '000000'

                    initial_flag = True

                else:
                    ch1_str = repr(ch1)
                    ch2_str = repr(ch2)
                    ch3_str = repr(ch3)
                    ch4_str = repr(ch4)

                ch_int_list = []
                
                ch_int_list.append(int(ch1_str[2:5], 16))
                ch_int_list.append(int(ch2_str[2:5], 16))
                ch_int_list.append(int(ch3_str[2:5], 16))
                ch_int_list.append(int(ch4_str[2:5], 16))

                for i in range(len(ch_int_list)):
                    if ch_int_list[i] < 2048:
                        ch_int_list[i] = ch_int_list[i] / 500
                    
                    else:
                        ch_int_list[i] = - ((4096 - ch_int_list[i]) / 500)

                print(ch_int_list)

                self._client.sendto(result,(HOST, PORT))

                #print(timestamp, ch1, ch2, ch3, ch4, self._trigger)

                if self._trigger is not None:
                    print("Skinos trigger")
                    row = [timestamp,
                           ch_int_list[0], 
                           ch_int_list[1],
                           ch_int_list[2],
                           ch_int_list[3],
                           self._trigger]
                    self._trigger = None
                else:
                    row = [timestamp,
                           ch_int_list[0],
                           ch_int_list[1],
                           ch_int_list[2],
                           ch_int_list[3],
                           self._trigger]
                self._stream_data.append(row)

        except KeyboardInterrupt:
            self._stop_skinos()

    def _stop_skinos(self):

        print("All done")

    def _save_to_file(self, file_name):
        if not os.path.exists(file_name):
            csv_file = open(file_name, 'a')
            header = ["time stamp", "ch1", "ch2", "ch3", "ch4", "label"
                      "trigger"]
            writer = csv.writer(csv_file)
            writer.writerow(header)
            csv_file.flush()
            csv_file.close()

        with open(file_name, 'a') as csv_file:
            writer = csv.writer(csv_file)
            for row in self._stream_data:
                writer.writerow(row)
                csv_file.flush()

    def _get_monitoring_data(self):
        '''Returns latest collected data for monitoring/visualizing purposes.'''
        # Last three seconds
        return self._stream_data[-1 * 3 * self._sampling_rate:]

    def get_saving_mode(self):
        '''
        Gets saving mode
        
        Returns
        -----------
        saving_mode: int
            The way of saving data: saving continiously in a file or save data related to
            each stimulus in a separate file. 
            SavingModeEnum is CONTINIOUS_SAVING_MODE = 0 or SEPARATED_SAVING_MODE = 1
        '''
        return self._saving_mode

    def get_output_path(self):
        '''
        Gets the path that is used for data recording

        Returns
        -----------
        output_path: str
           The output path that use for data recording
        '''
        return self.output_path
