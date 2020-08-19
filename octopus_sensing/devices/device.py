from octopus_sensing.config import processing_unit

class Device(processing_unit):
    def __init__(self, name):
        super().__init__()
        self.device_name = None
        self.message_queue = None
        self.subject_id = None
        self.stimulus_id = None
        self.output_path = "output"

    def run(self):
        raise NotImplementedError()

    def set_queue(self, queue):
        '''
        Sets message queue for the device

        @param queue: a queue that will be used for message passing
        '''
        self.message_queue = queue
