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


class SavingModeEnum():
    '''
    In CONTINIOUS_SAVING_MODE all data will be saved in one file, and some markers
    will be used to specify an event. In SEPARATED_SAVING_MODE, the data related to different events
    will be saved in separate files. 
    For example, if stimuli is a list of videos, in CONTINIOUS_SAVING_MODE, the data recorded
    during displaying all videos, will be recorded in a file and two markers one for start 
    and one for the stop of each video will be recorded in the data. In SEPARATED_SAVING_MODE for 
    each video stimuli, the data recorded while displaying each video will be recorded in 
    a separated file.


    '''
    CONTINIOUS_SAVING_MODE = 0
    SEPARATED_SAVING_MODE = 1
