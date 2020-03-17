import time
import cv2
from config import processing_unit
import multiprocessing
import threading

class VideoStreaming(processing_unit):
    def __init__(self, file_queue, camera_no):
        super().__init__()
        self._file_queue = file_queue
        self._stream_data = []
        self._record = False
        self._file_path = None
        self._camera_no = camera_no

    def run(self):
        self._video_capture = cv2.VideoCapture(self._camera_no)
        threading.Thread(target=self._stream_loop).start()
        while True:
            command = self._file_queue.get()
            if command == "terminate":
                break
            elif command == "stop_record":
                self._record = False
                self._save_to_file()
            else:
                # Command is the file name
                print("start video")
                print(command)
                self._file_path = "created_files/videos/" + command + '.avi'
                self._stream_data = []
                self._record = True
        self._video_capture.release()

    def _stream_loop(self):
        self._video_capture.read()
        try:
            while self._video_capture.isOpened:
                if self._record is False:
                    continue
                ret, frame = self._video_capture.read()
                if ret:
                    frame = cv2.flip(frame, 180)
                    self._stream_data.append(frame)

        except Exception as error:
            print(error)


    def _save_to_file(self):
        print("video recording")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self._file_path,
                              fourcc,
                              24.0,
                              (640,480))
        print(len(self._stream_data))
        for frame in self._stream_data:
            out.write(frame)
        out.release()

if __name__ == "__main__":
    queue = multiprocessing.Queue()
    video = VideoStreaming(queue, 5)
    video.start()
    time.sleep(7)
    queue.put("test_file")
    time.sleep(7)
    queue.put("terminate")
    video.join()
