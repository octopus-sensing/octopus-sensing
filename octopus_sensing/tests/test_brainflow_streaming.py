import pytest
import multiprocessing
import multiprocessing.dummy
import multiprocessing.queues
import queue
import random
import http.client
import pickle
import os
import json
import numpy as np
import time
import tempfile
from brainflow import board_shim

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

    def get_board_data(self):
        return (np.array([ [1,1],[1,1],[1,1] ]))


@pytest.fixture(scope="module")
def mocked():
    # Preventing processes from creating a new process
    original_process = multiprocessing.Process
    multiprocessing.Process = multiprocessing.dummy.Process
    original_queue = multiprocessing.queues.Queue
    multiprocessing.queues.Queue = queue.Queue
    original_queue_method = multiprocessing.Queue
    multiprocessing.Queue = queue.Queue

    original_BrainFlowInputParams = board_shim.BrainFlowInputParams
    board_shim.BrainFlowInputParams = MockBrainFlowInputParams
    original_BoardShim = board_shim.BoardShim
    board_shim.BoardShim = MockBoardShim

    yield None

    multiprocessing.Process = original_process
    multiprocessing.queues.Queue = original_queue
    multiprocessing.Queue = original_queue_method
    board_shim.BrainFlowInputParams = original_BrainFlowInputParams
    board_shim.BoardShim = original_BoardShim

def test_system_health(mocked):
    import octopus_sensing.devices.brainflow_streaming as brainflow_streaming
    from octopus_sensing.device_coordinator import DeviceCoordinator
    from octopus_sensing.common.message_creators import start_message, stop_message, terminate_message
    from octopus_sensing.monitoring_endpoint import MonitoringEndpoint

    output_dir = tempfile.mkdtemp(prefix="octopus-sensing-test")
    print(output_dir)
    coordinator = DeviceCoordinator()

    params = board_shim.BrainFlowInputParams()
    params.serial_port = "/dev/ttyUSB0"
    brainflow = brainflow_streaming.BrainFlowStreaming(2, 125, brain_flow_input_params=params, name="cyton_daisy", output_path="./output")    

    coordinator.add_device(brainflow)

    monitoring_endpoint = MonitoringEndpoint(coordinator)
    monitoring_endpoint.start()

    try:
        coordinator.dispatch(start_message("int_test", "stimulus_1"))
        # Allowing data collection for five seconds
        time.sleep(5)
        coordinator.dispatch(stop_message("int_test", "stimulus_1"))

        http_client = http.client.HTTPConnection("127.0.0.1:9330")
        http_client.request("GET", "/")
        response = http_client.getresponse()
        assert response.status == 200
        monitoring_data = pickle.loads(response.read())
        assert isinstance(monitoring_data, dict)
        assert isinstance(monitoring_data["cyton_daisy"], list)
        assert len(monitoring_data["cyton_daisy"]) == 375
        assert len(monitoring_data["cyton_daisy"][0]) == 5
        assert len(monitoring_data["cyton_daisy"][-1]) == 5

    finally:
        coordinator.dispatch(terminate_message())
        monitoring_endpoint.stop()

    # To ensure termination is happened.
    time.sleep(0.5)

    brain_output = os.path.join(output_dir, "cyton_daisy")
    assert os.path.exists(brain_output)
    assert len(os.listdir(brain_output)) == 1
    assert os.listdir(brain_output)[0] == "cyton_daisy-int_test.csv"