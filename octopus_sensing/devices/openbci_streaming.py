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
import threading
import csv
import datetime
import pyOpenBCI
import numpy as np

from octopus_sensing.common.message_creators import MessageType
from octopus_sensing.devices.realtime_data_device import RealtimeDataDevice
from octopus_sensing.devices.common import SavingModeEnum


uVolts_per_count = (4500000)/24/(2**23-1)
accel_G_per_count = 0.002 / (2**4)  # G/count


class OpenBCIStreaming(RealtimeDataDevice):
    '''
    Manages OpenBCI streaming
    It uses pyOpenBCI library which is not supporting by OpenBCI anymore.
    We recommend to use 
    :class:`octopus_sensing.devices.brainflow_openbci_streaming` instead.

    Data will be recorded in a csv file/files with the following column order:
    channels, Acc_x, Acc_y, Acc_z, sample_id, time_stamp, trigger

    Attributes
    -----------

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
    
    daisy: bool, default: True
           If it is True, it means we use cyton-daisy board,
           otherwise we use cyton board

    channels_order: list of str, default: None
        A list of channel names which specify the order and names of channels

    Example
    --------
    Creating an instance of OpenBCI board with USB dongle using 
    `pyOpenBCI <https://github.com/andreaortuno/pyOpenBCI>`_,
    and adding it to the device coordinator. Device coordinator is responsible
    for triggerng the OpenBCI to start or stop recording  or to add markers to
    recorded data.
    In this example, since the saving mode is continuous, all recorded data 
    will be saved in a file. But, when an event happens, device coordinator will send
    a trigger message to the device and recorded data will be marked with the trigger

    >>> my_openbci = 
    ...     OpenBCIStreaming(name="OpenBCI",
    ...                      output_path="./output",
    ...                      daisy=True,
    ...                      saving_mode=SavingModeEnum.CONTINIOUS_SAVING_MODE,
    ...                      channels_order=["Fp1", "Fp2", "F7", "F3", 
    ...                                      "F4", "F8", "T3", "C3",
    ...                                      "C4", "T4", "T5", "P3", 
    ...                                      "P4", "T6", "O1", "O2"])
    >>> device_coordinator.add_device(my_openbci)

    Note
    -----
    Before running the code, turn on the OpenBCI, connect the dongle and make sure its port is free.


    See Also
    --------
    :class:`octopus_sensing.device_coordinator`
    :class:`octopus_sensing.devices.device`,
    :class:`octopus_sensing.devices.brainflow_openbci_streaming`

    '''
    def __init__(self,
                 daisy=True,
                 channels_order=None,
                 saving_mode=SavingModeEnum.CONTINIOUS_SAVING_MODE,
                 **kwargs):
        super().__init__(**kwargs)

        self._saving_mode = saving_mode
        self._stream_data = []
        self._board = self._inintialize_board(daisy)
        self._trigger = None
        self._experiment_id = None
        self._sampling_rate = 128

        self.output_path = self._make_output_path()

        if channels_order is None:
            if daisy is True:
                self.channels = \
                    ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8", "ch9",
                     "ch10", "ch11", "ch12", "ch13", "ch14", "ch15", "ch16"]
            else:
                self.channels = \
                    ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8"]
        else:
            self.channels = channels_order
            if daisy is True:
                if len(self.channels) != 16:
                    raise "The number of channels in channels_order should be 16"
            elif daisy is False:
                if len(self.channels) != 8:
                    raise "The number of channels in channels_order should be 8"

    def _make_output_path(self):
        output_path = os.path.join(self.output_path, "eeg")
        os.makedirs(output_path, exist_ok=True)
        return output_path

    def _inintialize_board(self, daisy):
        return pyOpenBCI.OpenBCICyton(daisy=daisy)

    def _run(self):
        threading.Thread(target=self._stream_loop).start()

        while True:
            message = self.message_queue.get()
            if message is None:
                continue
            if message.type == MessageType.START:
                self.__set_trigger(message)
                self._experiment_id = message.experiment_id
            elif message.type == MessageType.STOP:
                if self._saving_mode == SavingModeEnum.SEPARATED_SAVING_MODE:
                    self._experiment_id = message.experiment_id
                    file_name = \
                        "{0}/{1}-{2}-{3}.csv".format(self.output_path,
                                                     self.name,
                                                     self._experiment_id,
                                                     message.stimulus_id)
                    self._save_to_file(file_name)
                else:
                    self._experiment_id = message.experiment_id
                    self.__set_trigger(message)
            elif message.type == MessageType.TERMINATE:
                if self._saving_mode == SavingModeEnum.CONTINIOUS_SAVING_MODE:
                    file_name = \
                        "{0}/{1}-{2}.csv".format(self.output_path,
                                                 self.name,
                                                 self._experiment_id)
                    self._save_to_file(file_name)
                break

        self._board.stop_stream()

    def __set_trigger(self, message):
        '''
        Takes a message and set the trigger using its data

        @param Message message: a message object
        '''
        self._trigger = \
            "{0}-{1}-{2}".format(message.type,
                                 message.experiment_id,
                                 str(message.stimulus_id).zfill(2))

    def _stream_loop(self):
        self._board.start_stream(self._stream_callback)

    def _stream_callback(self, sample):
        data = np.array(sample.channels_data) * uVolts_per_count
        acc_data = np.array(sample.aux_data) * accel_G_per_count
        data_list = list(data) + list(acc_data)
        data_list.append(sample.id)
        data_list.append(str(datetime.datetime.now().time()))
        if self._trigger is not None:
            data_list.append(self._trigger)
            self._trigger = None
        self._stream_data.append(data_list)

    def _save_to_file(self, file_name):
        if not os.path.exists(file_name):
            csv_file = open(file_name, 'a')
            header = []
            header.extend(self.channels)
            header.extend(["acc-x", "acc-y", "acc-z"])
            header.extend(["sample_id", "time stamp", "trigger"])
            writer = csv.writer(csv_file)
            writer.writerow(header)
            csv_file.flush()
            csv_file.close()
        with open(file_name, 'a') as csv_file:
            writer = csv.writer(csv_file)
            for row in self._stream_data:
                writer.writerow(row)
                csv_file.flush()

    def _get_realtime_data(self, duration: int):
        '''
        Returns n seconds (duration) of latest collected data for monitoring/visualizing or 
        realtime processing purposes.

        Parameters
        ----------
        duration: int
            A time duration in seconds for getting the latest recorded data in realtime

        Returns
        -------
        data: List[Any]
            List of records, or empty list if there's nothing.
        '''

        data = self._stream_data[-1 * duration * self._sampling_rate:]
        metadata = {"sampling_rate": self._sampling_rate,
                    "channels": self.channels,
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

    def get_channels(self):
        '''
        Gets the list of channels

        Returns
        -------

        channels_name: List[str]
            The list of channels' name

        '''
        return self.channels
