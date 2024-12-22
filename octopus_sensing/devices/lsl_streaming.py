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

import threading
import csv
import sys
import os
from typing import List, Optional, Any, Dict
from pylsl import StreamInlet, resolve_byprop

from octopus_sensing.common.message_creators import MessageType
from octopus_sensing.devices.realtime_data_device import RealtimeDataDevice
from octopus_sensing.devices.common import SavingModeEnum


class LslStreaming(RealtimeDataDevice):
    '''
    Get and Record data from a LSL stream.

    Attributes
    ----------

    Parameters
    ----------
    
    name: str
          device name
          This name will be used in the output path to identify each device's data

    stream_property_type: str
            It uses the property info to resolve a device from network. This the info provided by the LSL streamer
            you want to read. For example, stream_property_type='name' and stream_property_value='EEG' will try to
            find any device that it's name is 'EEG' and is streaming in the current network.

    stream_property_value: str
            See stream_property_type
    
    output_path: str, optional
            The path for recording files.
            Recorded file/files will be in folder {output_path}/{name}

    Example
    -------
    If you want to know get position data from a keyboard streaming, start the .exe available here: https://github.com/labstreaminglayer/App-Input/tree/5eec1b06b9b5db732acdb96f4bd2fc25a1e562fe

    Creating an instance of LSL streaming recorder and adding it to the device coordinator.
    Device coordinator is responsible for triggerng the audio recorder to start or stop recording

    >>> lsl_device = LslStreaming("mbtrain",
    ...                             "name",
    ...                             "EEG",
                                    250,
    ...                             output_path="output")
    >>> device_coordinator.add_device(lsl_device)

    See Also
    -----------
    :class:`octopus_sensing.device_coordinator`
    :class:`octopus_sensing.devices.device`

    '''

    def __init__(self,
                 name: str,
                 stream_property_type: str,
                 stream_property_value: str,
                 sampling_rate: int,
                 output_path: str = "output",
                 saving_mode: int=SavingModeEnum.CONTINIOUS_SAVING_MODE,
                 channels: Optional[list] = None,
                 **kwargs):
        super().__init__(**kwargs)

        self._name = name
        self._stream_property_type = stream_property_type
        self._stream_property_value = stream_property_value
        self._stream_data: List[float] = []
        self._loop_thread: Optional[threading.Thread] = None
        self._terminate = False
        self._state = ""
        self._experiment_id = None
        self._stream = None
        self._inlet = None
        self.sampling_rate = sampling_rate
        self.channels = channels
        self._trigger = None
        self._saving_mode = saving_mode

        self.output_path = os.path.join(output_path, self._name)
        os.makedirs(self.output_path, exist_ok=True)

    def _run(self):
        '''
        Listening to the message queue and manage messages
        '''
        self._loop_thread = threading.Thread(target=self._stream_loop)
        self._loop_thread.start()

        while True:
            message = self.message_queue.get()
            if message is None:
                continue

            if message.type == MessageType.START:
                if self._state == "START":
                    print(f"LSL Device: '{self.name}' has already started.")
                else:
                    print(f"LSL Device: '{self.name}' started.")
                    self._experiment_id = message.experiment_id
                    self.__set_trigger(message)
                    self._state = "START"

            elif message.type == MessageType.STOP:
                if self._state == "STOP":
                    print(f"LSL Device '{self.name}' has already stopped.")
                else:
                    print(f"LSL Device '{self.name}' stopped.")
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

            elif message.type == MessageType.TERMINATE:
                self._terminate = True
                if self._saving_mode == SavingModeEnum.CONTINIOUS_SAVING_MODE:
                    file_name = \
                        "{0}/{1}-{2}.csv".format(self.output_path,
                                                 self.name,
                                                 self._experiment_id)
                    self._save_to_file(file_name)
                break

        self._loop_thread.join()

    def _stream_loop(self):
        # self._stream = resolve_stream(self._device_type, self.device)
        self._stream = resolve_byprop(self._stream_property_type, self._stream_property_value, timeout=5)
        if self._stream is None or len(self._stream) == 0:
            raise RuntimeError(f"Couldn't resolve an LSL stream with {self._stream_property_type}={self._stream_property_value}")
        self._inlet = StreamInlet(self._stream[0])

        while True:
            if self._terminate is True:
                break
            sample, timestamp = self._inlet.pull_sample(timeout=0.2)
            if sample is not None:
                sample.append(timestamp)
                if self._trigger is not None:
                    sample.append(self._trigger)
                    self._trigger = None
                self._stream_data.append(sample)

    def __set_trigger(self, message):
        '''
        Takes a message and set the trigger using its data

        Parameters
        ----------
        message: Message
            a message object
        '''
        # Add the trigger to the data
        self._trigger = \
            "{0}-{1}-{2}".format(message.type,
                                 message.experiment_id,
                                 str(message.stimulus_id).zfill(2))

    def _save_to_file(self, file_name):
        if not os.path.exists(file_name):
            csv_file = open(file_name, 'a')
            writer = csv.writer(csv_file)
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
                `metadata` is a dictionary of device metadata including `sampling_rate` and `channels` and `type`

            '''
            # Last seconds of data

            data = self._stream_data[-1 * duration * self.sampling_rate:]
            metadata = {"sampling_rate": self.sampling_rate,
                        "channels": self.channels,
                        "type": self.__class__.__name__}

            realtime_data = {"data": data,
                    "metadata": metadata}
            return realtime_data
