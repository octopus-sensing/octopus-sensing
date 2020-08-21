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

from octopus_sensing.config import processing_unit
import multiprocessing

class Device(multiprocessing.Process):
    def __init__(self, name):
        super().__init__()
        self.device_name = None
        self.message_queue = None
        self.subject_id = None
        self.stimulus_id = None
        self.output_path = "output"
        self.name = name

    def run(self):
        raise NotImplementedError()

    def set_queue(self, queue):
        '''
        Sets message queue for the device

        @param queue: a queue that will be used for message passing
        '''
        self.message_queue = queue
