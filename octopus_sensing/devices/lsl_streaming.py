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

import threading
from typing import Optional

from octopus_sensing.common.message_creators import MessageType
from octopus_sensing.devices.device import Device


class LSLStreaming(Device):

    def __init__(self,
                 name: Optional[str] = None,
                 output_path: str = "output"):
        super().__init__(name=name, output_path=output_path)
        self._terminate = False

    def _run(self):
        threading.Thread(target=self._message_loop).start()

        while True:
            # The main thread.
            # Do all the communication with LSL here.
            if self._terminate is True:
                break

    def _message_loop(self):
        while True:
            message = self.message_queue.get()
            if message is None:
                continue

            if message.type == MessageType.START:
                self.__set_trigger(message)
                self._experiment_id = message.experiment_id

            elif message.type == MessageType.STOP:
                self._experiment_id = message.experiment_id
                self.__set_trigger(message)
                # Probably you want to write the data to the file here.

            elif message.type == MessageType.TERMINATE:
                self._terminate = True
                break

    def __set_trigger(self, message):
        '''
        Takes a message and set the trigger using its data

        Parameters
        ----------
        message: Message
            a message object
        '''
        # Add the trigger to the data
