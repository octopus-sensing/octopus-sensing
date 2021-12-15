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
import pathlib
from typing import List, Dict
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.devices.openbci_streaming import OpenBCIStreaming
from octopus_sensing.devices import BrainFlowOpenBCIStreaming
from octopus_sensing.devices import Shimmer3Streaming
from octopus_sensing.preprocessing.openbci import openbci_preprocess
from octopus_sensing.preprocessing.openbci_brainflow import openbci_brainflow_preprocess
from octopus_sensing.preprocessing.shimmer3 import shimmer3_preprocess


def preprocess_devices(device_coordinator: DeviceCoordinator, output_path: str,
                       openbci_sampling_rate: int = 128,
                       shimmer3_sampling_rate: int = 128,
                       signal_preprocess: bool = True):
    '''
    Preprocees recorded files for all devices that are added to device_coordinator and has a 
    preprocessing module. Some devices do not have any preprocessing, so this function will ignore them

    Parameters
    ----------
    device_coordinator: DeviceCoordinator
        an instance of DeviceCoordinator
    
    output_path: str
        Path for preprocessed Files
    
    openbci_sampling_rate: int
        New sampling rate for openbci resampling
    
    shimmer3_sampling_rate: int
        New sampling rate for shimmer3 resampling
    '''
    print("Start preprocessing ....")
    devices = device_coordinator.get_devices()
    for device in devices:
        if isinstance(device, OpenBCIStreaming):
            device_output_path = os.path.join(output_path, device.get_name())
            print("device_output_path", device_output_path)
            if not os.path.exists(device_output_path):
                pathlib.Path(device_output_path).mkdir(parents=True, exist_ok=True)

            # This is the path that device saves recording data
            input_path = device.get_output_path()
            print("input_path", input_path)
            file_names = os.listdir(input_path)
            file_names.sort()
            if not os.path.exists(device_output_path):
                os.mkdir(device_output_path)
            for file_name in file_names:
                openbci_preprocess(input_path, file_name, device_output_path,
                                   device.get_channels(),
                                   saving_mode=device.get_saving_mode(),
                                   sampling_rate=openbci_sampling_rate,
                                   signal_preprocess=signal_preprocess)
        elif isinstance(device, BrainFlowOpenBCIStreaming):
            device_output_path = os.path.join(output_path, device.get_name())
            print("device_output_path", device_output_path)
            if not os.path.exists(device_output_path):
                pathlib.Path(device_output_path).mkdir(parents=True, exist_ok=True)

            # This is the path that device saves recording data
            input_path = device.get_output_path()
            print("input_path", input_path)
            file_names = os.listdir(input_path)
            file_names.sort()
            if not os.path.exists(device_output_path):
                os.mkdir(device_output_path)
            for file_name in file_names:
                openbci_brainflow_preprocess(input_path, file_name, device_output_path,
                                             device.get_channels(),
                                             saving_mode=device.get_saving_mode(),
                                             sampling_rate=openbci_sampling_rate,
                                             signal_preprocess=signal_preprocess)
        elif isinstance(device, Shimmer3Streaming):
            device_output_path = os.path.join(output_path, device.get_name())
            if not os.path.exists(device_output_path):
                pathlib.Path(device_output_path).mkdir(parents=True, exist_ok=True)

            # This is the path that device saves recording data

            input_path = device.get_output_path()
            file_names = os.listdir(input_path)
            file_names.sort()
            print("preprocess shimmer input_path", input_path)
            print("preprocess shimmer device_output_path", device_output_path)
            for file_name in file_names:
                shimmer3_preprocess(input_path, file_name, device_output_path,
                                    saving_mode=device.get_saving_mode(),
                                    sampling_rate=shimmer3_sampling_rate,
                                    signal_preprocess=signal_preprocess)
    print("Preprocessing done")


def preprocess_devices_by_path(devices_path: Dict[str, str], output_path: str,
                       openbci_channels: List[str] = ["Fp1", "Fp2", "F7", "F3", "F4", "F8", "T3", "C3",
                        "C4", "T4", "T5", "P3", "P4", "T6", "O1", "O2"],
                       openbci_sampling_rate: int = 128,
                       shimmer3_sampling_rate: int = 128,
                       signal_preprocess: bool = True):
    '''
    Gets a list of path to the recorded data from different devices and preprocess them if they have  
    preprocessing module. Some devices do not have any preprocessing, so this function will ignore them

    Parameters
    ----------
    devices_path: dict[str, str]
        a dictionary of device_name: data_path that specify the path to recorded data by each device
       
    output_path: str
        Path for preprocessed Files
    
    openbci_channels: List[str]
        default is ["Fp1", "Fp2", "F7", "F3", "F4", "F8", "T3", "C3", "C4", "T4", "T5", "P3", "P4", "T6", "O1", "O2"]
        A list of OpenBCI channels' names
    
    openbci_sampling_rate: int
        New sampling rate for openbci resampling
    
    shimmer3_sampling_rate: int
        New sampling rate for shimmer3 resampling
    '''

    print("Start preprocessing ....")
    for device, input_path in devices_path.items():
        print(device, input_path)
        if device == "openbci":
            device_output_path = os.path.join(output_path, "openbci")
            print("device_output_path", device_output_path)
            if not os.path.exists(device_output_path):
                pathlib.Path(device_output_path).mkdir(parents=True, exist_ok=True)

            # This is the path that device saves recording data
            print("input_path", input_path)
            file_names = os.listdir(input_path)
            file_names.sort()
            if not os.path.exists(device_output_path):
                os.mkdir(device_output_path)
            for file_name in file_names:
                print(file_name, device_output_path)
                openbci_preprocess(input_path, file_name, device_output_path,
                                   openbci_channels,
                                   sampling_rate=openbci_sampling_rate,
                                   signal_preprocess=signal_preprocess)
        elif device == "openbci_brainflow":
            device_output_path = os.path.join(output_path, "openbci_brainflow")
            print("device_output_path", device_output_path)
            if not os.path.exists(device_output_path):
                pathlib.Path(device_output_path).mkdir(parents=True, exist_ok=True)

            # This is the path that device saves recording data
            print("input_path", input_path)
            file_names = os.listdir(input_path)
            file_names.sort()
            if not os.path.exists(device_output_path):
                os.mkdir(device_output_path)
            for file_name in file_names:
                print(file_name, device_output_path)
                openbci_brainflow_preprocess(input_path, file_name, device_output_path,
                                             openbci_channels,
                                             sampling_rate=openbci_sampling_rate,
                                             signal_preprocess=signal_preprocess)
        elif device == "shimmer3":
            device_output_path = output_path
            print("device_output_path", device_output_path)
            if not os.path.exists(device_output_path):
                pathlib.Path(device_output_path).mkdir(parents=True, exist_ok=True)

            # This is the path that device saves recording data
            print("input_path", input_path)
            if not os.path.exists(device_output_path):
                pathlib.Path(device_output_path).mkdir(parents=True, exist_ok=True)
            file_names = os.listdir(input_path)
            file_names.sort()
            print("preprocess shimmer input_path", input_path)
            print("preprocess shimmer device_output_path", device_output_path)
            for file_name in file_names:
                shimmer3_preprocess(input_path, file_name, device_output_path,
                                    sampling_rate=shimmer3_sampling_rate,
                                    signal_preprocess=signal_preprocess)
    print("Preprocessing done")
