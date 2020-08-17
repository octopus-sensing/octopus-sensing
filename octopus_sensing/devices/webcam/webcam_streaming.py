import time
import datetime
import cv2
import multiprocessing
import threading

from octopus_sensing.config import processing_unit


class WebcamStreaming(processing_unit):
    def __init__(self, file_queue, camera_no):
        super().__init__()
        self._file_queue = file_queue
        self._stream_data = []
        self._record = False
        self._file_path = None
        self._camera_no = camera_no

    def run(self):
        self._video_capture = cv2.VideoCapture(self._camera_no)
        self._fps = self._video_capture.get(cv2.CAP_PROP_FPS)
        print("fps ***********************", self._fps)
        threading.Thread(target=self._stream_loop).start()
        while True:
            message = self._file_queue.get()
            if message.type == "terminate":
                break
            elif message.type == "stop_record":
                self._record = False
                self._end = datetime.datetime.now()
                print("End video *************************", self._end)
                self._save_to_file()
            else:
                # Command is the file name
                print("start video")
                self._start = datetime.datetime.now()
                self._file_path = "created_files/videos/" + message.payload + '.avi'
                print(self._file_path)
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
        sec = (self._end-self._start).seconds
        fps = len(self._stream_data)/sec
        print("video recording")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self._file_path,
                              fourcc,
                              fps,
                              (640, 480))
        print(len(self._stream_data))
        for frame in self._stream_data:
            out.write(frame)
        out.release()


if __name__ == "__main__":
    queue = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()
    video1 = WebcamStreaming(queue, -1)
    video2 = WebcamStreaming(queue2, -1)
    video1.start()
    video2.start()
    time.sleep(7)
    queue.put("test_file")
    time.sleep(7)
    queue2.put("test_file2")
    time.sleep(6)
    queue.put("stop_record")
    queue2.put("stop_record")
    queue.put("terminate")
    queue2.put("terminate")
    video1.join()
    video2.join()
