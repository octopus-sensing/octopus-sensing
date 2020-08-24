# This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
# Copyright © Nastaran Saffaryazdi 2020
#
# Octopus Sensing is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
#  either version 3 of the License, or (at your option) any later version.
#
# Octopus Sensing is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Foobar.
# If not, see <https://www.gnu.org/licenses/>.

import os
import threading
import cv2
from octopus_sensing.devices.device import Device
from octopus_sensing.common.message_creators import MessageType


class WebcamStreaming(Device):
    def __init__(self, camera_no, **kwargs):
        super().__init__(**kwargs)
        self._stream_data = []
        self._record = False
        self.output_path = os.path.join(self.output_path, "video")
        os.makedirs(self.output_path, exist_ok=True)
        self._camera_number = camera_no
        self._video_capture = None
        self._fps = None

    def _run(self):
        self._video_capture = cv2.VideoCapture(self._camera_number)
        self._fps = self._video_capture.get(cv2.CAP_PROP_FPS)
        threading.Thread(target=self._stream_loop, daemon=True).start()
        while True:
            message = self.message_queue.get()
            print(message)
            if message is None:
                continue
            if message.type == MessageType.START:
                self._stream_data = []
                self._record = True
            elif message.type == MessageType.STOP:
                self._record = False
                file_name = \
                    "{0}/{1}-{2}-{3}.avi".format(self.output_path,
                                                 self.device_name,
                                                 message.experiment_id,
                                                 message.stimulus_id)
                self._save_to_file(file_name)
            elif message.type == MessageType.TERMINATE:
                break
        print("terminated")
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

    def _save_to_file(self, file_name):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(file_name,
                              fourcc,
                              self._fps,
                              (640, 480))
        print(len(self._stream_data))
        for frame in self._stream_data:
            out.write(frame)
        out.release()
