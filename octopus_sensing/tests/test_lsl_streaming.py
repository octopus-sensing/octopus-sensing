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
from pylsl import StreamInfo, StreamOutlet

import octopus_sensing.devices.lsl_streaming as lsl_streaming
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.common.message_creators import start_message, stop_message, terminate_message
from octopus_sensing.realtime_data_endpoint import RealtimeDataEndpoint


class RemoteEegLslDevice(threading.Thread):
    def __init__(self):
        super().__init__()
        stream_name = "FakeDeviceStream"
        stream_type = "EEG"  # or "ECG", "EDA", etc.
        self.channel_count = 8  # Number of channels to simulate (e.g., 8 EEG channels)
        self.sampling_rate = 100  # Sampling rate in Hz
        channel_format = "float32"  # Data type for the stream
        stream_id = "12345"  # Unique identifier for the stream

        # Create an LSL stream info object
        info = StreamInfo(name=stream_name,
                            type=stream_type,
                            channel_count=self.channel_count,
                            nominal_srate=self.sampling_rate,
                            channel_format=channel_format,
                            source_id=stream_id,)

        # Create an LSL outlet
        self.outlet = StreamOutlet(info)

        print(f"Streaming {stream_type} data with {self.channel_count} channels at {self.sampling_rate} Hz...")
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


@pytest.fixture(scope="module")
def mocked():
    original_bases = lsl_streaming.LslStreaming.__bases__[0].__bases__[0].__bases__
    lsl_streaming.LslStreaming.__bases__[0].__bases__[0].__bases__ = (threading.Thread,)
    yield None

    # Replacing back the original things
    lsl_streaming.LslStreaming.__bases__[0].__bases__[0].__bases__ = original_bases


def test_system_health(mocked):
    remote_lsl_device = RemoteEegLslDevice()
    remote_lsl_device.start()
    time.sleep(3)

    output_dir = tempfile.mkdtemp(prefix="octopus-sensing-test")
    experiment_id = 'test-exp-1'
    stimuli_id = 'sti-1'

    lsl_device_name = "FakeLslDevice"
    device = lsl_streaming.LslStreaming(lsl_device_name, "type", "EEG", 100, output_path=output_dir)

    msg_queue = queue.Queue()
    data_queue_in = queue.Queue()
    data_queue_out = queue.Queue()
    device.set_queue(msg_queue)
    device.set_realtime_data_queues(data_queue_in, data_queue_out)

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

    remote_lsl_device.stop_device()
    remote_lsl_device.join()

    # It should save the file after receiving a TERMINATE.
    lsl_output = os.path.join(output_dir, lsl_device_name)
    filename = f"{lsl_device_name}-{experiment_id}.csv"

    assert os.path.exists(lsl_output)
    assert len(os.listdir(lsl_output)) == 1
    assert os.listdir(lsl_output)[0] == filename

    filecontent = open(os.path.join(lsl_output, filename), 'r').read()
    print(f"filecontent: {filecontent}, length={len(filecontent)}")
    assert len(filecontent) >= 375
    # TODO: Check if the triggers are there.
    # TODO: We can check data in realtime data queues as well.
