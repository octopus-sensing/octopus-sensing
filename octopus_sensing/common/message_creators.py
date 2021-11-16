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
# You should have received a copy of the GNU General Public License along with Foobar.
# If not, see <https://www.gnu.org/licenses/>.

from octopus_sensing.common.message import Message


class MessageType():
    '''
    Predefined message types including:

        1- START: start of a stimulus

        2- STOP: End of each stimulus

        3- TERMINATE: terminating the process of each device
    '''
    START = "START"
    STOP = "STOP"
    TERMINATE = "TERMINATE"


def start_message(experiment_id: str, stimulus_id: str, payload=None):
    '''
    Creates a message to inform device of starting the stimulus

    Parameters
    -----------
    experiment_id: str, default: None
        A unique ID for each participant and task in the study
    
    stimulus_id: str, default: None
        A unique ID for each stimulus

    payload: Any, default: None
        the message data that can have differnt values
    

    Returns
    -------
    message: Message
        A start message

    Example
    --------
    In this example, we created a stop message. When DeviceCoordinator
    dispath this message, it will be sent to all devices in its list.
    Using this message we inform all devices that stimulus `stimulus_00` has started.

    >>> message = start_message("study_1_p10", "stimulus_00")
    >>> device_coordinator.dispatch(message)

    '''
    return Message(MessageType.START,
                   payload,
                   experiment_id=experiment_id,
                   stimulus_id=stimulus_id)


def stop_message(experiment_id: str, stimulus_id: str):
    '''
    Creates a message to inform device of stopping the stimulus


    Parameters
    -----------
    experiment_id: str, default: None
        A unique ID for each participant and task in the study
    
    stimulus_id: str, default: None
        A unique ID for each stimulus
    

    Returns
    -------
    message: Message
        A start message

    Example
    --------
    In this example, we created a start message. When DeviceCoordinator
    dispath this message, it will be sent to all devices in its list.
    Using this message we inform all devices that stimulus `stimulus_00` is finished.

    >>> message = stop_message("study_1_p10", "stimulus_00")
    >>> device_coordinator.dispatch(message)

    '''
    return Message(MessageType.STOP,
                   None,
                   experiment_id=experiment_id,
                   stimulus_id=stimulus_id)


def terminate_message():
    '''
    Creates a message to inform device of terminating the program
    

    Returns
    -------
    message: Message
        A start message

    Example
    --------
    In this example, we created a terminate message. When DeviceCoordinator
    dispath this message, it will be sent to all devices in its list.
    Using this message we inform all devices to terminate.

    >>> message = terminate()
    >>> device_coordinator.dispatch(message)

    '''

    return Message(MessageType.TERMINATE,
                   None)
