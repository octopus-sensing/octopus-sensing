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

import sys
import time
import traceback
import multiprocessing
import queue
import pickle

from octopus_sensing.devices.monitored_device import MonitoredDevice


class MonitoringCache:
    def __init__(self):
        self._time = time.time()
        self._last_requested_records = 0
        self._cached_data = []

    def get_cache(self, requested_records):
        '''Returns None if cache is not available or expired'''
        if requested_records != self._last_requested_records and time.time() - self._time > 100:
            return None
        return self._last_requested_records

    def cache(self, requested_records, data):
        self._last_requested_records = requested_records
        self._cached_data = data
        self._time = time.time()


class DeviceCoordinator:
    '''
    Coordinating devices
    '''

    def __init__(self):
        self.__devices = {}
        self.__queues = []
        self.__device_counter = 0
        self.__monitoring_queues = []
        self.__monitoring_cache = MonitoringCache()

    def __get_device_id(self):
        '''
        Generate an ID for devices that do not have name

        @rtype: str
        @return device_id
        '''
        self.__device_counter += 1
        device_id = "device_{0}".format(self.__device_counter)
        return device_id

    def add_device(self, device):
        '''
        Adds new device to the coordinator and starts it

        @param Device device: a device object

        @keyword str name: The name of device
        '''
        if device.device_name is None:
            device.device_name = self.__get_device_id()
        if device.device_name in self.__devices.keys():
            raise "This device already has been added"

        self.__devices[device.device_name] = device
        msg_queue = multiprocessing.Queue()
        device.set_queue(msg_queue)
        self.__queues.append(msg_queue)

        self.__set_monitoring_queues(device)

        device.start()

    def add_devices(self, devices):
        '''
        Adds new devices to the coordinator

        @param list devices: a list of device object
        @type devices: list(Device)
        '''
        for device in devices:
            self.add_device(device)

    def dispatch(self, message):
        '''
        dispatch new message to all devices

        @param Message message: a message object object
        '''
        for message_queue in self.__queues:
            message_queue.put(message)

    def get_monitoring_data(self, requested_records):
        '''
        Returns latest collected data from all devices.
        Device's data can be anything, depending on the device itself.

        @param: requested_records: Number of records to fetch from each device.
        @type requested_records: int

        @return: Dict of device name to the collected data.
        @rtype: Dict[device_name, List[Any]]
        '''
        assert isinstance(requested_records, int)

        cached = self.__monitoring_cache.get_cache(requested_records)
        if cached:
            return cached

        # Putting request for all devices, then collecting them all, for performance reasons.
        for in_q, _, device in self.__monitoring_queues:
            try:
                in_q.put(requested_records, timeout=0.1)
            except queue.Full:
                print("Could not put monitoring request for {0} device.".format(
                    device.name), file=sys.stderr)
                traceback.print_exc()

        result = {}
        for _, out_q, device in self.__monitoring_queues:
            try:
                records = pickle.loads(out_q.get(timeout=0.1))
                result[device.name] = records
            except (queue.Empty, pickle.PickleError):
                print("Could not read monitoring data from {0} device".format(
                    device.name), file=sys.stderr)
                traceback.print_exc()

        self.__monitoring_cache.cache(requested_records, result)
        return result

    def __set_monitoring_queues(self, device):
        if isinstance(device, MonitoredDevice):
            in_q = multiprocessing.Queue()
            out_q = multiprocessing.Queue()
            device.set_monitoring_queues(in_q, out_q)
            self.__monitoring_queues.append((in_q, out_q, device))
