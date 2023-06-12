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
# You should have received a copy of the GNU General Public License along with Octopus Sensing.
# If not, see <https://www.gnu.org/licenses/>.

from typing import Tuple, Any, Optional, Union
import os
import threading
import cv2
from octopus_sensing.devices.realtime_data_device import RealtimeDataDevice
from octopus_sensing.common.message_creators import MessageType
import time
from typing import Any, Dict

class CameraStreaming(RealtimeDataDevice):
    '''
    Stream and Record video data.
    If we have several stimuli, one vide file will be recorded for each stimuli.
    Device coordinator is responsible for triggerng the camera to start or stop recording.
    The content of recorded file is the recorded video between start and stop triggers

    Attributes
    ----------

    Parameters
    ----------
    name: str, default: None:
        The name of device

    output_path: str, default: output
                The path for recording files.
                Audio files will be recorded in folder {output_path}/{name}

    camera_no: int, default:0
        The camera number. Default is 0  which is defaul camera in system

    camera_path: str, default: None
        The physical path of camera device. It varies in different platforms.
        For Example in linux it can be something like this:
        `/dev/v4l/by-id/usb-046d_081b_97E6A7D0-video-index0`

    image_width: int, default: 1280
        The width of recorded frame/frames

    image_height: int, default: 720
        The height of recorded frame/frames.


    Notes
    -----
    - Only one of camera_no or camera_path should have value.

    - There is no guarantee that we can set the camera resolution.
      Because camera may not be able to support these resolution and it will change it
      based on its settings


    Example
    -----------
    Creating an instance of camera and adding it to the device coordinator.
    Device coordinator is responsible for triggerng the camera to start or stop recording

    >>> camera = CameraStreaming(camera_no=0,
    ...                          name="camera",
    ...                          output_path="./output")
    >>> device_coordinator.add_device(camera)

    See Also
    -----------
    :class:`octopus_sensing.device_coordinator`
    :class:`octopus_sensing.devices.device`
    :class:`octopus_sensing.devices.RealtimeDataDevice`

    '''
    def __init__(self, camera_no: Optional[Union[int, str]] = None,
                 camera_path: Optional[str] = None,
                 image_width: int = 1280,
                 image_height: int = 720,
                 **kwargs):
        assert (camera_no is not None) ^ (camera_path is not None), \
            "Only one of camera_no or camera_path should have value"
        super().__init__(**kwargs)
        self.output_path = os.path.join(self.output_path, self.name)
        os.makedirs(self.output_path, exist_ok=True)
        if camera_no is not None:
            self._camera_number = camera_no
        elif camera_path is not None:
            self._camera_number = os.path.realpath(camera_path)

        self._image_width = image_width
        self._image_height = image_height
        self._video_size: Tuple[int, int] = (self._image_width, self._image_height)
        self._video_capture: Any = None
        self._fps: int = 30
        self._capture_times: list = []
        self._frames: list = []
        self._counter = 0
        self._state = ""

    def _run(self):
        self._video_capture = cv2.VideoCapture(self._camera_number)
        try:
            self._video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self._image_width)
            self._video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self._image_height)
        except Exception as error:
            # Ignoring all errors
            print(f"[{self.name}] Could not set the camera resolution. Continuing.")
            print(error)

        # There's no guarantee that we can set the camera resolution. So, we
        # re-read the settings again from the camera.
        self._video_size = (int(self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                            int(self._video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self._video_capture.read()

        if self._video_size[0] <= 0 or self._video_size[1] <= 0:
            print(f"[{self.name}] Couldn't read the video size from the camera. Trying to terminate.")
            self._video_capture.release()
            raise RuntimeError(f"[{self.name}] Couldn't read the video size from the camera.")

        recording_thread = None
        recording_event = None

        print(f"[{self.name}] Initialized video device: video size: {self._video_size}")

        while True:
            message = self.message_queue.get()
            if message is None:
                continue
            if message.type == MessageType.START:
                print(f"[{self.name}] start camera")
                if self._state == "START":
                    print("Video streaming has already started")
                else:
                    self._frames = []
                    self._capture_times = []
                    if recording_thread is not None:
                        raise RuntimeError(
                            ("[{0} device] Received two start messages. "
                            "A STOP message should be send before trying "
                            "to start a new video recording.".format(self.name)))

                    file_name = "{0}/{1}-{2}-{3}.avi".format(self.output_path,
                                                            self.name,
                                                            message.experiment_id,
                                                            str(message.stimulus_id).zfill(2))
                    print(f"[{self.name}] Starting the recording thread")
                    recording_event = threading.Event()
                    recording_event.set()
                    recording_thread = threading.Thread(
                        target=self._stream_loop, args=(file_name, recording_event), daemon=True)
                    recording_thread.start()
                    self._state = "START"

            elif message.type == MessageType.STOP:
                if self._state == "STOP":
                    print(f"[{self.name}] Video streaming has already stopped")
                else:
                    if recording_event is not None:
                        recording_event.clear()
                    recording_thread = None
                    recording_event = None
                    self._state = "STOP"

            elif message.type == MessageType.TERMINATE:
                if recording_event is not None:
                    recording_event.clear()
                recording_thread = None
                recording_event = None
                break

        print(f"[{self.name}] video terminated")
        self._video_capture.release()

    def _stream_loop(self, file_name: str, event: threading.Event):
        print(f"[{self.name}] Start stream camera")
        codec = cv2.VideoWriter_fourcc(*'XVID')
        try:
            while self._video_capture.isOpened:
                if event.is_set():
                    ret, frame = self._video_capture.read()
                    if ret:
                        self._counter += 1
                        self._capture_times.append(time.time())
                        self._frames.append(frame)
                else:
                    fps = self._get_frame_rate()
                    print(f"[{self.name}] Recording frame per second", fps)
                    writer = cv2.VideoWriter(file_name,
                            codec,
                            fps,
                            self._video_size)
                    for frame in self._frames:
                        writer.write(frame)
                    writer.release()
                    break

        except Exception as error:
            print(f"[{self.name}] Error while recording video:")
            print(error)

    def _stream_loop_image(self, file_name: str, event: threading.Event):
        try:
            while self._video_capture.isOpened:
                if event.is_set():
                    ret, frame = self._video_capture.read()
                    if ret:
                        a = time.time()
                        os.makedirs(file_name[:-4], exist_ok=True)
                        image_file_name = file_name[:-4] + "/" + str(a) + ".jpg"
                        print(image_file_name)
                        cv2.imwrite(image_file_name, frame)
                else:
                    break

        except Exception as error:
            print(f"[{self.name}] Error while recording video.")
            print(error)

    def _get_realtime_data(self, duration: int) -> Dict[str, Any]:
        '''
        Returns n seconds (duration) of latest collected data for monitoring/visualizing or
        realtime processing purposes.

        Parameters
        ----------
        duration: int
            A time duration in seconds for getting the latest recorded data in realtime

        Returns
        -------
        data: Dict[str, Any]
            The keys are `data` and `metadata`.
            `data` is a list of records, or empty list if there's nothing.
            `metadata` is a dictionary of device metadata including `frame_rate` and `type`
        '''
        fps = self._get_frame_rate()

        data = self._frames[-1 * duration * fps:]
        metadata = {"frame_rate": fps,
                    "type": self.__class__.__name__}

        if len(data) == 0:
            realtime_data = {"data": [],
                             "metadata": metadata}
        else:
            one_frame_per_seconds = []
            for i in range(duration):
                if (i * fps) + 1 > len(data):
                    break
                one_frame_per_seconds.append(data[i * fps])

            realtime_data = {"data": one_frame_per_seconds,
                             "metadata": metadata}
        return realtime_data

    def _get_frame_rate(self):
        time_diff = 1
        i = 1
        while time_diff < 5 and len(self._capture_times) > i:
            time_diff = self._capture_times[-1] - self._capture_times[-(i+1)]
            i += 1
        fps = int(i/time_diff)

        return fps
