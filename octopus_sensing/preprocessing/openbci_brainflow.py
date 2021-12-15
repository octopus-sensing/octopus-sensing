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
from typing import List
import pandas as pd

from octopus_sensing.preprocessing.openbci import clean_eeg
from octopus_sensing.preprocessing.utils import load_all_samples_without_time, load_all_trials_without_time
from octopus_sensing.devices.common import SavingModeEnum

def openbci_brainflow_preprocess(input_path: str, file_name: str, output_path: str,
                                 channels: List[str],
                                 saving_mode: int = SavingModeEnum.CONTINIOUS_SAVING_MODE,
                                 sampling_rate: int = 125,
                                 signal_preprocess: bool = True):
    '''
    Preprocess openbci recorded files to prepare them for visualizing and analysis
    It applys data cleaning (according to signal_preprocess), resampling (according to sampling_rate),
    and splits data if data has been recorded continuously.
    This method uses `mne library <https://mne.tools/stable/index.html>`_ for EEG data processing

    Parameters
    ----------
    input_path: str
        The path to recorded openbci data
    
    file_name: str
        The file name of recorded openbci data
    
    output_path: str
        preprocessed file path
    
    channels: List(str)
        a list of recorded channels name
    
    saving_mode: int, default: SavingModeEnum.CONTINIOUS_SAVING_MODE
        The saving mode of recorded data. If it is CONTINIOUS_SAVING_MODE, data will be splitted
        according to markers and will be recorded in the separated files

    sampling_rate: int, default: 128
        The desired sampling_rate. Data will be resampled according to this sampling rate
    
    signal_preprocess: bool, default: True
        If True will apply preliminary preprocessing steps to clean line noises
    
    Note
    -----
    Sometimes recorded data in one second with Openbci are less or more than 
    the specified sampling rate. So, we resample data by replicating
    the last samples or removing some samples to achieve the desired sampling_rate
    '''
    if saving_mode == SavingModeEnum.SEPARATED_SAVING_MODE:
        if len(channels) == 8:
            data = \
                load_all_samples_without_time(os.path.join(input_path, file_name),
                                              (1, 9))  # channel columns

        elif len(channels) == 16:
            data = \
                load_all_samples_without_time(os.path.join(input_path, file_name),
                                              (1, 17)),  # channel columns
        output_file_path = \
            "{0}/{1}".format(output_path, file_name)
        data = data[:int(len(data)/sampling_rate)*sampling_rate]
        if signal_preprocess is True:
            preprocessed_data = \
                clean_eeg(data,
                          channel_names=channels,
                          sampling_rate=sampling_rate)
        else:
            preprocessed_data = data
            # convert array into dataframe
        data_frame = pd.DataFrame(preprocessed_data, columns=channels)
        data_frame.to_csv(output_file_path, index=False)

    elif saving_mode == SavingModeEnum.CONTINIOUS_SAVING_MODE:
        if len(channels) == 8:
            trials_data, triger_list = \
                load_all_trials_without_time(os.path.join(input_path, file_name),  # File path
                                             (1, 9),  # channel columns
                                             26)  # triger column

        elif len(channels) == 16:
            trials_data, triger_list = \
                load_all_trials_without_time(os.path.join(input_path, file_name),  # File path
                                            (1, 17),  # channel columns
                                            34)  # triger column

        i = 0
        for trial in trials_data:
            output_file_path = \
                "{0}/{1}-{2}.csv".format(output_path,
                                         file_name[:-4],  # Removing .csv from file_name
                                         str(triger_list[i]).zfill(2))
            print("output_file_path", output_file_path)
            data = trial[:int(len(trial)/sampling_rate)*sampling_rate]

            if signal_preprocess is True:
                preprocessed_data = \
                    clean_eeg(data,
                              channel_names=channels,
                              sampling_rate=sampling_rate)
            else:
                preprocessed_data = data
                # convert array into dataframe
            data_frame = pd.DataFrame(preprocessed_data, columns=channels)

            # save the dataframe as a csv file
            data_frame.to_csv(output_file_path, index=False)
            i += 1
    else:
        raise Exception("Saving mode is incorrect")
