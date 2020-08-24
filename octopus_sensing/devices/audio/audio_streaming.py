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
# You should have received a copy of the GNU General Public License along with Foobar.
# If not, see <https://www.gnu.org/licenses/>.

import threading
import os
import wave
import pyaudio

from octopus_sensing.devices.device import Device
from octopus_sensing.common.message_creators import MessageType

SAMPLING_RATE = 44100  # Sample rate
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RECORD_SECONDS = 5


class AudioStreaming(Device):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._stream_data = []
        self._record = False
        self.output_path = os.path.join(self.output_path, "audio")
        os.makedirs(self.output_path, exist_ok=True)
        self.__audio_recorder = pyaudio.PyAudio()

        self.__stream = \
            self.__audio_recorder.open(format=FORMAT,
                                       channels=CHANNELS,
                                       rate=SAMPLING_RATE,
                                       input=True,
                                       frames_per_buffer=CHUNK)

    def _run(self):
        threading.Thread(target=self._stream_loop).start()
        while True:
            message = self.message_queue.get()
            if message is None:
                continue
            if message.type == MessageType.START:
                self._stream_data = []
                self._record = True
            elif message.type == MessageType.STOP:
                self._record = False
                file_name = \
                    "{0}/{1}-{2}-{3}.wav".format(self.output_path,
                                                 self.device_name,
                                                 message.experiment_id,
                                                 message.stimulus_id)
                self._save_to_file(file_name)
            elif message.type == MessageType.TERMINATE:
                break

        self.__stream.stop_stream()
        self.__stream.close()
        self.__audio_recorder.terminate()

    def _stream_loop(self):
        while True:
            if self._record is True:
                data = self.__stream.read(CHUNK)
                self._stream_data.append(data)

    def _save_to_file(self, file_name):

        wave_file = wave.open(file_name, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(self.__audio_recorder.get_sample_size(FORMAT))
        wave_file.setframerate(SAMPLING_RATE)
        wave_file.writeframes(b''.join(self._stream_data))
        wave_file.close()
