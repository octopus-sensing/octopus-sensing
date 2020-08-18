# This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
# Copyright © Zahra Saffaryazdi 2020
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

import sounddevice as sd
from scipy.io.wavfile import write
from threading import Thread

SAMPLING_RATE = 44100  # Sample rate

# The sounddevice library is not working with multiprocessing
class AudioStreaming(Thread):
    def __init__(self, file_name, recording_time):
        super().__init__()
        self._file_path =  "created_files/audio/" + file_name + '.wav'
        self._recording_time = recording_time
        sd._initialize()

    def run(self):
        print("start audio recording")
        myrecording = \
            sd.rec(int(self._recording_time * SAMPLING_RATE),
                   samplerate=SAMPLING_RATE,
                   channels=2)
        sd.wait()  # Wait until recording is finished
        print("stop audio recording")
        write(self._file_path, SAMPLING_RATE, myrecording)
