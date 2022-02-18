import os
import time
import tempfile
import queue
import threading
import pytest

import octopus_sensing.devices.camera_streaming as camera_streaming
from octopus_sensing.common.message_creators import start_message, stop_message, terminate_message

class MockedCv2Module:

    def VideoCapture(self, camera_number):
        return MockedVideoCaptureModule(camera_number)
    
    def VideoWriter_fourcc(self, a, b, c, d):
        return ('XVID')
    
    def VideoWriter(self, file_name, codec, fps, _video_size):
        return MockedVideoWriterModule(file_name)

    '''
    Get the information of your computer using:
    >>> import cv2
    >>> cap=cv2.VideoCapture(0)
    >>> print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    >>> print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    '''
    def CAP_PROP_FRAME_WIDTH(self):
        return (float(640.0))
    
    def CAP_PROP_FRAME_HEIGHT(self):
        return (float(480.0))
    
    def imwrite(self, filename, img):
        a = time.time()
        # self.output_path/self.name-experiment_id-str(message.stimulus_id).zfill(2)/str(a).jpg
        open(filename[:-4] + "/" + str(a) + ".jpg", 'w+').write(img)

class MockedVideoCaptureModule:

    def isOpened(self):
        return True

    def set(self):
        pass

    def read(self):
        # bool, 3d matrix
        return True, [[[0,10,10],[1,11,11]], [[0,10,10],[1,11,11]]]
    
    def release(self):
        pass

    def get(self):
        return (float(640.0))


class MockedVideoWriterModule:

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, frame):
        a = time.time()
        print('111111!',self.file_name)
        open(self.file_name, 'w+').write(frame)

    def release(self):
        pass

@pytest.fixture(scope="module")
def mocked():
    original_bases = camera_streaming.CameraStreaming.__bases__[0].__bases__
    camera_streaming.CameraStreaming.__bases__[0].__bases__ = (threading.Thread,)

    original_cv2 = camera_streaming.cv2
    camera_streaming.cv2 = MockedCv2Module()

    yield None

    # Replacing back the original things
    camera_streaming.CameraStreaming.__bases__[0].__bases__ = original_bases
    camera_streaming.cv2 = original_cv2


def test_happy_path(mocked):

    output_dir = tempfile.mkdtemp(prefix="octopus-sensing-test")
    device_name = 'test-video-device'
    experiment_id = 'test-exp-1'
    stimuli_id = 'sti-1'

    device = camera_streaming.CameraStreaming(
        camera_no=0, output_path=output_dir, name=device_name)

    msg_queue = queue.Queue()
    device.set_queue(msg_queue)
    device.start()

    time.sleep(0.2)

    msg_queue.put(start_message(experiment_id, stimuli_id))

    time.sleep(1)

    msg_queue.put(stop_message(experiment_id, stimuli_id))

    time.sleep(0.2)

    # It should save the file after receiving a STOP.
    device_output = os.path.join(output_dir, device_name)
    assert os.path.exists(device_output)

    recorded_file = os.path.join(device_output, '{}-{}-{}.avi'.format(
        device_name, experiment_id, stimuli_id))

    
    ''' 
    for bug testing only
    list_dir = os.listdir(device_output)
    print ('output_dir:',output_dir)
    print('device_name:',device_name)
    print ('device_output:', device_output)
    print("list_dir:",list_dir)
    for temp in list_dir:
        print("temp:",temp)
    '''

    assert os.path.exists(recorded_file)

    # Sending terminate and waiting for the device process to exit.
    msg_queue.put(terminate_message())
    device.join()