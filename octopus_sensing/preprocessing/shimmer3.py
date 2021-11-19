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
import heartpy as hp
from scipy import signal
import numpy as np
import pathlib

from octopus_sensing.preprocessing.utils import load_all_trials, resample, load_all_samples
from octopus_sensing.devices.common import SavingModeEnum


def shimmer3_preprocess(input_path: str, file_name: str, output_path: str,
                        saving_mode: int = SavingModeEnum.CONTINIOUS_SAVING_MODE,
                        sampling_rate: int = 128,
                        signal_preprocess: bool = True):
    '''
    Preprocess shimmer recorded files to prepare them for visualizing and analysis
    It applys data cleaning (according to signal_preprocess), resampling (according to sampling_rate),
    and splits data if data has been recorded continuously. It will save PPG and GSR data in separated files

    Parameters
    ----------
    input_path: str
        The path to recorded shimmer data
    
    file_name: str
        The file name of recorded shimmer data
    
    output_path: str
        preprocessed file path
    
    saving_mode: int, default: SavingModeEnum.CONTINIOUS_SAVING_MODE
        The saving mode of recorded data. If it is CONTINIOUS_SAVING_MODE, data will be splitted
        according to markers and will be recorded in the separated files

    sampling_rate: int, default: 128
        The desired sampling_rate. Data will be resampled according to this sampling rate
    
    signal_preprocess: bool, default: True
        If True will apply preliminary preprocessing steps to clean line noises
    
    Note
    -----
    Sometimes recorded data in one second with Shimmer3 are less or more than 
    the specified sampling rate. So, we resample data by replicating
    the last samples or removing some samples to achieve the desired sampling_rate
    '''
    if saving_mode == SavingModeEnum.SEPARATED_SAVING_MODE:
        data, times = \
            load_all_samples(os.path.join(input_path, file_name),
                             (5, 7),
                             7,
                             '%Y-%m-%d %H:%M:%S.%f')
        resampled_data = \
            resample(data, times, sampling_rate)
        if signal_preprocess is True:
            cleaned_gsr = \
                clean_gsr(resampled_data[:, 0],
                          sampling_rate)
            cleaned_ppg = \
                clean_ppg(resampled_data[:, 1],
                          sampling_rate)
        else:
            cleaned_gsr = resampled_data[:, 0]
            cleaned_ppg = resampled_data[:, 1]

        gsr_output_path = os.path.join(output_path, "gsr")
        if not os.path.exists(gsr_output_path):
            pathlib.Path(gsr_output_path).mkdir(parents=True, exist_ok=True)
        gsr_file_path = \
            "{0}/gsr{1}".format(gsr_output_path, file_name[7:])
        
        ppg_output_path = os.path.join(output_path, "ppg")
        if not os.path.exists(ppg_output_path):
            pathlib.Path(ppg_output_path).mkdir(parents=True, exist_ok=True)
        ppg_file_path = \
            "{0}/ppg{1}".format(ppg_output_path, file_name[7:])
        np.savetxt(gsr_file_path, cleaned_gsr)
        np.savetxt(ppg_file_path, cleaned_ppg)

    elif saving_mode == SavingModeEnum.CONTINIOUS_SAVING_MODE:
        print("shimmer input_path", input_path)
        # First data needs to be splitted based on markers
        trials_data, trials_times, triger_list = \
            load_all_trials(os.path.join(input_path, file_name),  # File path
                            (5, 7),  # channel columns
                            7,  # timestamp column
                            8,  # triger column
                            '%Y-%m-%d %H:%M:%S.%f')  # timestamp format

        i = 0
        for trial in trials_data:
            gsr_output_path = os.path.join(output_path, "gsr")
            if not os.path.exists(gsr_output_path):
                pathlib.Path(gsr_output_path).mkdir(parents=True, exist_ok=True)
            gsr_file_path = \
                "{0}/gsr{1}-{2}.csv".format(gsr_output_path,
                                            # Removing .csv and shimmer from file_name
                                            file_name[7:-4],
                                            str(triger_list[i]).zfill(2))
            ppg_output_path = os.path.join(output_path, "ppg")
            if not os.path.exists(ppg_output_path):
                pathlib.Path(ppg_output_path).mkdir(parents=True, exist_ok=True)
            ppg_file_path = \
                "{0}/ppg{1}-{2}.csv".format(ppg_output_path,
                                            # Removing .csv and shimmer from file_name
                                            file_name[7:-4],
                                            str(triger_list[i]).zfill(2))

            resampled_data = \
                resample(trial, trials_times[i], sampling_rate)

            if signal_preprocess is True:
                print("shape", resampled_data.shape)
                cleaned_gsr = \
                    clean_gsr(resampled_data[:, 0],
                              sampling_rate)
                cleaned_ppg = \
                    clean_ppg(resampled_data[:, 1],
                              sampling_rate)
            else:
                cleaned_gsr = resampled_data[:, 0]
                cleaned_ppg = resampled_data[:, 1]

            np.savetxt(gsr_file_path, cleaned_gsr)
            np.savetxt(ppg_file_path, cleaned_ppg)
            i += 1
    else:
        raise Exception("Saving mode is incorrect")


def clean_gsr(data, sampling_rate: int, low_pass: float=0.1, high_pass: float=15):
    '''
    Removes high frequency and rapid transient noises

    Parameters
    -----------
    data: numpy.array
        An 1D array of GSR data

    smpling_rate: int, default: 128
        sampling rate

    low_pass: float, default: 0.7
        The low cut frequency for filtering
    
    high_pass: float, default: 2.5
        The high cut frequency for filtering
    
    Returns
    -------
    cleaned_data: numpy.array
        An 1D array of cleaned GSR data
    '''
    nyqs = sampling_rate * 0.5
    # Removing high frequency noises
    b, a = signal.butter(5, [low_pass / nyqs, high_pass / nyqs], 'bands')
    output = signal.filtfilt(b, a, np.array(data, dtype=np.float64))

    # Removing rapid transient artifacts
    final_output = signal.medfilt(output, kernel_size=5)
    return final_output


def clean_ppg(data: np.ndarray, sampling_rate: int, low_pass: float=0.7, high_pass: float=2.5):
    '''
    Removes high frequency noises

    It uses `heartpy <https://github.com/paulvangentcom/heartrate_analysis_python>` library

    Parameters
    -----------
    data: numpy.ndarray
        An 1D array of PPG data

    smpling_rate: int, default: 128
        sampling rate

    low_pass: float, default: 0.7
        The low cut frequency for filtering
    
    high_pass: float, default: 2.5
        The high cut frequency for filtering
    
    Returns
    -------
    cleaned_data: numpy.array
        An 1D array of cleaned PPG data

    '''
    filtered = hp.filter_signal(data,
                                [low_pass, high_pass],
                                sample_rate=sampling_rate,
                                order=3,
                                filtertype='bandpass')

    return filtered
