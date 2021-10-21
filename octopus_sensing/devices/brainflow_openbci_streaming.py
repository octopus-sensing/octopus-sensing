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

import platform
from octopus_sensing.devices.brainflow_streaming import BrainFlowStreaming
from brainflow.board_shim import BrainFlowInputParams

class BrainFlowOpenBCIStreaming(BrainFlowStreaming):
    '''
    Manages OpenBCI streaming

    Data will be recorded in a csv file/files with the following column order:
    channels, Acc_x, Acc_y, Acc_z, sample_id, time_stamp, trigger

    Attributes
    -----------
    name: str, optional
        device name
        This name will be used in the output path to identify each device's data
    
    output_path: str, optional
                 The path for recording files.
                 Audio files will be recorded in folder {output_path}/{name}
    
    saving_mode: int, optional, default = SavingModeEnum.CONTINIOUS_SAVING_MODE
        The way of saving data: saving continiously in a file or save data related to
        each stimulus in a separate file. 
        SavingModeEnum: CONTINIOUS_SAVING_MODE
                        SEPARATED_SAVING_MODE
    
    board_type: str, optional, default = "cyton-daisy"
                The type of OpenBCI boards that connect by USB dongle.
                It can be:
                cyton
                    for cyton board sampling rate is 250 and it has 8 channels
                cyton-daisy
                    for cyton-daisy board sampling rate is 125 and it has 16 channels
                ganglion
                    for Ganglion board sampling rate is 200 and it has 4 channels

    channels_order: list of str, default = None
        A list of channel names which specify the order and names of channels

    Examples
    -----------
    >>> my_openbci = \
            BrainFlowOpenBCIStreaming(name="OpenBCI",
                                      output_path="./output",
                                      board_type="cyton-daisy",
                                      saving_mode=SavingModeEnum.CONTINIOUS_SAVING_MODE,
                                      channels_order=["Fp1", "Fp2", "F7", "F3", 
                                                      "F4", "F8", "T3", "C3",
                                                      "C4", "T4", "T5", "P3", 
                                                      "P4", "T6", "O1", "O2"])

    See Also
    -----------
    BrainflowStreaming
        BrainflowStreaming is managing data streaming through different boards
 
    DeviceCoordinator
        DeviceCoordinator is managing data recording by sending messages to this class 

    '''

    def __init__(self,
                 channels_order: list[str]=None,
                 borad_type:str ="cyton-daisy",
                 **kwargs):
        self.channels = channels_order
        
        if borad_type == "cyton-daisy":
            device_id = 2
            sampling_rate = 125
            if self.channels is None:
                self.channels = \
                    ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8", "ch9",
                    "ch10", "ch11", "ch12", "ch13", "ch14", "ch15", "ch16"]
            if len(self.channels) != 16:
                raise RuntimeError("The number of channels in channels_order should be 16")
        elif borad_type == "cyton":
            device_id = 0
            sampling_rate = 250
            self.channels = \
                ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8"]
            if len(self.channels) != 8:
                raise RuntimeError("The number of channels in channels_order should be 8")
        elif borad_type == "Ganglion":
            device_id = 1
            sampling_rate = 200
            self.channels = \
                ["ch1", "ch2", "ch3", "ch4"]
            if len(self.channels) != 4:
                raise RuntimeError("The number of channels in channels_order should be 4")
        else:
            raise RuntimeError("Use BrainflowStreaming fr other boards")

        if platform.system() == "Linux":
            serial_port = "/dev/ttyUSB0"
        elif platform.system() == "Windows":
            serial_port = "Com3"
        else:
            serial_port = "/dev/cu.*"

        params = BrainFlowInputParams()
        params.serial_port = serial_port
        super().__init__(device_id,
                         sampling_rate,
                         brain_flow_input_params=params,
                         **kwargs)
