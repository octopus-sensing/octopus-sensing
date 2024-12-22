# This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
# Copyright © Nastaran Saffaryazdi 2020
#
# Octopus Sensing is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
#  either version 3 of the License, or (at your option) any later version.
#
# Octopus Sensing is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Octopus Sensing.
# If not, see <https://www.gnu.org/licenses/>.

import sys
import time
import traceback
import multiprocessing
import queue
import pickle
from typing import List, Any, Tuple, Dict, Optional

from octopus_sensing.devices.device import Device
from octopus_sensing.devices.realtime_data_device import RealtimeDataDevice
from octopus_sensing.common.message import Message
from octopus_sensing.common.message_creators import terminate_message

QueueType = multiprocessing.queues.Queue


class RealtimeDataCache:
    def __init__(self) -> None:
        self._time = time.time_ns()
        self._cached_data: Dict[str, List[Any]] = {}

    def get_cache(self):
        '''Returns None if cache is not available or expired'''
        # 100 ms
        if time.time_ns() - self._time > 100000000:
            return None
        return self._cached_data

    def cache(self, data: Dict[str, List[Any]]):
        self._cached_data = data
        self._time = time.time_ns()


class DeviceCoordinator:
    '''
    Device coordinator is responsible for coordination, like start recording data
    from all devices at once, stop recording, triggering (marking data at point),
    and terminating devices.
    When a device is added to the device coordinator, it will be initialized and prepared for data recording.
    '''

    def __init__(self) -> None:
        self.__devices: Dict[str, Device] = {}
        self.__queues: List[QueueType] = []
        self.__device_counter: int = 0
        self.__realtime_data_queues: List[Tuple[QueueType, QueueType, Device]] = [
        ]
        self.__realtime_data_cache = RealtimeDataCache()

    def __get_device_id(self) -> str:
        '''
        Generate an ID for devices that do not have name

        Returns
        -----------
        str
            an ID for device
        '''

        self.__device_counter += 1
        device_id = "device_{0}".format(self.__device_counter)
        return device_id

    def get_devices(self) -> List[Device]:
        '''
        Return a list of added devices

        Returns
        -----------
        List[Device]
            List of device objects
        '''

        return list(self.__devices.values())

    def add_device(self, device: Device) -> None:
        '''
        Adds new device to the coordinator and starts it

        Parameters
        ----------
        device: Device
            a device object

        Example
        --------
        >>> my_shimmer = Shimmer3Streaming(name="Shimmer3_sensor", output_path="./output")
        >>> device_coordinator.add_device(my_shimmer)

        See Also
        ---------
        add_devices: Adds a list of new devices to the coordinator and starts them
        '''
        assert isinstance(device, Device)

        if device.name is None:
            device.name = self.__get_device_id()
        if device.name in self.__devices.keys():
            raise RuntimeError("This device already has been added")

        self.__devices[device.name] = device
        msg_queue: QueueType = multiprocessing.Queue()
        device.set_queue(msg_queue)
        self.__queues.append(msg_queue)

        self.__set_realtime_data_queues(device)

        device.start()

    def add_devices(self, devices: List[Device]) -> None:
        '''
        Adds a list of new devices to the coordinator and starts them

        Parameters
        ----------
        devices: List[Device]
            a list of device objects

        Example
        --------
        >>> my_shimmer = Shimmer3Streaming(name="Shimmer3_sensor",
                                           output_path="./output")
        >>> device_coordinator.add_devices([my_shimmer])

        See Also
        ---------
        add_device: Adds new device to the coordinator and starts it
        '''
        for device in devices:
            self.add_device(device)

    def dispatch(self, message: Message) -> None:
        '''
        dispatches a new message to all devices

        Parameters
        ----------
        message: Message
            a message object

        Example
        --------
        >>> device_coordinator.dispatch(start_message(experiment_id,
                                                      stimuli_id))
        '''

        for message_queue in self.__queues:
            message_queue.put(message)

    def health_check(self):
        '''
        Checks if all the devices are okay.

        Returns
        -----------
        boolean
            True if all are healthy, False otherwise
        '''
        for device_name, device, in self.__devices.items():
            if not device.is_alive():
                print("device [{0}] is not alive anymore.".format(device_name))
                return False
        return True

    def terminate(self):
        '''
        sends terminate message to all devices and terminate all processes

        Example
        --------
        >>> device_coordinator.terminate()
        '''
        self.dispatch(terminate_message())
        for item in self.__devices.values():
            item.join()

    def get_realtime_data(self, duration: int, device_list: Optional[List[str]]) -> Dict[str, List[Any]]:
        '''
        Returns latest collected data from all devices.
        Device's data can be anything, depending on the device itself.

        Parameters
        ----------
        duration: int
            a time duration for getting realtime data in seconds

        device_list: List[str]
            a list of device names. Only devices in this list will be monitored or processed in realtime

        Returns
        ---------
        data : dict[str, list[any]]
            The keys are device names and values are collected data from the device

        Note
        ----
        This method is being used for getting data in real-time for monitoring or realtime processing

        '''
        cached = self.__realtime_data_cache.get_cache()
        if cached:
            return cached

        out_queues: List[Tuple[QueueType, str]] = []
        # Putting request for all devices, then collecting them all, for performance reasons.
        for in_q, out_q, device in self.__realtime_data_queues:
            if device_list is None or device.name in device_list:
                try:
                    # The sub-process won't use the data we put in the queue. It's just a signal.
                    in_q.put(str(duration), timeout=0.1)
                    out_queues.append((out_q, device.name))
                except queue.Full:
                    print("Could not put realtime data request for {0} device.".format(
                        device.name), file=sys.stderr)
                    traceback.print_exc()

        result: Dict[str, List[Any]] = {}
        for out_q, device_name in out_queues:
            try:
                records = pickle.loads(out_q.get(timeout=0.1))
                # We ensured device has a name in the add_device, ignoring it here.
                result[device_name] = records  # type: ignore
            except (queue.Empty, pickle.PickleError):
                print("Could not read realtime data from {0} device".format(
                    device_name), file=sys.stderr)
                traceback.print_exc()

        self.__realtime_data_cache.cache(result)
        return result

    def __set_realtime_data_queues(self, device: Device) -> None:
        if isinstance(device, RealtimeDataDevice):
            in_q: QueueType = multiprocessing.Queue()
            out_q: QueueType = multiprocessing.Queue()
            device.set_realtime_data_queues(in_q, out_q)
            self.__realtime_data_queues.append((in_q, out_q, device))
