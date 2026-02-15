import multiprocessing
import queue
import os
import time
import tempfile
from brainflow import BoardIds, BrainFlowInputParams

import octopus_sensing.devices.brainflow_streaming as brainflow_streaming
from octopus_sensing.common.message_creators import start_message, stop_message, terminate_message


def test_system_health():

    output_dir = tempfile.mkdtemp(prefix="octopus-sensing-test")
    experiment_id = 'test-exp-2'
    stimuli_id = 'sti-2'

    params = BrainFlowInputParams()
    params.serial_port = "/dev/ttyUSB0"
    device = \
        brainflow_streaming.BrainFlowStreaming(BoardIds.SYNTHETIC_BOARD,
                                               125,
                                               brain_flow_input_params=params,
                                               name="cyton_daisy",
                                               output_path=output_dir)
    msg_queue = multiprocessing.Queue()
    device.set_queue(msg_queue)
    realtime_data_queue_in = multiprocessing.Queue()
    realtime_data_queue_out = multiprocessing.Queue()
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
    # TODO: Use BoardIds.PLAYBACK_FILE_BOARD and check the data is exactly the same as the input file.
