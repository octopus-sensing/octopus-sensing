from octopus_sensing.common.message import Message

class MessageType():
    START = "START"
    STOP = "STOP"
    TERMINATE = "TERMINATE"

class ControlMessage():
    '''
    Managing control messages
    '''
    def __init__(self, experiment_id, stimulus_id):
        self.experiment_id = experiment_id
        self.stimulus_id = stimulus_id

    def start_message(self, payload=None):
        '''
        Creates a message to inform device from starting the stimulus

        @rtype: Message
        @return: a start message
        '''
        start_message = \
            Message(MessageType.START,
                    payload,
                    experiment_id=self.experiment_id,
                    stimulus_id=self.stimulus_id)
        return start_message


    def stop_message(self):
        '''
        Creates a message to inform device of stopping the stimulus

        @rtype: Message
        @return: a stop message
        '''
        stop_message = \
            Message(MessageType.STOP,
                    None,
                    experiment_id=self.experiment_id,
                    stimulus_id=self.stimulus_id)
        return stop_message

    def terminate_message(self):
        '''
        Creates a message to inform device of terminating the program

        @rtype: Message
        @return: a terminate message
        '''
        terminate_message = \
            Message(MessageType.TERMINATE,
                    None)
        return terminate_message
