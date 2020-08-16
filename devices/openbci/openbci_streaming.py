import threading
from config import processing_unit
import csv
import numpy as np

import pyOpenBCI
import datetime
#import multiprocessing

uVolts_per_count = (4500000)/24/(2**23-1)
accel_G_per_count = 0.002 / (2**4) #G/count

class OpenBCIStreaming(processing_unit):
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
        print("start eeg")
        threading.Thread(target=self._stream_loop).start()
        while(True):
            message = self._command_queue.get()
            if message is None:
                continue
            elif message.type == "trigger":
                print("Send trigger eeg", message)
                self._trigger = message.payload
            elif message.type == "terminate":
                self._backup_file.close()
                self._save_to_file()
                break
            else:
                continue

        self._board.stop_stream()

    def _stream_loop(self):
        self._board.start_stream(self._stream_callback)

    def _stream_callback(self, sample):
        data = np.array(sample.channels_data) * uVolts_per_count
        acc_data = np.array(sample.aux_data) * accel_G_per_count
        data_list = list(data) + list(acc_data)
        data_list.append(sample.id)
        data_list.append(str(datetime.datetime.now().time()))
        if self._trigger is not None:
            data_list.append(self._trigger)
            self._trigger = None
        self._stream_data.append(data_list)
        self._writer.writerow(data_list)

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
