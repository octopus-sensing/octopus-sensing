# This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
# Copyright © Zahra Saffaryazdi 2020
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
import os.path
import multiprocessing
import multiprocessing.dummy
import multiprocessing.queues
import queue
import random
import time
import tempfile

import pytest
import pyOpenBCI


class MockSample:
    def __init__(self, channels):
        self.channels_data = [round(random.uniform(
            0.01, 0.9)) for _ in range(channels)]
        self.aux_data = [round(random.uniform(0.01, 0.9))
                         for _ in range(channels)]
        self.id = random.randrange(1, 200)


class MockedOpenBCICyton:
    def __init__(self, daisy):
        self._channels = 16
        if daisy is False:
            self._channels = 8

    def stop_stream(self):
        pass

    def start_stream(self, callback):
        for _ in range(128):
            callback(MockSample(self._channels))
            # Sample rate: 128 per second
            time.sleep(1 / 128)


@pytest.fixture(scope="module")
def mocked():
    # Preventing processes from creating a new process
    original_process = multiprocessing.Process
    multiprocessing.Process = multiprocessing.dummy.Process
    original_queue = multiprocessing.queues.Queue
    multiprocessing.queues.Queue = queue.Queue
    original_queue_method = multiprocessing.Queue
    multiprocessing.Queue = queue.Queue

    original_openbcicyton = pyOpenBCI.OpenBCICyton
    pyOpenBCI.OpenBCICyton = MockedOpenBCICyton

    yield None

    multiprocessing.Process = original_process
    multiprocessing.queues.Queue = original_queue
    multiprocessing.Queue = original_queue_method
    pyOpenBCI.OpenBCICyton = original_openbcicyton


def test_system_health(mocked):
    '''Runs the whole system to roughly check everything is working together.'''
    # To ensure mocks are applied, we import these modules here.
    import octopus_sensing.devices.openbci.openbci_streaming as openbci_streaming
    from octopus_sensing.device_coordinator import DeviceCoordinator
    from octopus_sensing.common.message_creators import ControlMessage

    output_dir = tempfile.mkdtemp(prefix="octopus-sensing-test")

    openbci = openbci_streaming.OpenBCIStreaming(
        name="eeg", output_path=output_dir)
    coordinator = DeviceCoordinator()
    coordinator.add_device(openbci)

    try:
        control_message = ControlMessage("int_test", "stimulus_1")
        coordinator.dispatch(control_message.start_message())
        time.sleep(1)
        coordinator.dispatch(control_message.stop_message())

        records = coordinator.get_monitoring_data(3)
        assert "eeg" in records
        assert len(records["eeg"]) == 3
        assert len(records["eeg"][0]) >= 8

    finally:
        coordinator.dispatch(control_message.terminate_message())

    # To ensure termination is happened.
    time.sleep(0.5)

    eeg_output = os.path.join(output_dir, "eeg")
    assert os.path.exists(eeg_output)
    assert len(os.listdir(eeg_output)) == 1, \
        "More than one file created by eeg"
