import socket
import time
from config import processing_unit

HOST = '127.0.0.1'
PORT = 15361

# transform a value into an array of byte values in little-endian order.
class OpenVibeTrigger(processing_unit):
    def __init__(self, queue):
        super().__init__()
        self._queue = queue
        # connect
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((HOST, PORT))

    def run(self):
        print("start EEG")
        while(True):
            command = self._queue.get()
            if command is None:
                continue
            elif str(command).isdigit() is True:
                print("Send trigger")
                self._send_trigger(command)
            elif command == "terminate":
                break
            else:
                continue
        self._socket.close()

    def _send_trigger(self, event_id):
        # create the three pieces of the tag, padding, event_id and timestamp
        padding=[0]*8

        # transform the value into an array of byte values in little-endian order
        event_id = list(event_id.to_bytes(8, byteorder='little'))

        # timestamp can be either the posix time in ms, or 0 to let the acquisition server timestamp the tag itself.
        t = int(time.time()*1000)
        timestamp = list(t.to_bytes(8, byteorder='little'))

        self._socket.sendall(bytearray(padding+event_id+timestamp))
