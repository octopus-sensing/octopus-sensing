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
import pickle
import multiprocessing.queues
import threading
import traceback
from typing import Dict, Any

from octopus_sensing.devices.device import Device

QueueType = multiprocessing.queues.Queue


class RealtimeDataDevice(Device):
    '''
    Provides functionalities for realtime processing or monitoring a device's data. 
    For example, visualizing data in real time.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._realtime_data_in_q = None
        self._realtime_data_out_q = None

    def set_realtime_data_queues(self, realtime_data_in_q: QueueType, realtime_data_out_q: QueueType) -> None:
        '''Sets the queues for communicating with the parent process.
        It should be called before the start of the process.
        '''
        self._realtime_data_in_q = realtime_data_in_q
        self._realtime_data_out_q = realtime_data_out_q

    def run(self) -> None:
        # Ensuring queues are set.
        assert self._realtime_data_in_q is not None
        assert self._realtime_data_out_q is not None

        threading.Thread(target=self._realtime_data_loop,
                         name=self.__class__.__name__ + " realtime data thread", daemon=True) \
            .start()

        self._run()

    def _realtime_data_loop(self) -> None:
        while True:
            # There is a duration for getting data n queue
            data = self._realtime_data_in_q.get()
            duration = int(data)

            try:
                # Only 10ms timeout, because we don't want to take cpu time from the
                # main thread (data collector)
                self._realtime_data_out_q.put(
                    pickle.dumps(
                        self._get_realtime_data(duration),
                        protocol=pickle.HIGHEST_PROTOCOL),
                    timeout=0.01)

            except pickle.PickleError:
                print("Error pickling realtime data", file=sys.stderr)
                traceback.print_exc()
                # We don't want to keep the parent process waiting
                self._realtime_data_out_q(pickle.dumps(
                    [], protocol=pickle.HIGHEST_PROTOCOL))

    def _get_realtime_data(self, duration: int) -> Dict[str, Any]:
        '''
        Subclasses must implmenet this method. It should return
        a list of latest collected records.
        This method will be called in a separate thread, and should
        be thread-safe.
        Also, implmentation must return as quick as possible, to prevent
        blocking of the main thread that doing the collecting.

        Parameters
        ----------
        duration: int
            A time duration in seconds for getting the latest recorded data in realtime

        Returns
        -------
        data: Dict[str, Any]
            it includes `data`: List of records, or empty list if there's nothing.
                        `metadata`: Dict of device metadata

        '''
        raise NotImplementedError()
