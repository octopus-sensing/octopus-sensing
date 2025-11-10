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

import time
import os
import threading
import csv
import random
from typing import List, Optional, Dict, Any

from octopus_sensing.common.message_creators import MessageType
from octopus_sensing.devices.realtime_data_device import RealtimeDataDevice
from octopus_sensing.devices.common import SavingModeEnum

class TestDeviceStreaming(RealtimeDataDevice):
    '''
    Manage TestDevice streaming

    Attributes
    ----------
    sampling_rate
        the sampling rate for recording data

    name
        device name
        This name will be used in the output path to identify each device's data

    output_path
                 The path for recording files.
                 Audio files will be recorded in folder {output_path}/{name}

    saving_mode
        The way of saving data. It saves data continiously in a file
        or saves data which are related to various stimulus in separate files.
        default is SavingModeEnum.CONTINIOUS_SAVING_MODE
        SavingModeEnum is [CONTINIOUS_SAVING_MODE, SEPARATED_SAVING_MODE]

    See Also
    -----------
    :class:`octopus_sensing.device_coordinator`
    :class:`octopus_sensing.devices.device`

    Examples
    ---------
    Here is an example of a test device for creating a random data stream and testing the flow without any devices

    >>> my_test_device =
    ...       TestDeviceStreaming(125,
    ...                           name="test_device",
    ...                           output_path="./output",
    ...                           saving_mode=SavingModeEnum.CONTINIOUS_SAVING_MODE)

    '''
    def __init__(self,
                 sampling_rate: int,
                 saving_mode: int=SavingModeEnum.CONTINIOUS_SAVING_MODE,
                 name: Optional[str] = None,
                 output_path: str = "output"):
        super().__init__(name=name, output_path=output_path)

        self._saving_mode = saving_mode
        self._stream_data: List[float] = []
        self.sampling_rate = sampling_rate
        self._terminate = False
        self._trigger = None
        self._experiment_id = None
        self.__loop_thread: Optional[threading.Thread] = None

        self.output_path = os.path.join(self.output_path, self.name)
        os.makedirs(self.output_path, exist_ok=True)
        self._state = ""

    def __get_sample(self):
        return [random.randint(0, 100), random.randint(0, 50), time.time()]

    def _run(self):
        self.__loop_thread = threading.Thread(target=self._stream_loop)
        self.__loop_thread.start()

        while True:
            message = self.message_queue.get()

            if not self.__loop_thread.is_alive():
                print("TestDevice streaming: The streaming thread is dead. Terminating.")
                break

            if message is None:
                continue

            if message.type == MessageType.START:
                if self._state == "START":
                    print("TestDevice streaming has already recorded the START triger")
                else:
                    print("TestDevice start")
                    self.__set_trigger(message)
                    self._experiment_id = message.experiment_id
                    self._state = "START"
            elif message.type == MessageType.STOP:
                if self._state == "STOP":
                    print("TestDevice streaming has already recorded the STOP triger")
                else:
                    print("TestDevice stop")
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
                        self._experiment_id = message.experiment_id
                        self.__set_trigger(message)
                    self._state = "STOP"
            elif message.type == MessageType.SAVE:
                if self._saving_mode == SavingModeEnum.CONTINIOUS_SAVING_MODE:
                    self._experiment_id = message.experiment_id
                    file_name = \
                        "{0}/{1}-{2}.csv".format(self.output_path,
                                                 self.name,
                                                 self._experiment_id)
                    self._save_to_file(file_name)
                    self._stream_data = []
            elif message.type == MessageType.TERMINATE:
                self._terminate = True
                if self._saving_mode == SavingModeEnum.CONTINIOUS_SAVING_MODE:
                    file_name = \
                        "{0}/{1}-{2}.csv".format(self.output_path,
                                                 self.name,
                                                 self._experiment_id)
                    self._save_to_file(file_name)
                break

        self.__loop_thread.join()

    def _stream_loop(self):
        while True:
            if self._terminate is True:
                break
            data = self.__get_sample()
            if self._trigger is not None:
                data.append(self._trigger)
                self._trigger = None
            self._stream_data.append(data)
            time.sleep(1/self.sampling_rate)


    def __set_trigger(self, message):
        '''
        Takes a message and set the trigger using its data

        Parameters
        ----------
        message: Message
            a message object
        '''
        self._trigger = \
            "{0}-{1}-{2}".format(message.type,
                                 message.experiment_id,
                                 str(message.stimulus_id).zfill(2))

    def _save_to_file(self, file_name):
        print("Saving {0} to file {1}".format(self._name, file_name))
        with open(file_name, 'a') as csv_file:
            writer = csv.writer(csv_file)
            for row in self._stream_data:
                writer.writerow(row)
            csv_file.flush()
        print("Saving {0} to file {1} is done".format(self._name, file_name))

    def get_channels(self):
        '''
        Gets the list of channels

        Returns
        -------

        channels_name: List[str]
            The list of channels' name

        '''
        return ["channel_1", "channel_2", "timestamp"]

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
            `metadata` is a dictionary of device metadata including `sampling_rate` and `channels` and `type`

        '''
        # Last seconds of data

        data = self._stream_data[-1 * duration * self.sampling_rate:]
        metadata = {"sampling_rate": self.sampling_rate,
                    "channels": self.get_channels(),
                    "type": self.__class__.__name__}

        realtime_data = {"data": data,
                  "metadata": metadata}
        return realtime_data
