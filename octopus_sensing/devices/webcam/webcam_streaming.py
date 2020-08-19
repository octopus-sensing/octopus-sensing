import datetime
import threading
import cv2


from octopus_sensing.devices.device import Device


class WebcamStreaming(Device):
    def __init__(self, camera_no):
        super().__init__()
        self._stream_data = []
        self._record = False
        self._camera_no = camera_no

    def run(self):
        self._video_capture = cv2.VideoCapture(self._camera_no)
        self._fps = self._video_capture.get(cv2.CAP_PROP_FPS)
        print("fps ***********************", self._fps)
        threading.Thread(target=self._stream_loop).start()
        while True:
            message = self.message_queue.get()
            if message is not None:
                self.subject_id = message.subject_id
                self.stimulus_id = message.stimulus_id
            if message.type == "terminate":
                break
            elif message.type == "stop_record":
                self._record = False
                self._end = datetime.datetime.now()
                print("End video *************************", self._end)
                self._save_to_file()
            else:
                # Command is the file name
                self._start = datetime.datetime.now()
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
        file_name = \
            "{0}/video/{1}-{2}-{3}.avi".format(self.output_path,
                                               self.device_name,
                                               self.subject_id,
                                               self.stimulus_id)
        sec = (self._end-self._start).seconds
        fps = len(self._stream_data)/sec
        print("video recording")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(file_name,
                              fourcc,
                              fps,
                              (640, 480))
        print(len(self._stream_data))
        for frame in self._stream_data:
            out.write(frame)
        out.release()
