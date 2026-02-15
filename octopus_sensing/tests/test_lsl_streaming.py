import multiprocessing
import pytest
import threading
import queue
import os
import numpy as np
import time
import tempfile
from pylsl import StreamInfo, StreamOutlet
from pylsl.lib import cf_float32

import octopus_sensing.devices.lsl_streaming as lsl_streaming
from octopus_sensing.common.message_creators import start_message, stop_message, terminate_message, save_message
from octopus_sensing.tests.test_helpers import wait_until_file_updated

class RemoteEegLslDevice(threading.Thread):
    def __init__(self, lsl_device_name: str):
        super().__init__(daemon=True)
        stream_type = "EEG"  # or "ECG", "EDA", etc.
        self.channel_count = 8  # Number of channels to simulate (e.g., 8 EEG channels)
        self.sampling_rate = 100  # Sampling rate in Hz
        channel_format = cf_float32  # Data type for the stream
        stream_id = "octopus-test-stream"  # Unique identifier for the stream

        # Create an LSL stream info object
        info = StreamInfo(name=lsl_device_name,
                            type=stream_type,
                            channel_count=self.channel_count,
                            nominal_srate=self.sampling_rate,
                            channel_format=channel_format,
                            source_id=stream_id)

        # Create an LSL outlet
        self.outlet = StreamOutlet(info)

        print(f"LSL: Streaming {stream_type} data with {self.channel_count} channels at {self.sampling_rate} Hz...")
        print("Press Ctrl+C to stop.")
        self.__running_flag = True
    
    def stop_device(self):
        self.__running_flag = False

    def run(self):
        while self.__running_flag is True:
            # Generate a random sample (replace with desired simulation logic)
            sample = np.random.randn(self.channel_count)  # Simulated data for each channel
            self.outlet.push_sample(sample)  # Send the sample over LSL
            time.sleep(1.0 / self.sampling_rate)  # Wait to maintain the sampling rate

        # Ensuring it's properly closed
        del self.outlet

# We use this fixture to make sure we will shutdown the device in case of test failure.
@pytest.fixture(scope="function")
def device():
    output_dir = tempfile.mkdtemp(prefix="octopus-sensing-test")
    # Ensuring unique name when test are run in parallel.
    device_name = f"lsl_test_device-{time.time()}"
    device = lsl_streaming.LslStreaming(device_name, "type", "EEG", 100, output_path=output_dir)

    yield device

    device.terminate()
    device.join()

def test_lsl_streaming(device: lsl_streaming.LslStreaming):
    lsl_device_name = device.name

    remote_lsl_device = RemoteEegLslDevice(lsl_device_name)
    remote_lsl_device.start()
    time.sleep(3)

    experiment_id = 'test-exp-1'
    stimuli_id = 'sti-1'
    lsl_output = device.output_path

    msg_queue: multiprocessing.Queue = multiprocessing.Queue()
    data_queue_in: multiprocessing.Queue = multiprocessing.Queue()
    data_queue_out: multiprocessing.Queue = multiprocessing.Queue()
    device.set_queue(msg_queue)
    device.set_realtime_data_queues(data_queue_in, data_queue_out)

    device.start()

    time.sleep(0.4)

    msg_queue.put(start_message(experiment_id, stimuli_id))
    # Allowing data collection for one second
    time.sleep(1)

    msg_queue.put(stop_message(experiment_id, stimuli_id))

    time.sleep(0.4)

    msg_queue.put(save_message(experiment_id))

    # Sending terminate and waiting for the device process to exit.
    msg_queue.put(terminate_message())
    device.join()

    remote_lsl_device.stop_device()
    remote_lsl_device.join()

    # It should save the file after receiving a TERMINATE.
    filename = f"{lsl_device_name}-{experiment_id}.csv"

    assert os.path.exists(lsl_output)
    assert len(os.listdir(lsl_output)) == 1
    assert os.listdir(lsl_output)[0] == filename

    filecontent = open(os.path.join(lsl_output, filename), 'r').read()
    print(f"filecontent: {filecontent}, length={len(filecontent)}")
    assert len(filecontent) >= 375
    # TODO: Check if the triggers are there.
    # TODO: We can check data in realtime data queues as well.

def test_save_message(device: lsl_streaming.LslStreaming):
    lsl_device_name = device.name

    remote_lsl_device = RemoteEegLslDevice(lsl_device_name)
    remote_lsl_device.start()
    time.sleep(3)

    lsl_output = device.output_path
    experiment_id = 'test-exp-1'
    stimuli_id = 'sti-1'

    msg_queue: multiprocessing.Queue = multiprocessing.Queue()
    data_queue_in: multiprocessing.Queue = multiprocessing.Queue()
    data_queue_out: multiprocessing.Queue = multiprocessing.Queue()
    device.set_queue(msg_queue)
    device.set_realtime_data_queues(data_queue_in, data_queue_out)

    device.start()

    time.sleep(0.5)

    msg_queue.put(save_message(experiment_id))

    filename = f"{lsl_device_name}-{experiment_id}.csv"
    output_file_path = os.path.join(lsl_output, filename)

    wait_until_file_updated(output_file_path, 0, timeout=5)

    # It should save the file after receiving a SAVE.
    assert os.path.exists(lsl_output)
    assert len(os.listdir(lsl_output)) == 1
    assert os.listdir(lsl_output)[0] == filename

    # TODO: Check the content of the file
    first_size_bytes = os.path.getsize(output_file_path)
    assert first_size_bytes >= 100

    time.sleep(0.5)

    # Sending start and stop messages to collect data.
    msg_queue.put(start_message(experiment_id, stimuli_id))
    # Allowing data collection for one second
    time.sleep(1)

    msg_queue.put(stop_message(experiment_id, stimuli_id))

    msg_queue.put(save_message(experiment_id))

    # Waiting until the file is updated
    # NOTE: wait_until_file_updated uses os.path.getsize() (bytes). Using len(filecontent)
    # can be smaller due to universal newline translation (e.g. '\r\n' -> '\n'), causing
    # false positives and flaky tests.
    wait_until_file_updated(output_file_path, first_size_bytes, timeout=5)

    # TODO: Check the content of the file
    file_size = os.path.getsize(output_file_path)
    assert file_size > first_size_bytes
    assert file_size >= 200

    # Sending terminate and waiting for the device process to exit.
    msg_queue.put(terminate_message())
    device.join()

    remote_lsl_device.stop_device()
    remote_lsl_device.join()

# TODO: Test non-continuous mode
# TODO: Test real time data queues
