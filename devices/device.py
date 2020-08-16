from config import processing_unit

class Device(processing_unit):
    def __init__(self, message_queue):
        super().__init__()
        self._message_queue = message_queue

    def run(self):
        raise NotImplementedError()
