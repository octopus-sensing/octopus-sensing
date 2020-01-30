import socket
import time
from config import processing_unit

HOST = '127.0.0.1'
PORT = 15361
EMOTION_LIST = ["happy", "sad", "angry", "disgust", "surprise", "fear"]

# transform a value into an array of byte values in little-endian order.
class OpenVibeTrigger(processing_unit):
    def __init__(self, queue, event_id_queue):
        super().__init__()
        self._queue = queue
        self._event_id_queue = event_id_queue
        self._stimuli_id = None
        self._type_id = None
        self._state_id = None
        self._emotion_id = 0
        # connect
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((HOST, PORT))

    def run(self):
        while(True):
            command = self._queue.get()
            if command == "start_stimuli":
                print("trigger start")
                self._stimuli_id = self._event_id_queue.get()
                self._type_id = 1 # stimuli
                self._state_id = 1 # start
                self._set_event_id()
            elif command == "start_conversation":
                print("trigger conv start")
                self._type_id = 2 # conversation
                self._state_id = 1 # start
                self._set_event_id()
            elif command == "stop_stimuli":
                self._type_id = 1 # stimuli
                self._state_id = 2 # stop
                self._set_event_id()
            elif command == "stop_conversation":
                self._type_id = 2 # conversation
                self._state_id = 2 # stop
                self._set_event_id()
            elif command in EMOTION_LIST:
                self._emotion_id = EMOTION_LIST.index(command)+1
                self._set_event_id()
            elif command == "terminate":
                break
            else:
                continue
        self._socket.close()

    def _set_event_id(self):
        # create the three pieces of the tag, padding, event_id and timestamp
        padding=[0]*8
        # transform the value into an array of byte values in little-endian order

        event_id = self._type_id * 1000 + self._state_id * 100 + self._stimuli_id * 10 + self._emotion_id

        event_id = list(event_id.to_bytes(8, byteorder='little'))


        # timestamp can be either the posix time in ms, or 0 to let the acquisition server timestamp the tag itself.
        t = int(time.time()*1000)
        timestamp = list(t.to_bytes(8, byteorder='little'))

        # send tag
        print(padding+event_id+timestamp)
        print(bytearray(padding+event_id+timestamp))
        self._socket.sendall(bytearray(padding+event_id+timestamp))
