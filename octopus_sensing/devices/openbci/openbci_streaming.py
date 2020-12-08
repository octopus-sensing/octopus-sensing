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

import os
import threading
import csv
import datetime
import pyOpenBCI
import numpy as np

from octopus_sensing.common.message_creators import MessageType
from octopus_sensing.devices.monitored_device import MonitoredDevice

CONTINIOUS_SAVING_MODE = 0
SEPARATED_SAVING_MODE = 1

uVolts_per_count = (4500000)/24/(2**23-1)
accel_G_per_count = 0.002 / (2**4)  # G/count


class OpenBCIStreaming(MonitoredDevice):
    def __init__(self,
                 daisy=True,
                 channels_order=None,
                 saving_mode=CONTINIOUS_SAVING_MODE,
                 **kwargs):
        super().__init__(**kwargs)

        self._saving_mode = saving_mode
        self._stream_data = []
        self._board = pyOpenBCI.OpenBCICyton(daisy=daisy)
        self._trigger = None
        self._experiment_id = None

        self.output_path = os.path.join(self.output_path, "eeg")
        os.makedirs(self.output_path, exist_ok=True)

        if channels_order is None:
            if daisy is True:
                self.channels_order = \
                    ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8", "ch9",
                     "ch10", "ch11", "ch12", "ch13", "ch14", "ch15", "ch16"]
            else:
                self.channels_order = \
                    ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8"]
        else:
            self.channels_order = channels_order
            if daisy is True:
                if len(self.channels_order) != 16:
                    raise "The number of channels in channels_order should be 16"
            elif daisy is False:
                if len(self.channels_order) != 8:
                    raise "The number of channels in channels_order should be 8"

    def _run(self):
        threading.Thread(target=self._stream_loop).start()

        while True:
            message = self.message_queue.get()
            if message is None:
                continue
            if message.type == MessageType.START:
                self.__set_trigger(message)
                self._experiment_id = message.experiment_id
            elif message.type == MessageType.STOP:
                if self._saving_mode == SEPARATED_SAVING_MODE:
                    self._experiment_id = message.experiment_id
                    file_name = \
                        "{0}/{1}-{2}-{3}.csv".format(self.output_path,
                                                     self.name,
                                                     self._experiment_id,
                                                     message.stimulus_id)
                    self._save_to_file(file_name)
                else:
                    self._experiment_id = message.experiment_id
                    self.__set_trigger(message)
            elif message.type == MessageType.TERMINATE:
                if self._saving_mode == CONTINIOUS_SAVING_MODE:
                    file_name = \
                        "{0}/{1}-{2}.csv".format(self.output_path,
                                                 self.name,
                                                 self._experiment_id)
                    self._save_to_file(file_name)
                break

        self._board.stop_stream()

    def __set_trigger(self, message):
        '''
        Takes a message and set the trigger using its data

        @param Message message: a message object
        '''
        self._trigger = \
            "{0}-{1}-{2}".format(message.type,
                                 message.experiment_id,
                                 str(message.stimulus_id).zfill(2))

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

    def _save_to_file(self, file_name):
        if not os.path.exists(file_name):
            csv_file = open(file_name, 'a')
            header = []
            header.extend(self.channels_order)
            header.extend(["acc-x", "acc-y", "acc-z"])
            header.extend(["sample_id", "time stamp", "trigger"])
            writer = csv.writer(csv_file)
            writer.writerow(header)
            csv_file.flush()
            csv_file.close()
        with open(file_name, 'a') as csv_file:
            writer = csv.writer(csv_file)
            for row in self._stream_data:
                writer.writerow(row)
                csv_file.flush()

    def _get_monitoring_data(self):
        '''Returns latest collected data for monitoring/visualizing purposes.'''
        # Last three seconds
        # FIXME: hard-coded data collection rate
        return self._stream_data[-1 * 3 * 128:]
