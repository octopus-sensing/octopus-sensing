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

from datetime import datetime
import time
import os
import threading
import csv
import numpy as np
from typing import List, Optional, Dict, Any

from octopus_sensing.common.message_creators import MessageType
from octopus_sensing.devices.realtime_data_device import RealtimeDataDevice
from octopus_sensing.devices.common import SavingModeEnum

from libtobiiglassesctrl import TobiiGlassesController


class TobiiGlassesStreaming(RealtimeDataDevice):
    '''
    Manage Tobii Glasses streaming

    Attributes
    ----------
    device_ip
        Device IP address. (e.g.192.168.71.50)

    sampling_rate
        the sampling rate for recording data


    name
        device name
        This name will be used in the output path to identify each device's data

    output_path
        The path for recording files.
        Recorded files will be recorded in folder {output_path}/{name}

    saving_mode
        The way of saving data. It saves data continiously in a file
        or saves data which are related to various stimulus in separate files.
        default is SavingModeEnum.CONTINIOUS_SAVING_MODE
        SavingModeEnum is [CONTINIOUS_SAVING_MODE, SEPARATED_SAVING_MODE]
    
    Notes
    -----
    This class is used for reading data from Tobii Pro Glasses 2.
    It uses the `libtobiiglassesctrl` library to connect to the device and read data.
    The output file is in CSV format and its columns are as follows:
    [ac_ts, ac_x, ac_y, ac_z,
    gy_ts, gy_x, gy_y, gy_z,
    right_eye_pc_ts, right_eye_pc_x, right_eye_pc_y, right_eye_pc_z,
    right_eye_pd_ts, right_eye_pd,
    right_eye_gd_ts, right_eye_gd_x, right_eye_gd_y, right_eye_gd_z,
    left_eye_pc_ts, left_eye_pc_x, left_eye_pc_y, left_eye_pc_z,
    left_eye_pd_ts, left_eye_pd,
    left_eye_gd_ts, left_eye_gd_x, left_eye_gd_y, left_eye_gd_z,
    gp_ts, gp_l, gp_x, gp_y,
    gp3_ts, gp3_x, gp3_y, gp3_z,
    timestamp,
    trigger]
    ts: timestamp for each sensor
    ac: accelometer data
    gy: gyroscope data  
    pc: pupil center
    pd: pupil diameter
    gd: gaze direction
    gp: gaze position
    gp3: 3D gaze position
    timestamp: the time when the data is recorded
    The `trigger` column is used to identify the stimuli marker

    See Also
    -----------
    :class:`octopus_sensing.device_coordinator`
    :class:`octopus_sensing.devices.device`

    Examples
    ---------
    Here is an example of using Tobii pro glasses 2 for reading data

    >>> params.serial_port = "/dev/ttyUSB0"
    >>> my_tobiiglasses =
    ...       TobiGlassesStreaming("192.168.71.50",
    ...                            50,
    ...                            name="tobii_glasses",
    ...                            output_path="./output",
    ...                            saving_mode=SavingModeEnum.CONTINIOUS_SAVING_MODE)

    '''
    def __init__(self,
                 device_ip: str,
                 sampling_rate: int,
                 saving_mode: int=SavingModeEnum.CONTINIOUS_SAVING_MODE,
                 name: Optional[str] = None,
                 output_path: str = "output"):
        super().__init__(name=name, output_path=output_path)

        self._saving_mode = saving_mode
        self._stream_data: List[float] = []
        self.sampling_rate = sampling_rate

        self._board = None
        self._device_ip = device_ip
        self._terminate = False
        self._trigger = None
        self._experiment_id = None
        self.__loop_thread: Optional[threading.Thread] = None
        self._controller = None

        self.output_path = os.path.join(self.output_path, self.name)
        os.makedirs(self.output_path, exist_ok=True)
        self._state = ""

    def _run(self):
        self._controller = TobiiGlassesController("192.168.71.50")
        print("TobiiGlasses streaming: Connecting to the device...")
        print(self._controller.get_battery_status())
        
        self.__loop_thread = threading.Thread(target=self._stream_loop)
        self.__loop_thread.start()

        while True:
            message = self.message_queue.get()

            if not self.__loop_thread.is_alive():
                print("TobiiGlasses streaming: The streaming thread is dead. Terminating.")
                break

            if message is None:
                continue

            if message.type == MessageType.START:
                if self._state == "START":
                    print("TobiiGlasses streaming has already recorded the START triger")
                else:
                    print("TobiiGlasses start")
                    self.__set_trigger(message)
                    self._experiment_id = message.experiment_id
                    self._state = "START"
            elif message.type == MessageType.STOP:
                if self._state == "STOP":
                    print("Tobii glasses streaming has already recorded the STOP triger")
                else:
                    print("Tobii glasses stop")
                    if self._saving_mode == SavingModeEnum.SEPARATED_SAVING_MODE:
                        self._experiment_id = message.experiment_id
                        file_name = \
                            "{0}/{1}-{2}-{3}.csv".format(self.output_path,
                                                        self.name,
                                                        self._experiment_id,
                                                        message.stimulus_id)
                        self._save_to_file(file_name)
                        self._stream_data = []
                    else:
                        self._experiment_id = message.experiment_id
                        self.__set_trigger(message)
                    self._state = "STOP"
            elif message.type == MessageType.SAVE:
                if self._saving_mode == SavingModeEnum.CONTINIOUS_SAVING_MODE:
                    self._experiment_id = message.experiment_id
                    file_name = \
                        "{0}/{1}-{2}.csv".format(self.output_path,
                                                 self.name,
                                                 self._experiment_id)
                    self._save_to_file(file_name)
                    self._stream_data = []
            elif message.type == MessageType.TERMINATE:
                self._terminate = True
                if self._saving_mode == SavingModeEnum.CONTINIOUS_SAVING_MODE:
                    file_name = \
                        "{0}/{1}-{2}.csv".format(self.output_path,
                                                 self.name,
                                                 self._experiment_id)
                    self._save_to_file(file_name)
                break

        self._controller.stop_streaming()
        self._controller.close()
        self.__loop_thread.join()

    def _stream_loop(self):
        self._controller.start_streaming()
        while True:
            if self._terminate is True:
                break
            data = self.__safe_get(self._controller.get_data())
            
            if self._trigger is not None:
                data.append(self._trigger)
                self._trigger = None

            self._stream_data.append(np.array(data))
            time.sleep(1/self.sampling_rate)

    def __set_trigger(self, message):
        '''
        Takes a message and set the trigger using its data

        Parameters
        ----------
        message: Message
            a message object
        '''
        self._trigger = \
            "{0}-{1}-{2}".format(message.type,
                                 message.experiment_id,
                                 str(message.stimulus_id).zfill(2))

    def _save_to_file(self, file_name):
        print("Saving {0} to file {1}".format(self._name, file_name))
        header = ["ac_ts", "ac_x", "ac_y", "ac_z",
                  "gy_ts", "gy_x", "gy_y", "gy_z",
                  "left_eye_pc_ts", "left_eye_pc_x", "left_eye_pc_y", "left_eye_pc_z",
                  "left_eye_pd_ts", "left_eye_pd",
                  "left_eye_gd_ts", "left_eye_gd_x", "left_eye_gd_y", "left_eye_gd_z",
                  "right_eye_pc_ts", "right_eye_pc_x", "right_eye_pc_y", "right_eye_pc_z",
                  "right_eye_pd_ts", "right_eye_pd",
                  "right_eye_gd_ts", "right_eye_gd_x", "right_eye_gd_y", "right_eye_gd_z",
                  "gp_ts", "gp_l", "gp_x", "gp_y",
                  "gp3_ts", "gp3_x", "gp3_y", "gp3_z",
                  "timestamp",
                  "trigger"]
        with open(file_name, 'a') as csv_file:
            writer = csv.writer(csv_file)
            if os.stat(file_name).st_size == 0:
                print("TobiiGlassesStreaming: file created")
                writer.writerow(header)
                csv_file.flush()
            print("TobiiGlassesStreaming: file already exists, appending data")
            for row in self._stream_data:
                writer.writerow(row)
                csv_file.flush()
        print("Saving {0} to file {1} is done".format(self._name, file_name))


    def _get_realtime_data(self, duration: int) -> Dict[str, Any]:
        '''
        Returns n seconds (duration) of latest collected data for monitoring/visualizing or
        realtime processing purposes.

        Parameters
        ----------
        duration: int
            A time duration in seconds for getting the latest recorded data in realtime

        Returns
        -------
        data: Dict[str, Any]
            The keys are `data` and `metadata`.
            `data` is a list of records, or empty list if there's nothing.
            `metadata` is a dictionary of device metadata including `sampling_rate` and `channels` and `type`

        '''
        # Last seconds of data

        data = self._stream_data[-1 * duration * self.sampling_rate:]
        metadata = {"sampling_rate": self.sampling_rate,
                    "type": self.__class__.__name__}

        realtime_data = {"data": data,
                  "metadata": metadata}
        return realtime_data


    def __safe_get(self, data):
        '''
        Safely get nested dictionary values with fallback to None.
        Parameters
        ----------
        data: dict
            The data dictionary to extract values from.
        Returns
        -------
        flat_data: list
            A flat list of values extracted from the nested dictionary.
        '''
        flat_data = []
        mems = data.get("mems", [None]*8)
        if isinstance(mems, dict):
            mems_ac = mems.get("ac", [None]*4)
            if isinstance(mems_ac, dict):
                flat_data.extend([mems_ac.get("ts", None), *mems_ac.get("ac", [None]*3)])
            mems_gy = mems.get("gy", [None]*4)
            if isinstance(mems_gy, dict):
                flat_data.extend([mems_gy.get("ts", None), *mems_gy.get("gy", [None]*3)])
        left_eye = data.get("left_eye", [None]*10)
        if isinstance(left_eye, dict):
            left_pc = left_eye.get("pc", [None]*4)
            if isinstance(left_pc, dict):
                flat_data.extend([left_pc.get("ts", None), *left_pc.get("pc", [None]*3)])

            left_pd = left_eye.get("pd", [None, None])
            flat_data.extend([left_pd.get("ts", None), left_pd.get("pd", None)])

            left_gd = left_eye.get("gd", [None]*4)
            if isinstance(left_gd, dict):
                flat_data.extend([left_gd.get("ts", None), *left_gd.get("gd", [None]*3)]) 
        right_eye = data.get("right_eye", [None]*10)
        if isinstance(right_eye, dict):
            right_pc = right_eye.get("pc", [None]*4)
            if isinstance(right_pc, dict):
                flat_data.extend([right_pc.get("ts", None), *right_pc.get("pc", [None]*3)])

            right_pd = right_eye.get("pd", [None, None])
            flat_data.extend([right_pd.get("ts", None), right_pd.get("pd", None)])

            right_gd = right_eye.get("gd", [None]*4)
            if isinstance(right_gd, dict):
                flat_data.extend([right_gd.get("ts", None), *right_gd.get("gd", [None]*3)])
        gp = data.get("gp", [None]*4)
        if isinstance(gp, dict):
            flat_data.extend([gp.get("ts", None), gp.get("l", None), *gp.get("gp", [None]*2)])
        gp3 = data.get("gp3", [None]*4)
        if isinstance(gp3, dict):
            flat_data.extend([gp3.get("ts", None), *gp3.get("gp3", [None]*3)])
        flat_data.append(time.time())

        return flat_data
    
