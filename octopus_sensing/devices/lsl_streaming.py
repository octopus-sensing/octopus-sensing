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
from typing import Optional

from pylsl import StreamInlet, resolve_stream
import csv
import sys
import os

from octopus_sensing.common.message_creators import MessageType
from octopus_sensing.devices.device import Device


class LSLStreaming(Device):
    '''
    Get and Record data from a LSL stream.

    Attributes
    ----------

    Parameters
    ----------
    
    name: str, optional
          device name
          This name will be used in the output path to identify each device's data
    
    output_path: str, optional
                 The path for recording files.
                 Audio files will be recorded in folder {output_path}/{name}

    device_type: str
                 Device type provided by the specific LSL streaming device documentation. To access all available devices, see: https://github.com/sccn/labstreaminglayer/tree/master/Apps

    device: str
            Device name provided by the specific LSL streaming device documentation.


    Example
    -------
    If you want to know get position data from a keyboard streaming, start the .exe available here: https://github.com/labstreaminglayer/App-Input/tree/5eec1b06b9b5db732acdb96f4bd2fc25a1e562fe

    Creating an instance of LSL streaming recorder and adding it to the device coordinator.
    Device coordinator is responsible for triggerng the audio recorder to start or stop recording

    >>> lsl_keyboard = LSLStreaming(1,
    ...                                 name="my_keyboard",
    ...                                 device_type="name",
    ...                                  device="MousePosition")
    >>> device_coordinator.add_device(lsl_keyboard)

    See Also
    -----------
    :class:`octopus_sensing.device_coordinator`
    :class:`octopus_sensing.devices.device`

    '''

    def __init__(self,
                 name: Optional[str] = None,
                 device_type: str = "name",
                 device: str = "Keyboard",                 
                 **kwargs):
        super().__init__(**kwargs)

        self.output_path = os.path.join(self.output_path, self.name)
        os.makedirs(self.output_path, exist_ok=True)
        self._name = name
        self._device_type = device_type
        self._device = device
        self._stream_data = []
        self._terminate = False
        self._state = ""

    def _run(self):
        '''
        Listening to the message queue and manage messages
        '''

        self._stream = resolve_stream(self._device_type, self._device)
        self._inlet = StreamInlet(self._stream[0])

        threading.Thread(target=self._message_loop).start()

        while True:
            # The main thread.
            # Do all the communication with LSL here.

            chunk, timestamp = self._inlet.pull_chunk()
            
            if timestamp:
                data = [timestamp[0]]
                for element in chunk[0]:
                    data.append(element)
                self._stream_data.append(data)
            
            if self._terminate is True:
                break

    def _message_loop(self):
        while True:
            message = self.message_queue.get()
            if message is None:
                continue

            if message.type == MessageType.START:

                
                if self._state == "START":
                    print(f"LSL Device: '{self._device}' has already started")
                else:
                    print(f"LSL device: '{self._device}' start")
                    self._experiment_id = message.experiment_id
                    self.__set_trigger(message)
                    self._state = "START"

            elif message.type == MessageType.STOP:                
                # Probably you want to write the data to the file here.
                if self._state == "STOP":
                    print(f"LSL Device '{self._device}' has already stopped")
                else:
                    
                    self._experiment_id = message.experiment_id
                    self.__set_trigger(message)
                    file_name = \
                        "{0}/{1}-{2}-{3}.csv".format(self.output_path,
                                                    self.name,
                                                    self._experiment_id,
                                                    message.stimulus_id)
                    self._save_to_file(file_name)                        
                    self._state = "STOP"                

            elif message.type == MessageType.TERMINATE:
                self._terminate = True
                break
                
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
