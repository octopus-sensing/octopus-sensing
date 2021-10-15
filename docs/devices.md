
#### Shimmer3 sensor
Shimmer3 works similar to OpenBCI with similar saving modes and extra column in data for triggers.
```python
from octopus_sensing.devices.shimmer3_streaming import Shimmer3Streaming
my_shimmer = Shimmer3Streaming(name="Shimmer_video", output_path=output_path)
```
#### Camera
The camera device only supports separated saving mode and will save a file for each stimulus. It will start recording when it receives the start trigger and save the file when it receives the stop command. The name of files will have the same pattern as OpenBCI files in separate saving_mode.
We can have several camera devices by identifying the camera number or the physical address of the camera in the system. For example, in the following code camera path is the device path in Linux.

```python
from octopus_sensing.devices.camera_streaming import CameraStreaming
webcam_camera_path = "/dev/v4l/by-id/usb-046d_081b_97E6A7D0-video-index0"
my_camera = \
    CameraStreaming(name="camera",
                    camera_path = webcam_camera_path,
                    output_path=output_path)
```
#### Audio recorder
It works in only separaed saving mode. Audio recording is not supported in Windows.
```python
from octopus_sensing.devices.audio_streaming import AudioStreaming
audio_monitoring = AudioStreaming(name="Audio_monitoring", output_path=output_path)
```
