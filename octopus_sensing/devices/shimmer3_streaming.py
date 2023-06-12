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
import time
import datetime
import csv
import math
import struct
import serial
from typing import List, Optional, Any, Dict

from octopus_sensing.devices.realtime_data_device import RealtimeDataDevice
from octopus_sensing.common.message_creators import MessageType
from octopus_sensing.common.message import Message
from octopus_sensing.devices.common import SavingModeEnum

# In seconds
SERIAL_PORT_TIMEOUT = 0.6

class Shimmer3Streaming(RealtimeDataDevice):
    '''
    Streams and Records Shimmer3 data.
    Data will be recorded in a csv file/files with the following column order:
    type, time stamp, Acc_x, Acc_y, Acc_z, GSR_ohm, PPG_mv, time, trigger

    Attributes
    ----------

    Parameters
    ----------
    name: str, default: None
        Device name. This name will be used in the output path to identify
        each device's data.

    output_path: str,  default: output
        The path for recording files.
        Audio files will be recorded in folder {output_path}/{name}

    saving_mode: int, default: SavingModeEnum.CONTINIOUS_SAVING_MODE
        The way of saving data: saving continiously in a file or save data related to
        each stimulus in a separate file.
        SavingModeEnum is:

            0. CONTINIOUS_SAVING_MODE
            1. SEPARATED_SAVING_MODE

    serial_port: str, default: Windows=Com12, Linux=/dev/rfcomm0
        The serial port that Shimmer is paired with (See the Note below)

    sampling_rate: int, default: 128
        The sampling frequency for acquiring data from the device


    See Also
    -----------
    :class:`octopus_sensing.device_coordinator`
    :class:`octopus_sensing.devices.device`

    Example
    -------
    Creating an instance of shimmer3 and adding it to the device coordinator.
    Device coordinator is responsible for triggerng the shimmer3 to
    start or stop recording  or to add markers to recorded data.
    In this example, since the saving mode is continuous, all recorded data
    will be saved in a file. But, when an event happens, device coordinator will send a trigger message
    to the device and recorded data will be marked with the trigger

    >>> my_shimmer = Shimmer3Streaming(name="shimmer",
    ...                                saving_mode=SavingModeEnum.CONTINIOUS_SAVING_MODE,
    ...                                output_path="./output")
    >>> device_coordinator.add_device(my_shimmer)


    Note
    -----
    Keep in your mind, before running the code for Shimmer data recording,
    turn on the Shimmer3 sensor and pair bluetooth and the serial port. (Shimmer password: 1234)

    For example in linux you can do it as follow:
        1- hcitool scan   //It shows the macaddress of device. for shimmer it is 00:06:66:F0:95:95

        2- vim /etc/bluetooth/rfcomm.conf write the below line in it:
        rfcomm0{ bind no; device 00:06:66:F0:95:95; channel 1; comment "serial port" }

        3- sudo rfcomm connect rfcomm0 00:06:66:F0:95:95 // This is for reading bluetooth data from a serial port

    Note
    -----
    This class is based on `ShimmerReader <https://github.com/nastaran62/ShimmerReader>`_
    which is an extended version of
    `LogAndStream python firmware <http://www.shimmersensing.com/images/uploads/docs/LogAndStream_for_Shimmer3_Firmware_User_Manual_rev0.11a.pdf>`_
    for Shimmer3 data streaming.
    '''

    def __init__(self,
                 sampling_rate: int = 128,
                 saving_mode: int = SavingModeEnum.CONTINIOUS_SAVING_MODE,
                 serial_port: Optional[str] = None,
                 **kwargs):
        super().__init__(**kwargs)

        self._saving_mode = saving_mode
        self._stream_data: List[float] = []
        self._sampling_rate = sampling_rate
        self._trigger: Optional[str] = None
        self._break_loop = False
        self._loop_thread: Optional[threading.Thread] = None
        self.output_path = self._make_output_path()
        self._state = ""
        if serial_port is None:
            if platform.system() == "Windows":
                self._serial_port = "Com12"
            else:
                self._serial_port = "/dev/rfcomm0"
        else:
            self._serial_port = serial_port

    def _make_output_path(self):
        output_path = os.path.join(self.output_path, self.name)
        os.makedirs(output_path, exist_ok=True)
        return output_path

    def _inintialize_connection(self):
        '''
        Initializing connection with Simmer3 device
        '''
        self._serial = serial.Serial(port=self._serial_port, baudrate=115200, timeout=SERIAL_PORT_TIMEOUT, write_timeout=SERIAL_PORT_TIMEOUT)
        if not self._serial.is_open:
            raise RuntimeError(
                "shimmer3: Couldn't open the port for some reason.")

        self._serial.flushInput()
        print("port opening, done.")
        # send the set sensors command
        # 4 bytes command:
        #     0x08 is SET_SENSORS_COMMAND
        #     Each bit in the three following bytes are one sensor.
        self._serial.write(struct.pack(
            'BBBB', 0x08, 0x84, 0x01, 0x00))  # GSR and PPG
        self._wait_for_ack()
        print("sensor setting, done.")

        # Enable the internal expansion board power
        self._serial.write(struct.pack('BB', 0x5E, 0x01))
        self._wait_for_ack()
        print("enable internal expansion board power, done.")

        # send the set sampling rate command

        '''
        sampling_freq = 32768 / clock_wait = X Hz
        2 << 14 = 32768
        '''
        clock_wait = math.ceil((2 << 14) / self._sampling_rate)

        self._serial.write(struct.pack('<BH', 0x05, clock_wait))
        self._wait_for_ack()

        # Inquiry configurations (For finding channels order)
        # Page 16 of This PDF:
        # http://www.shimmersensing.com/images/uploads/docs/LogAndStream_for_Shimmer3_Firmware_User_Manual_rev0.11a.pdf

        self._serial.write(struct.pack('B', 0x01))
        self._wait_for_ack()
        inquiery_response = bytes("", 'utf-8')
        # response_size is 1 packet_type + 2 Sampling rate + 4 Config Bytes +
        # 1 Num Channels + 1 Buffer size
        response_size = 9
        numbytes = 0
        while numbytes < response_size:
            inquiery_response += self._serial.read(response_size)
            numbytes = len(inquiery_response)

        num_channels = inquiery_response[7]
        print("Number of Channels:", num_channels)
        print("Buffer size:", inquiery_response[8])

        # There's one byte for each channel
        # For the meaning of each byte, refer to the above PDF
        channels = bytes("", "utf-8")
        numbytes = 0
        while numbytes < num_channels:
            channels += self._serial.read(num_channels)
            numbytes = len(channels)

        print("Channel 1:", channels[0])
        print("Channel 2:", channels[1])
        print("Channel 3:", channels[2])
        print("Channel 4:", channels[3])
        print("Channel 5:", channels[4])

        # send start streaming command
        self._serial.write(struct.pack('B', 0x07))
        self._wait_for_ack()
        print("start command sending, done.")
        self._experiment_id = 0

    def _wait_for_ack(self):
        start_time = time.time()
        ddata = ""
        ack = struct.pack('B', 0xff)
        while ddata != ack:
            if time.time() - start_time >= 1:
                raise RuntimeError(f"[{self.name}] Did not receive 'ack' from Shimmer3 after one second")
            ddata = self._serial.read(1)

    def _run(self):
        '''
        Listening to the message queue and manage messages
        '''
        self._inintialize_connection()

        self._loop_thread = threading.Thread(target=self._stream_loop)
        self._loop_thread.start()

        while True:
            message = self.message_queue.get()

            if not self._loop_thread.is_alive():
                print(f"[{self.name}] Shimmer3: Streaming loop is dead. Terminating.")
                break

            if message is None:
                continue

            if message.type == MessageType.START:
                if self._state == "START":
                    print("Shimmer3 streaming has already recorded the START triger")
                else:
                    print("Shimmer start")
                    self._experiment_id = message.experiment_id
                    self.__set_trigger(message)
                    self._state = "START"
            elif message.type == MessageType.STOP:
                if self._state == "STOP":
                    print("Shimmer3 streaming has already recorded the STOP triger")
                else:
                    if self._saving_mode == SavingModeEnum.SEPARATED_SAVING_MODE:
                        self._experiment_id = message.experiment_id
                        file_name = \
                            "{0}/{1}-{2}-{3}.csv".format(self.output_path,
                                                         self.name,
                                                         self._experiment_id,
                                                         message.stimulus_id)
                        self._save_to_file(file_name)
                        self._stream_data = []
                    else:
                        print("Shimmer stop")
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
        self._loop_thread.join()

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
        ddata = bytes("", 'utf-8')
        numbytes = 0
        # 1byte packet type + 3byte timestamp + 2 byte X + 2 byte Y +
        # 2 byte Z + 2 byte PPG + 2 byte GSR
        framesize = 14

        try:
            while True:
                while numbytes < framesize:
                    ddata += self._serial.read(framesize)
                    numbytes = len(ddata)
                    if self._break_loop:
                        break

                if self._break_loop:
                    self._stop_shimmer()
                    break

                data = ddata[0:framesize]
                ddata = ddata[framesize:]
                numbytes = len(ddata)

                # read basic packet information
                (packettype) = struct.unpack('B', data[0:1])
                (timestamp0, timestamp1, timestamp2) = \
                    struct.unpack('BBB', data[1:4])

                # read packet payload
                (x, y, z, PPG_raw, GSR_raw) = \
                    struct.unpack('HHHHH', data[4:framesize])
                record_time = datetime.datetime.now()

                # get current GSR range resistor value
                data_range = ((GSR_raw >> 14) & 0xff)  # upper two bits
                if data_range == 0:
                    rf = 40.2   # kohm
                elif data_range == 1:
                    rf = 287.0  # kohm
                elif data_range == 2:
                    rf = 1000.0  # kohm
                elif data_range == 3:
                    rf = 3300.0  # kohm

                # convert GSR to kohm value
                gsr_to_volts = (GSR_raw & 0x3fff) * (3.0/4095.0)
                GSR_ohm = rf/((gsr_to_volts / 0.5) - 1.0)

                # convert PPG to milliVolt value
                PPG_mv = PPG_raw * (3000.0/4095.0)

                timestamp = timestamp0 + timestamp1*256 + timestamp2*65536

                # print([packettype[0], timestamp, GSR_ohm, PPG_mv] + self._trigger)

                if self._trigger is not None:
                    print("Shimmer trigger")
                    row = [packettype[0],
                           timestamp,
                           x, y, z,
                           GSR_ohm,
                           PPG_mv,
                           record_time,
                           self._trigger]
                    self._trigger = None
                else:
                    row = [packettype[0],
                           timestamp,
                           x, y, z,
                           GSR_ohm,
                           PPG_mv,
                           record_time]
                self._stream_data.append(row)

        except KeyboardInterrupt:
            self._stop_shimmer()

    def _stop_shimmer(self):
        # send stop streaming command
        self._serial.write(struct.pack('B', 0x20))

        print("stop command sent, waiting for ACK_COMMAND")
        self._wait_for_ack()
        print("ACK_COMMAND received.")
        self._serial.close()
        print("All done")

    def _save_to_file(self, file_name):
        if not os.path.exists(file_name):
            csv_file = open(file_name, 'a')
            header = ["type", "time stamp", "Acc_x", "Acc_y", "Acc_z",
                      "GSR_ohm",
                      "PPG_mv",
                      "time",
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

    def _get_realtime_data(self, duration: int) -> Dict[str, Any]:
        '''
        Returns n seconds (duration) of latest collected data for monitoring/visualizing or
        realtime processing purposes.

        Parameters
        ----------
        duration: int
            A time duration in seconds for getting the latest recorded data in realtime

        Returns
        -------
        data: Dict[str, Any]
            The keys are `data` and `metadata`.
            `data` is a list of records, or empty list if there's nothing.
            `metadata` is a dictionary of device metadata including `sampling_rate` and `type`
        '''
        # Last recorded data
        data = self._stream_data[-1 * duration * self._sampling_rate:]
        metadata = {"sampling_rate": self._sampling_rate,
                    "channels": ["type", "time stamp", "Acc_x", "Acc_y", "Acc_z",
                                 "GSR_ohm", "PPG_mv", "time", "trigger"],
                    "type": self.__class__.__name__}
        realtime_data = {"data": data,
                         "metadata": metadata}
        return realtime_data

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
