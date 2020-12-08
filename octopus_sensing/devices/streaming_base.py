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

import csv
import threading
import multiprocessing

from octopus_sensing.devices.device import Device


class StreamingBase(Device):
    def __init__(self, message_queue: multiprocessing.queues.Queue, file_name: str):
        super().__init__()
        self._message_queue = message_queue
        self._file_name = file_name

    def _run(self):
        threading.Thread(target=self._stream_loop).start()
        while(True):
            command = self._message_queue.get()
            if command is None:
                continue
            elif command == "terminate":
                self._save_to_file()
                break
            elif str(command).isdigit() is True:
                self._trigger = command
            else:
                continue

        self._board.stop_stream()

    def _stream_loop(self):
        '''
        Streaming
        '''
        raise NotImplementedError()

    def _save_to_file(self):
        with open(self._file_name, 'a') as csv_file:
            writer = csv.writer(csv_file)
            for row in self._stream_data:
                writer.writerow(row)
