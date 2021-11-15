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

from typing import Optional, Any


class Message():
    '''
    Message class. 
    It is being used for communicating between DeviceCoordinator and various devices.
    DeviceCoordinator uses message objects to inform devices about an event

    Attributes
    ----------

    Parameters
    ----------
    type: str
        The type of message
    
    payload: Any
        the message data that can have differnt values
    
    experiment_id: str, default: None
        A unique ID for each participant and task in the study
    
    stimulus_id: str, default: None
        A unique ID for each stimulus
    

    Example
    -------
    We can create a customized message using this class, or use prepared messages in the common/message_creators.
    In this example, we created an instance of message, which its type is start. When DeviceCoordinator
    dispath this message, it will be sent to all devices in its list.
    Using this message we inform all devices that start of `stimulus_00` is happened.

    >>> message = Message("START",
    ...                   "study_1_p10",
    ...                   "stimulus_00")
    >>> device_coordinator.dispatch(message)
    '''

    def __init__(self, message_type: str, payload: Any,
                 experiment_id: Optional[str] = None,
                 stimulus_id: Optional[str] = None):
        self.type = message_type
        self.payload = payload
        self.experiment_id = experiment_id
        self.stimulus_id = stimulus_id
