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
from brainflow import board_shim

import octopus_sensing.devices.brainflow_streaming as brainflow_streaming
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.common.message_creators import start_message, stop_message, terminate_message
from octopus_sensing.realtime_data_endpoint import RealtimeDataEndpoint


class MockBrainFlowInputParams():
    def __init__(self):
        pass

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class MockBoardShim():
    def __init__(self, board_id, input_params):
        try:
            self.input_json = input_params.to_json().encode()
        except BaseException:
            self.input_json = input_params.to_json()
        self.board_id = board_id
        self._master_board_id = self.board_id

    def set_log_level(self, a):
        pass
    def prepare_session(self):
        pass
    def start_stream(self):
        pass
    def stop_stream(self):
        pass
    def release_session(self):
        pass

    def get_board_data(self):
        return (np.array([ [1,1],[1,1],[1,1] ]))


@pytest.fixture(scope="module")
def mocked():
    original_bases = brainflow_streaming.BrainFlowStreaming.__bases__[0].__bases__[0].__bases__
    brainflow_streaming.BrainFlowStreaming.__bases__[0].__bases__[0].__bases__ = (threading.Thread,)
    original_BrainFlowInputParams = brainflow_streaming.BrainFlowInputParams
    brainflow_streaming.BrainFlowInputParams = MockBrainFlowInputParams
    original_BoardShim = brainflow_streaming.BoardShim
    brainflow_streaming.BoardShim = MockBoardShim

    yield None

    brainflow_streaming.BrainFlowStreaming.__bases__[0].__bases__[0].__bases__ = original_bases
    brainflow_streaming.BrainFlowInputParams = original_BrainFlowInputParams
    brainflow_streaming.BoardShim = original_BoardShim

def test_system_health(mocked):

    output_dir = tempfile.mkdtemp(prefix="octopus-sensing-test")
    experiment_id = 'test-exp-2'
    stimuli_id = 'sti-2'

    params = board_shim.BrainFlowInputParams()
    params.serial_port = "/dev/ttyUSB0"
    device = \
        brainflow_streaming.BrainFlowStreaming(2,
                                               125,
                                               brain_flow_input_params=params,
                                               name="cyton_daisy",
                                               output_path=output_dir)
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
    brain_output = os.path.join(output_dir, "cyton_daisy")
    filename = "cyton_daisy-{}.csv".format(experiment_id)

    assert os.path.exists(brain_output)
    assert len(os.listdir(brain_output)) == 1
    assert os.listdir(brain_output)[0] == filename

    filecontent = open(os.path.join(brain_output, filename), 'r').read()
    assert len(filecontent) >= 375
    # TODO: Check if the triggers are there.
    # TODO: We can check data in realtime data queues as well.
