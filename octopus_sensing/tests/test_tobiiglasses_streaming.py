import pytest
import multiprocessing
import multiprocessing.queues
import threading
import queue
import http.client
import pickle
import os
import json
import numpy as np
import time
import tempfile

import octopus_sensing.devices.tobiiglasses_streaming as tobiiglasses_streaming
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.common.message_creators import start_message, stop_message, terminate_message
from octopus_sensing.realtime_data_endpoint import RealtimeDataEndpoint



class MockTobiiGlassesController():
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self._is_connected = True
        self._is_streaming = False
    def get_battery_status(self):
        return {"battery_level": 100, "charging": False}
    
    def get_data(self):
        return {"mems":{'ac': {'ts': 3872249638, 's': 0, 'ac': [0.863, -9.257, 4.382]}, 'gy': {'ts': 3872260722, 's': 0, 'gy': [11.13, 89.306, 22.002]}},
                "left_eye": {'pc': {'ts': 3872276156, 's': 0, 'gidx': 15585, 'pc': [25.67, -19.62, -31.37], 'eye': 'left'}, 'pd': {'ts': 3872276156, 's': 0, 'gidx': 15585, 'pd': 3.04, 'eye': 'left'}, 'gd': {'ts': 3872276156, 's': 0, 'gidx': 15585, 'gd': [0.0338, 0.0821, 0.996], 'eye': 'left'}}, 
                "right_eye": {'pc': {'ts': 3872296141, 's': 0, 'gidx': 15586, 'pc': [-39.17, -19.39, -33.74], 'eye': 'right'}, 'pd': {'ts': 3872296141, 's': 0, 'gidx': 15586, 'pd': 2.84, 'eye': 'right'}, 'gd': {'ts': 3872276156, 's': 0, 'gidx': 15585, 'gd': [0.0754, 0.12, 0.9899], 'eye': 'right'}}, 
                "gp": {'ts': 3872276156, 's': 0, 'gidx': 15585, 'l': 59995, 'gp': [0.4823, 0.4335]}, 
                "gp3": {'ts': 3872276156, 's': 0, 'gidx': 15585, 'gp3': [38.88, 64.52, 792.89]}}
    def start_streaming(self):
        self._is_streaming = True
    def stop_streaming(self):
        self._is_streaming = False
    def close(self):
        self._is_connected = False


@pytest.fixture(scope="module")
def mocked():
    original_bases = tobiiglasses_streaming.TobiiGlassesStreaming.__bases__[0].__bases__[0].__bases__
    tobiiglasses_streaming.TobiiGlassesStreaming.__bases__[0].__bases__[0].__bases__ = (threading.Thread,)
    original_TobiiGlassesController = tobiiglasses_streaming.TobiiGlassesController
    tobiiglasses_streaming.TobiiGlassesController = MockTobiiGlassesController

    yield None

    tobiiglasses_streaming.TobiiGlassesStreaming.__bases__[0].__bases__[0].__bases__ = original_bases
    tobiiglasses_streaming.TobiiGlassesController = original_TobiiGlassesController

def test_system_health(mocked):

    output_dir = tempfile.mkdtemp(prefix="octopus-sensing-test")
    experiment_id = 'test-exp-2'
    stimuli_id = 'sti-2'

    device = \
        tobiiglasses_streaming.TobiiGlassesStreaming("192.168.71.50",
                                                     50,
                                                     output_path=output_dir,
                                                     name="tobii")
    msg_queue = queue.Queue()
    device.set_queue(msg_queue)
    realtime_data_queue_in = queue.Queue()
    realtime_data_queue_out = queue.Queue()
    device.set_realtime_data_queues(realtime_data_queue_in, realtime_data_queue_out)

    device.start()

    time.sleep(0.2)

    msg_queue.put(start_message(experiment_id, stimuli_id))
    # Allowing data collection for one second
    time.sleep(1)

    msg_queue.put(stop_message(experiment_id, stimuli_id))

    time.sleep(0.2)

    # Sending terminate and waiting for the device process to exit.
    msg_queue.put(terminate_message())
    device.join()

    # It should save the file after receiving a TERMINATE.
    tobii_output = os.path.join(output_dir, "tobii")
    filename = "tobii-{}.csv".format(experiment_id)

    assert os.path.exists(tobii_output)
    assert len(os.listdir(tobii_output)) == 1
    assert os.listdir(tobii_output)[0] == filename

    filecontent = open(os.path.join(tobii_output, filename), 'r').read()
    assert len(filecontent) >= 100
    # TODO: Check if the triggers are there.
    # TODO: We can check data in realtime data queues as well.
