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
import array
from typing import List, Any, Dict
import datetime
import csv
import miniaudio

from octopus_sensing.devices.realtime_data_device import RealtimeDataDevice
from octopus_sensing.common.message_creators import MessageType
from octopus_sensing.devices.common import SavingModeEnum

class AudioStreaming(RealtimeDataDevice):
    '''
    Stream and Record audio

    Attributes
    ----------

    Parameters
    ----------

    device_id: int
        The audio recorder ID. If there is several audio recorder in the system
    
    name: str, optional
          device name
          This name will be used in the output path to identify each device's data
    
    output_path: str, optional
                 The path for recording files.
                 Audio files will be recorded in folder {output_path}/{name}


    Example
    -------
    If you want to know what is your audio recorder's ID run the following example  from `miniaudio <https://github.com/irmen/pyminiaudio>`_

    >>> import miniaudio
    >>> devices = miniaudio.Devices()
    >>> captures = devices.get_captures()
    >>> for d in enumerate(captures):
            print("{num} = {name}".format(num=d[0], name=d[1]['name']))

    Example
    -----------
    Creating an instance of audio recorder and adding it to the device coordinator.
    Device coordinator is responsible for triggerng the audio recorder to start or stop recording

    >>> audio_recorder = AudioStreaming(1,
    ...                                 name="Audio_monitoring",
    ...                                 output_path="./output")
    >>> device_coordinator.add_device(audio_recorder)

    See Also
    -----------
    :class:`octopus_sensing.device_coordinator`
    :class:`octopus_sensing.devices.Device`
    :class:`octopus_sensing.devices.RealtimeDataDevice`

    '''
    def __init__(self, device_id:int, 
                 saving_mode: int=SavingModeEnum.SEPARATED_SAVING_MODE, **kwargs):
        super().__init__(**kwargs)
        self.output_path = os.path.join(self.output_path, self.name)
        os.makedirs(self.output_path, exist_ok=True)

        self._device_id = device_id
        
        self._saving_mode = saving_mode
        self._stream_data: List[bytes] = []
        self._record = False
        self._terminate = False
        self._state = ""
        self._log: List[str] = []
        self._continuous_capture = False
        self._sampling_rate = 44100

    def __stream_loop(self):
        _ = yield
        while True:
            data = yield
            self._stream_data.append(data)

    def _run(self):
        devices = miniaudio.Devices()
        captures = devices.get_captures()
        selected_device = captures[self._device_id]
        capture = \
            miniaudio.CaptureDevice(buffersize_msec=1000,
                                    sample_rate=self._sampling_rate,
                                    device_id=selected_device["id"])

        recorder = self.__stream_loop()
        next(recorder)

        while True:
            message = self.message_queue.get()
            if message is None:
                continue
            if message.type == MessageType.START:
                if self._state == "START":
                    print("Audio streaming has already started")
                else:
                    if self._saving_mode == SavingModeEnum.SEPARATED_SAVING_MODE:
                        self._stream_data = []
                        capture.start(recorder)
                        self._record = True
                    else:
                        if self._continuous_capture is False:
                            capture.start(recorder)
                            self._continuous_capture = True
                            self._record = True
                        self._log.append([datetime.datetime.now(),
                                         str(message.stimulus_id).zfill(2),
                                         'MESSAGE START'])

                    self._state = "START"
            elif message.type == MessageType.STOP:
                if self._state == "STOP":
                   print("Audio streaming has already stopped")
                else:
                    if self._saving_mode == SavingModeEnum.SEPARATED_SAVING_MODE:
                        capture.stop()
                        self._record = False
                        file_name = \
                            "{0}/{1}-{2}-{3}.wav".format(self.output_path,
                                                        self.name,
                                                        message.experiment_id,
                                                        str(message.stimulus_id).zfill(2))
                        self._save_to_file(file_name, capture)
                    else:
                        self._log.append([datetime.datetime.now(),
                                         str(message.stimulus_id).zfill(2),
                                         'MESSAGE STOP'])
                        self._experiment_id = message.experiment_id
                    self._state = "STOP"
            elif message.type == MessageType.TERMINATE:
                self._terminate = True
                if self._saving_mode == SavingModeEnum.CONTINIOUS_SAVING_MODE:
                    self._log.append([datetime.datetime.now(),
                                     "-",
                                     'MESSAGE TERMINATE'])
                    capture.stop()
                    self._record = False
                    file_name = \
                        "{0}/{1}-{2}.wav".format(self.output_path,
                                                 self.name,
                                                 self._experiment_id)
                    self._save_to_file(file_name, capture)
                    self._save_log_file(f"{self.output_path}/{self.name}-{self._experiment_id}-log.csv")                    
                break

    def _save_to_file(self, file_name:str, capture:miniaudio.CaptureDevice):
        buffer = b"".join(self._stream_data)
        samples = array.array('h')
        samples.frombytes(buffer)
        sound = miniaudio.DecodedSoundFile('capture',
                                           capture.nchannels,
                                           capture.sample_rate,
                                           capture.format,
                                           samples)
        miniaudio.wav_write_file(file_name, sound)

    def _save_log_file(self, file_name:str):
        with open(file_name, 'a') as csv_file:
            writer = csv.writer(csv_file)
            for row in self._log:
                writer.writerow(row)
                csv_file.flush()

    def get_saving_mode(self):
        '''
        Gets saving mode
        
        Returns
        -----------
        saving_mode: int
            The way of saving data: saving continiously in a file or save data related to
            each stimulus in a separate file. 
            SavingModeEnum is CONTINIOUS_SAVING_MODE = 0 or SEPARATED_SAVING_MODE = 1
        '''
        return self._saving_mode
    
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
            `metadata` is a dictionary of device metadata including `sampling_rate` and `type`
        '''

        data = self._stream_data[-1 * duration * self._sampling_rate:]
        metadata = {"sampling_rate": self._sampling_rate,
                    "type": self.__class__.__name__}

        realtime_data = {"data": data,
                         "metadata": metadata}
        return realtime_data