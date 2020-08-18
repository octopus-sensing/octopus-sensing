class Message():
    '''
    Message class
    '''
    def __init__(self, message_type, payload,
                 subject_id=None, stimulus_id=None):
        '''
        Initializes the message object

        @param str message_type: The type of message
        @param payload: the message data that can have differnt values

        @keyword str subject_id: subject's ID
        @keyword str stimulus_id: stimulus's ID
        '''
        self.message_type = message_type
        self.payload = payload
        self.subject_id = subject_id
        self.stimulus_id = stimulus_id
