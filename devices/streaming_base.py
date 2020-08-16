import csv
import threading
from device import Device

class StreamingBase(Device):
    def __init__(self, message_queue, file_name):
        super().__init__()
        self._message_queue = message_queue
        self._file_name = file_name

    def run(self):
        threading.Thread(target=self._stream_loop).start()
        while(True):
            command = self._message_queue.get()
            if command is None:
                continue
            elif command == "terminate":
                self._save_to_file()
                break
            elif str(command).isdigit() is True:
                self._trigger = command
            else:
                continue

        self._board.stop_stream()

    def _stream_loop(self):
        '''
        Streaming
        '''
        raise NotImplementedError()

    def _save_to_file(self):
        with open(self._file_name, 'a') as csv_file:
            writer = csv.writer(csv_file)
            for row in self._stream_data:
                writer.writerow(row)
