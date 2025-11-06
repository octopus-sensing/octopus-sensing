import queue
import os
import time
import tempfile
import threading

from octopus_sensing.devices.testdevice_streaming import TestDeviceStreaming
from octopus_sensing.common.message_creators import start_message, stop_message, terminate_message


def test_system_health():
    print("test device")
    output_dir = tempfile.mkdtemp(prefix="octopus-sensing-test")
    experiment_id = 'test-exp-2'
    stimuli_id = 'sti-2'

    device = \
        TestDeviceStreaming(12,
                            name="test_device",
                            output_path=output_dir)
    msg_queue = queue.Queue()
    device.set_queue(msg_queue)
    realtime_data_queue_in = queue.Queue()
    realtime_data_queue_out = queue.Queue()
    device.set_realtime_data_queues(realtime_data_queue_in, realtime_data_queue_out)

    device_thread = threading.Thread(target=device._run)
    device_thread.start()
    print("after start")

    time.sleep(0.2)

    msg_queue.put(start_message(experiment_id, stimuli_id))
    # Allowing data collection for one second
    time.sleep(1)

    msg_queue.put(stop_message(experiment_id, stimuli_id))

    time.sleep(0.2)

    # Sending terminate and waiting for the device process to exit.
    msg_queue.put(terminate_message())
    device_thread.join()

    # It should save the file after receiving a TERMINATE.
    test_device_output = os.path.join(output_dir, "test_device")
    filename = "test_device-{}.csv".format(experiment_id)

    assert os.path.exists(test_device_output)
    assert len(os.listdir(test_device_output)) == 1
    assert os.listdir(test_device_output)[0] == filename

    filecontent = open(os.path.join(test_device_output, filename), 'r').read()
    assert len(filecontent) >= 375
    # TODO: Check if the triggers are there.
    # TODO: We can check data in realtime data queues as well.
