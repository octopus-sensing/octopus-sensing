# This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
# Copyright © Nastaran Saffaryazdi 2020-2026
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

import multiprocessing
import os
import time
import tempfile
import pytest

import octopus_sensing.devices.camera_streaming as camera_streaming
from octopus_sensing.common.message_creators import start_message, stop_message, terminate_message
from octopus_sensing.tests.test_helpers import wait_until_path_exists

class MockedCv2Module:

    def VideoCapture(self, camera_number):
        return MockedVideoCaptureModule(camera_number)
    
    def VideoWriter_fourcc(self, a, b, c, d):
        # The code cv2 returns for XVID
        return 1145656920
    
    def VideoWriter(self, file_name, codec, fps, _video_size):
        return MockedVideoWriterModule(file_name)

    def CAP_PROP_FRAME_WIDTH(self):
        return (float(640.0))
    
    def CAP_PROP_FRAME_HEIGHT(self):
        return (float(480.0))
    
    def imwrite(self, filename, img):
        a = time.time()
        open(filename[:-4] + "/" + str(a) + ".jpg", 'w+').write(img)

class MockedVideoCaptureModule:

    def __init__(self, camera_number):
        pass

    def isOpened(self):
        return True

    def set(self, a, b):
        pass

    def read(self):
        # A short delay to make it more realistic
        time.sleep(0.05)
        # bool, 3d matrix (fake signal)
        return True, [[[0,10,10],[1,11,11]], [[0,10,10],[1,11,11]]]
    
    def write(self, frame):
        pass

    def release(self):
        pass

    def get(self, option):
        return (float(640.0))


class MockedVideoWriterModule:

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, frame):
        a = time.time()
        open(self.file_name, 'a').write(str(frame))

    def release(self):
        pass

@pytest.fixture(scope="module")
def mocked():
    original_cv2 = camera_streaming.cv2
    camera_streaming.cv2 = MockedCv2Module()

    yield None

    # Replacing back the original things
    camera_streaming.cv2 = original_cv2


def test_happy_path(mocked):

    output_dir = tempfile.mkdtemp(prefix="octopus-sensing-test")
    device_name = 'test-video-device'
    experiment_id = 'test-exp-1'
    stimuli_id = 'sti-1'

    device = camera_streaming.CameraStreaming(
        camera_no=0, output_path=output_dir, name=device_name)

    msg_queue = multiprocessing.Queue()
    data_queue_in = multiprocessing.Queue()
    data_queue_out = multiprocessing.Queue()
    device.set_queue(msg_queue)
    device.set_realtime_data_queues(data_queue_in, data_queue_out)
    device.start()

    time.sleep(0.2)

    msg_queue.put(start_message(experiment_id, stimuli_id))

    time.sleep(1)

    # Sending None message to the queue and making sure it does not cause any problem.
    msg_queue.put(None)
    time.sleep(0.05)

    msg_queue.put(stop_message(experiment_id, stimuli_id))

    time.sleep(0.2)

    # Second stop message should be ignored.
    msg_queue.put(stop_message(experiment_id, 'ignore-this'))

    # It should save the file after receiving a STOP.
    device_output = os.path.join(output_dir, device_name)
    recorded_file = os.path.join(device_output, '{}-{}-{}.avi'.format(
        device_name, experiment_id, stimuli_id))
    
    wait_until_path_exists([device_output, recorded_file], timeout=5)

    assert os.path.exists(device_output)
    assert os.path.exists(recorded_file)
    assert os.path.getsize(recorded_file) > 1000 # check the file size to assure it is not empty

    # Sending terminate and waiting for the device process to exit.
    msg_queue.put(terminate_message())
    device.join()
