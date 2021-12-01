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

import datetime
import csv
import numpy as np
from typing import List, Any, Tuple


def load_all_samples(file_path: str, channels_cols: Tuple[int, int], time_stamp_col: int, time_format: str):
    '''
    Reads the recorded data file and separate data according to the START and STOP triggers

    Parameters
    ----------
    file_path: str
        The path of recorded data
    
    channels_cols: Tuple[int, int]
        The start column and end column number of channels. 
        For example [1, 16] means column 1 to 16 in the csv file includes channels data
    
    time_stamp_col: int
        The column number of time stamp
    
    time_format: str
        The format of recorded times

    Returns
    ---------
    trial_data, converted_times: tuple(List[Any], List[datetime.datetime])

    trial_data: List[Any]
        A list of a trial's data
    
    converted_times: List[datetime.datetime]
        A list of trial's time stamps

    '''
    data = []
    times = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        i = 0
        for row in reader:
            if i == 0:
                # Skip header line
                i += 1
                continue
            data.append(np.array(row[channels_cols[0]:channels_cols[1]], dtype=np.float32))
            times.append(row[time_stamp_col])
    converted_times = str_to_times(times, time_format)
    return data, converted_times


def load_all_trials(file_path: str, channels_cols: Tuple[int, int], time_stamp_col: int, triger_col: int, time_format: str):
    '''
    Reads the recorded data files and separate data according to the START and STOP triggers

    Parameters
    ----------
    file_path: str
        The path of recorded data
    
    channels_cols: Tuple[int]
        The start column and end column number of channels. 
        For example [1, 16] means column 1 to 16 in the csv file includes channels data
    
    time_stamp_col: int
        The column number of time stamp
    
    triger_col: int
        The column number of trigger
    
    time_format: str
        The format of recorded times

    Returns
    ---------
    all_trials_data, all_trials_times, trial_numbers: 
        tuple(List[Any], List[List[datetime.datetime]], List[List[int]])

    all_trials_data: List[Any]
        A list of all trials data
    
    all_trials_times: List[List[datetime.datetime]]
        A list of all trials time stamps
    
    all_trials_times: List[List[int]]
        A list of all trials IDs
    '''
    all_trials_data = []
    all_trials_times = []
    trial_numbers = []

    action_flag = None
    data:List[Any] = []
    times: List[Any] = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')

        for i, row in enumerate(reader):
            if i == 0:
                # Ignore header
                continue
            if len(row) > triger_col:
                if row[triger_col] not in (None, ''):
                    triger = row[triger_col]
                    action = triger[0:4]
                    trial_number = int(triger[-2:])
                    if action == "STAR":
                        action_flag = 1
                    elif action == "STOP":
                        action_flag = 0
                        all_trials_data.append(data)
                        converted_times = str_to_times(times, time_format)
                        all_trials_times.append(converted_times)
                        trial_numbers.append(trial_number)
                        data = []
                        times = []
            if action_flag == 1:
                data.append(np.array(row[channels_cols[0]:channels_cols[1]], dtype=np.float32))
                times.append(row[time_stamp_col])
    return all_trials_data, all_trials_times, trial_numbers


def str_to_times(times: List[str], time_format: str):
    '''
    Convert a list of str times to datetime

    Parameters
    ----------
    times: List[str]
        A list of times in str format
    
    time_format: str:
        Fomatting time style
    
    Returns
    --------
    List[datetime.datetime]
        A list of times
    '''
    converted_times = []
    for item in times:
        try:
            time = datetime.datetime.strptime(item, time_format)
        except:
            try:
                time = datetime.datetime.strptime(item, '%H:%M:%S')
            except:
                time = datetime.datetime.strptime(item, '%Y-%m-%d %H:%M:%S')
        converted_times.append(time)
    return converted_times


def resample(data: List[Any], times: List[datetime.datetime], sampling_rate: int):
    '''
    Resamples data according to time stamps and sampling rate

    Parameters
    ----------
    data: List[Any]
        data to be resampled
    
    times: List[datetime.datetime]
        A list of timestamp. There is a timestamp for each sample of data

    sampling_rate: int
        Data will be resampled to this sampling rate
    
    Returns
    -------
    numpy.array
        An array of resampled data
    '''
    i = 0
    time_delta = datetime.timedelta(0, 1, 0)
    start_time = times[0]
    sample_start_time = start_time
    block: List[Any] = []
    all_data = []
    j = 0
    block_number = 0
    for item in data:
        if times[i] - sample_start_time > time_delta:
            block_number += 1
            if len(block) < sampling_rate:
                while len(block) < sampling_rate:
                    # repeating last item
                    block.extend(block[-(sampling_rate-len(block)):])
            elif len(block) > sampling_rate:
                # Ignoring last items
                block = block[:sampling_rate]
            all_data.extend(block)
            block = []
            sample_start_time = start_time + (block_number * time_delta)
        block.append(item)
        i += 1
    if len(block) > 0:
        if len(block) > sampling_rate/2:
            while len(block) < sampling_rate:
                # repeating last item
                block.extend(block[-(sampling_rate-len(block)):])
            block_number += 1
            all_data.extend(block)
    return np.array(all_data)


def load_all_samples_without_time(file_path: str, channels_cols: Tuple[int, int]):
    '''
    Reads the recorded data file and separate data according to the START and STOP triggers

    Parameters
    ----------
    file_path: str
        The path of recorded data
    
    channels_cols: Tuple[int, int]
        The start column and end column number of channels. 
        For example [1, 16] means column 1 to 16 in the csv file includes channels data


    Returns
    ---------
    trial_data: List[Any]
        A list of a trial's data
    '''
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            data.append(np.array(row[channels_cols[0]:channels_cols[1]], dtype=np.float32))
    return data


def load_all_trials_without_time(file_path: str, channels_cols: Tuple[int, int], triger_col: int):
    '''
    Reads the recorded data files and separate data according to the START and STOP triggers

    Parameters
    ----------
    file_path: str
        The path of recorded data
    
    channels_cols: Tuple[int, int]
        The start column and end column number of channels. 
        For example [1, 16] means column 1 to 16 in the csv file includes channels data
    
    triger_col: int
        The column number of trigger

    Returns
    ---------
    all_trials_data, trial_numbers: 
        tuple(List[Any], List[List[int]])

    all_trials_data: List[Any]
        A list of all trials data
    
    all_trials_times: List[List[int]]
        A list of all trials IDs
    '''
    all_trials_data = []
    trial_numbers = []

    action_flag = None
    data:List[Any] = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')

        for i, row in enumerate(reader):
            if len(row) > triger_col:
                if row[triger_col] not in (None, ''):
                    triger = row[triger_col]
                    action = triger[0:4]
                    trial_number = int(triger[-2:])
                    if action == "STAR":
                        action_flag = 1
                    elif action == "STOP":
                        action_flag = 0
                        all_trials_data.append(data)
                        trial_numbers.append(trial_number)
                        data = []
            if action_flag == 1:
                data.append(np.array(row[channels_cols[0]:channels_cols[1]], dtype=np.float32))
    return all_trials_data, trial_numbers