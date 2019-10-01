import socket
import time
from config import processing_unit

HOST = '127.0.0.1'
PORT = 15361

# transform a value into an array of byte values in little-endian order.
class OpenVibeTrigge(processing_unit):
    def __init__(self, queue, event_id_queue):
        super().__init__()
        self._queue = queue
        self._event_id_queue = event_id_queue
        self._event_id = None
        # connect
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((HOST, PORT))

    def run(self):
        while(True):
            command = self._queue.get()
            if command == "start":
                print("trigger start")
                self._event_id = self._event_id_queue.get()
                self._set_event_id()
            elif command == "stop":
                self._set_event_id()
            elif command == "terminate":
                break
            else:
                continue
        print("terminate")
        self._socket.close()

    def _set_event_id(self):
        # create the three pieces of the tag, padding, event_id and timestamp
        padding=[0]*8

        # transform the value into an array of byte values in little-endian order
        event_id = list(self._event_id.to_bytes(8, byteorder='little'))
        print("trigger", self._event_id)

        # timestamp can be either the posix time in ms, or 0 to let the acquisition server timestamp the tag itself.
        t = int(time.time()*1000)
        timestamp = list(t.to_bytes(8, byteorder='little'))

        # send tag
        self._socket.sendall(bytearray(padding+event_id+timestamp))
