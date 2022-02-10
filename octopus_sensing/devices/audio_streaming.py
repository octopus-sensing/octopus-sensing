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
import array
from typing import List
import miniaudio

from octopus_sensing.devices.device import Device
from octopus_sensing.common.message_creators import MessageType

class AudioStreaming(Device):
    '''
    Stream and Record audio

    Attributes
    ----------

    Parameters
    ----------

    device_id: int
        The audio recorder ID. If there is several audio recorder in the system
    
    name: str, optional
          device name
          This name will be used in the output path to identify each device's data
    
    output_path: str, optional
                 The path for recording files.
                 Audio files will be recorded in folder {output_path}/{name}


    Example
    -------
    If you want to know what is your audio recorder's ID run the following example  from `miniaudio <https://github.com/irmen/pyminiaudio>`_

    >>> import miniaudio
    >>> devices = miniaudio.Devices()
    >>> captures = devices.get_captures()
    >>> for d in enumerate(captures):
            print("{num} = {name}".format(num=d[0], name=d[1]['name']))

    Example
    -----------
    Creating an instance of audio recorder and adding it to the device coordinator.
    Device coordinator is responsible for triggerng the audio recorder to start or stop recording

    >>> audio_recorder = AudioStreaming(1,
    ...                                 name="Audio_monitoring",
    ...                                 output_path="./output")
    >>> device_coordinator.add_device(audio_recorder)

    See Also
    -----------
    :class:`octopus_sensing.device_coordinator`
    :class:`octopus_sensing.devices.device`

    '''
    def __init__(self, device_id:int, **kwargs):
        super().__init__(**kwargs)
        self.output_path = os.path.join(self.output_path, self.name)
        os.makedirs(self.output_path, exist_ok=True)

        self._device_id = device_id
        
        self._stream_data: List[bytes] = []
        self._record = False
        self._terminate = False
        self._state = ""

    def __stream_loop(self):
        _ = yield
        while True:
            data = yield
            self._stream_data.append(data)

    def _run(self):
        devices = miniaudio.Devices()
        captures = devices.get_captures()
        selected_device = captures[self._device_id]
        capture = \
            miniaudio.CaptureDevice(buffersize_msec=1000,
                                    sample_rate=44100,
                                    device_id=selected_device["id"])

        recorder = self.__stream_loop()
        next(recorder)

        while True:
            message = self.message_queue.get()
            if message is None:
                continue
            if message.type == MessageType.START:
                if self._state == "START":
                    print("Audio streaming has already started")
                else:
                    self._stream_data = []
                    capture.start(recorder)
                    self._record = True
                    self._state = "START"
            elif message.type == MessageType.STOP:
                if self._state == "STOP":
                   print("Audio streaming has already stopped")
                else:
                    capture.stop()
                    self._record = False
                    file_name = \
                        "{0}/{1}-{2}-{3}.wav".format(self.output_path,
                                                    self.name,
                                                    message.experiment_id,
                                                    str(message.stimulus_id).zfill(2))
                    self._save_to_file(file_name, capture)
                    self._state = "STOP"
            elif message.type == MessageType.TERMINATE:
                self._terminate = True
                break

    def _save_to_file(self, file_name:str, capture:miniaudio.CaptureDevice):
        buffer = b"".join(self._stream_data)
        samples = array.array('h')
        samples.frombytes(buffer)
        sound = miniaudio.DecodedSoundFile('capture',
                                           capture.nchannels,
                                           capture.sample_rate,
                                           capture.format,
                                           samples)
        miniaudio.wav_write_file(file_name, sound)
