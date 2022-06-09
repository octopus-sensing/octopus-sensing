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

import os
import time
import tempfile
import queue
import threading
import multiprocessing

import pytest

import octopus_sensing.devices.audio_streaming as audio_streaming
from octopus_sensing.common.message_creators import start_message, stop_message, terminate_message


class MockedMiniAudioModule:

    def Devices(self):
        return MockedMiniAudioDevices()

    def CaptureDevice(self, buffersize_msec, sample_rate, device_id):
        return MockedMiniAudioCapture()

    def DecodedSoundFile(self, name, nchannels, sample_rate, file_format, samples):
        # Just returning back samples without change!
        return samples

    def wav_write_file(self, file_name, sound_data):
        # Just writing our fake data to the file.
        open(file_name, 'w').write(str(sound_data))


class MockedMiniAudioDevices:

    def get_captures(self):
        # A dict of device_id to a Device Object.
        # From the Device Object, we only use 'id' field.
        return {1: {'id': 'dev-1'}}


class MockedMiniAudioCapture:

    # None of these are important. They will just pass back to our Mock.
    nchannels = 5
    sample_rate = 125
    format = 'wav'

    def start(self, recorder):
        recorder.send(b'123')

    def stop(self):
        pass


@pytest.fixture(scope="module")
def mocked():
    # Replacing base with Thread instead of Process. Because:
    # 1. Process on Windows doesn't use fork (copy-on-write) so we will lose
    #    the mocks we made in here (the parent process).
    # 2. Coverage will lose track in the child process.
    original_bases = audio_streaming.AudioStreaming.__bases__[0].__bases__[0].__bases__
    audio_streaming.AudioStreaming.__bases__[0].__bases__[0].__bases__ = (threading.Thread,)

    # We're replacing the 'miniaudio' imported by our 'audio_streaming' module
    # with our mocked one.
    original_miniaudio = audio_streaming.miniaudio
    audio_streaming.miniaudio = MockedMiniAudioModule()

    yield None

    # Replacing back the original things
    audio_streaming.AudioStreaming.__bases__[0].__bases__[0].__bases__ = original_bases
    audio_streaming.miniaudio = original_miniaudio


def test_happy_path(mocked):

    output_dir = tempfile.mkdtemp(prefix="octopus-sensing-test")
    device_name = 'test-audio-device'
    experiment_id = 'test-exp-1'
    stimuli_id = 'sti-1'

    device = audio_streaming.AudioStreaming(
        1, name=device_name, output_path=output_dir)

    # Since there's no device coordinator running, we set the queue ourselves,
    # and will start the process.
    msg_queue = queue.Queue()
    data_queue_in = queue.Queue()
    data_queue_out = queue.Queue()
    device.set_queue(msg_queue)
    device.set_realtime_data_queues(data_queue_in, data_queue_out)
    device.start()
    # To ensure the process is started.
    time.sleep(0.2)

    msg_queue.put(start_message(experiment_id, stimuli_id))

    time.sleep(1)

    msg_queue.put(stop_message(experiment_id, stimuli_id))

    time.sleep(0.2)

    # It should save the file after receiving a STOP.
    device_output = os.path.join(output_dir, device_name)
    assert os.path.exists(device_output)
    recorded_file = os.path.join(device_output, '{}-{}-{}.wav'.format(
        device_name, experiment_id, stimuli_id))
    assert os.path.exists(recorded_file)

    # Sending terminate and waiting for the device process to exit.
    msg_queue.put(terminate_message())
    device.join()
