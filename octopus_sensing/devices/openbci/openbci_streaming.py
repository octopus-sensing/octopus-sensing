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

import threading
import csv
import datetime
import pyOpenBCI
import numpy as np

from octopus_sensing.devices.device import Device

CONTINIOUS_SAVING_MODE = 0
SEPARATED_SAVING_MODE = 1

uVolts_per_count = (4500000)/24/(2**23-1)
accel_G_per_count = 0.002 / (2**4) #G/count

class OpenBCIStreaming(Device):
    def __init__(self, saving_mode=CONTINIOUS_SAVING_MODE):
        super().__init__()
        self._saving_mode = saving_mode
        self._stream_data = []
        self._board = pyOpenBCI.OpenBCICyton(daisy=True)
        self._trigger = None

    def run(self):
        threading.Thread(target=self._stream_loop).start()
        while True:
            message = self.message_queue.get()
            if message is not None:
                self.subject_id = message.subject_id
                self.stimulus_id = message.stimulus_id
            if message is None:
                continue
            elif message.type == "trigger":
                self._trigger = message.payload
            elif message.type == "terminate":
                self._save_to_file()
                break
            else:
                continue

        self._board.stop_stream()

    def _stream_loop(self):
        self._board.start_stream(self._stream_callback)

    def _stream_callback(self, sample):
        data = np.array(sample.channels_data) * uVolts_per_count
        acc_data = np.array(sample.aux_data) * accel_G_per_count
        data_list = list(data) + list(acc_data)
        data_list.append(sample.id)
        data_list.append(str(datetime.datetime.now().time()))
        if self._trigger is not None:
            data_list.append(self._trigger)
            self._trigger = None
        self._stream_data.append(data_list)
        self._writer.writerow(data_list)

    def _save_to_file(self):
        if self._saving_mode == CONTINIOUS_SAVING_MODE:
            file_name = "{0}/eeg/{1}-{2}.csv".format(self.output_path,
                                                     self.device_name,
                                                     self.subject_id)
        else:
            file_name = "{0}/eeg/{1}-{2}-{3}.csv".format(self.output_path,
                                                         self.device_name,
                                                         self.subject_id,
                                                         self.stimulus_id)
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for row in self._stream_data:
                writer.writerow(row)
                csv_file.flush()
