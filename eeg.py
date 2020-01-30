import threading
from config import processing_unit
import csv
import pyOpenBCI
import datetime
#import multiprocessing

class EEGStreaming(processing_unit):
    def __init__(self, file_name, command_queue):
        super().__init__()
        self._stream_data = []
        self._board = pyOpenBCI.OpenBCICyton(daisy=True)
        self._trigger = None
        self._command_queue = command_queue
        self._file_name = "created_files/eeg/" + file_name + '.csv'
        backup_file_name = "created_files/eeg/" + file_name + '-backup.csv'
        self._backup_file = open(backup_file_name, 'a')
        self._writer = csv.writer(self._backup_file)

    def run(self):
        threading.Thread(target=self._stream_loop).start()

        print("start eeg")
        threading.Thread(target=self._stream_loop).start()
        while(True):
            command = self._command_queue.get()
            if command is None:
                continue
            elif str(command).isdigit() is True:
                print("Send trigger eeg", command)
                self._trigger = command
            elif command == "terminate":
                self._backup_file.close()
                self._save_to_file()
                break
            else:
                continue

        self._board.stop_stream()

    def _stream_loop(self):
        self._board.start_stream(self._stream_callback)

    def _stream_callback(self, sample):
        sample.channels_data.append(str(datetime.datetime.now().time()))
        if self._trigger is not None:
            sample.channels_data.append(self._trigger)
            self._trigger = None
        self._stream_data.append(sample.channels_data)
        self._writer.writerow(sample.channels_data)

    def _save_to_file(self):
        print("save eeg")
        with open(self._file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for row in self._stream_data:
                writer.writerow(row)

#queue = multiprocessing.Queue()
#streaming = EEGStreaming("file_name", queue)
#streaming.start()
#import time
#time.sleep(2)
#queue.put("1234")
#print("***************************************")
#time.sleep(1)
#queue.put("terminate")
