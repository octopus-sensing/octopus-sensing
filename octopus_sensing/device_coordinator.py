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

import multiprocessing


class DeviceCoordinator():
    '''
    Coordinating devices
    '''
    def __init__(self):
        self.devices = []
        self.quesues = []
        self.__device_counter = 0

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
        Adds new device to the coordinator

        @param Device device: a device object

        @keyword str name: The name of device
        '''
        if device in self.devices:
            raise "This device already has been added"
        if device.device_name is None:
            device.device_name = self.__get_device_id()

        self.devices.append(device)
        queue = multiprocessing.Queue()
        device.set_queue(queue)
        self.quesues.append(queue)

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
        for queue in self.quesues:
            queue.put(message)
