from octopus_sensing.common.message import Message


class MessageType():
    START = "START"
    STOP = "STOP"
    TERMINATE = "TERMINATE"


def start_message(experiment_id: str, stimulus_id: int, payload=None):
    '''
    Creates a message to inform device of starting the stimulus

    @param str experiment_id: experiment ID
    @param int stimulus_id: stimulus ID

    @kwargs payload: Some meta data related to starting the stimulus

    @rtype: Message
    @return: a start message
    '''
    message = \
        Message(MessageType.START,
                payload,
                experiment_id=experiment_id,
                stimulus_id=stimulus_id)
    return message


def stop_message(experiment_id: str, stimulus_id: int):
    '''
    Creates a message to inform device of stopping the stimulus

    @param str experiment_id: experiment ID
    @param int stimulus_id: stimulus ID

    @rtype: Message
    @return: a stop message
    '''
    message = \
        Message(MessageType.STOP,
                None,
                experiment_id=experiment_id,
                stimulus_id=stimulus_id)
    return message


def terminate_message():
    '''
    Creates a message to inform device of terminating the program

    @rtype: Message
    @return: a terminate message
    '''
    message = \
        Message(MessageType.TERMINATE,
                None)
    return message
