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

        4- SAVE: Save the data in the file
    '''
    START = "START"
    STOP = "STOP"
    TERMINATE = "TERMINATE"
    SAVE = "SAVE"


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

def save_message(experiment_id: str):
    '''
    Creates a message to inform device of saving the data in the file
    This message is used when the data is saved in a continuous mode for partial save of data several times during the experiment.
    After receiving this message, the device will save the data in a file with the name and clear the data in memory.
    It will takes some time to save the data in the file, so after sending a message, wait for a short time to make sure IO is done.
    it is recommended to use this message several times in the long duration experiments to avoid losing data in case of unexpected termination of the program.
    The device will continue data recording by sending the next start message.
    
    Parameters
    -----------
    experiment_id: str, default: None
        A unique ID for each participant and task in the study

    Returns
    -------
    message: Message
        A save message

    Example
    --------
    In this example, we created a save message. When DeviceCoordinator
    dispath this message, it will be sent to all devices in its list.
    Using this message we inform all devices to save the data in file.

    >>> message = save_message("study_1_p10")
    >>> device_coordinator.dispatch(message)

    '''

    return Message(MessageType.SAVE,
                   None,
                   experiment_id=experiment_id)

def terminate_message():
    '''
    Creates a message to inform device of terminating the program
    

    Returns
    -------
    message: Message
        A terminate message

    Example
    --------
    In this example, we created a terminate message. When DeviceCoordinator
    dispath this message, it will be sent to all devices in its list.
    Using this message we inform all devices to terminate.

    >>> message = terminate_message()
    >>> device_coordinator.dispatch(message)

    '''

    return Message(MessageType.TERMINATE,
                   None)


