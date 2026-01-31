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

# pyright: reportUnusedImport=false

print('Importing for the first time. Checking installed devices.')
print('For not installed devices, please refer to the documentation for installation instructions.')

print('OpenVibeStreaming.................Installed')
from octopus_sensing.devices.open_vibe_streaming import OpenVibeStreaming
print('TestDeviceStreaming...............Installed')
from octopus_sensing.devices.testdevice_streaming import TestDeviceStreaming
print('SocketNetworkDevice...............Installed')
from octopus_sensing.devices.network_devices.socket_device import SocketNetworkDevice
print('HttpNetworkDevice.................Installed')
from octopus_sensing.devices.network_devices.http_device import HttpNetworkDevice

print('Shimmer3Streaming.................', end='')
try:
    from octopus_sensing.devices.shimmer3_streaming import Shimmer3Streaming
    print('Installed')
except ImportError:
    print('Not Installed')

print('BrainFlowOpenBCIStreaming.........', end='')
try:
    from octopus_sensing.devices.brainflow_openbci_streaming import BrainFlowOpenBCIStreaming
    print('Installed')
except ImportError:
    print('Not Installed')

print('CameraStreaming...................', end='')
try:
    from octopus_sensing.devices.camera_streaming import CameraStreaming
    print('Installed')
except ImportError:
    print('Not Installed')

print('AudioStreaming....................', end='')
try:
    from octopus_sensing.devices.audio_streaming import AudioStreaming
    print('Installed')
except ImportError:
    print('Not Installed')

print('BrainFlowStreaming................', end='')
try:
    from octopus_sensing.devices.brainflow_streaming import BrainFlowStreaming
    print('Installed')
except ImportError:
    print('Not Installed')

print('LslStreaming......................', end='')
try:
    from octopus_sensing.devices.lsl_streaming import LslStreaming
    print('Installed')
except ImportError:
    print('Not Installed')

print('TobiiGlassesStreaming.............', end='')
try:
    from octopus_sensing.devices.tobiiglasses_streaming import TobiiGlassesStreaming
    print('Installed')
except ImportError:
    print('Not Installed')

