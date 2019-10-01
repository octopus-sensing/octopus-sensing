import threading
from config import processing_unit
import csv
import pyOpenBCI

class EEGStreaming(processing_unit):
    def __init__(self, file_queue):
        super().__init__()
        self._file_queue = file_queue
        self._stream_data = []
        self._board = pyOpenBCI.OpenBCICyton(daisy=True)
        self._record = None

    def run(self):
        threading.Thread(target=self._stream_loop).start()

        while True:
            command = self._file_queue.get()
            if command == "terminate":
                break
            elif command == "stop_record":
                self._save_to_file()
                self._record = False

            else:
                # Command is the file name
                self._file_path = "created_files/eeg/" + command + '.csv'
                print(self._file_path)
                self._stream_data = []
                self._record = True

        self._board.stop_stream()

    def _stream_loop(self):
        self._board.start_stream(self._stream_callback)

    def _stream_callback(self, sample):
        print(sample.channels_data)
        if self._record:
            self._stream_data.append(sample.channels_data)

    def _save_to_file(self):
        print("save eeg")
        print(len(self._stream_data))
        with open(self._file_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for row in self._stream_data:
                writer.writerow(row)
