# Octopus Sensing Tutorial
------------------------

## What Are We Building?

In this tutorial, we'll show how to design a simple scenario with octopus-sensing step by step.

The example scenario is the most common in emotion recognition research in affective computing. In this scenario, firstly, a stimulus like a video or an image is used to stimulate emotion in humans. Simultaneously, several sensors, including behavioral and physiological sensors, record data.  Finally, using a self-report questionnaire, the human feelings will be recorded. These steps could be repeated several times. Recording data from different sources synchronously and monitoring data for inspection detection in real-time and offline data visualization and processing are the main challenges of designing these scenarios.

#### By designing this scenario, we learn how to:

1. Use various kinds of stimuli in octopus-sensing.
2. Record data from various sources synchronously in python.
3. Being synchronized with other softwares like Matlab and unity.
4. Design self-report questionnaires.
5. Monitor and Visualize data in real-time.
6. Preprocess and visualize data offline.

## Adding sensors and synchronous data recording
The most important feature of octopus-sensing is synchronous data recording from different sensors. Octopus-sensing supports a set of sensors with a python library for data streaming. Also, it supports synchronous data recording using other software like Matlab and Unity. In this section, we learn how to record data from different sensors with internal or external drivers.

### Adding a sensor
Imagine starting data recording from the brain using OpenBCI EEG headset by pressing the "Enter" button and stopping recording after 5 seconds.

Firstly we should create an OpenBCI object with a specific name and an output path for recording data.

```python
my_openbci = OpenBCIStreaming(name="OpenBCI_sensor", output_path="./output")
```

Then we should add the created object to the DeviceManager's devices list. DeviceManager is responsible for managing devices like start recording, stop recording, triggering devices, and terminating them. When a device is added to the device coordinator, it will be initialized and prepared for data recording.

```python
device_coordinator = DeviceCoordinator()
device_coordinator.add_devices([my_openbci])
```

Now, we are developing a simple code to start data recording by pressing "Enter" button and stop recording after 5 seconds. 
```python
input("Press a button to start data recording")
device_coordinator.dispatch(start_message(experiment_id))
time.sleep(5)
device_coordinator.dispatch(stop_message(experiment_id))
device_coordinator.terminate()
```
Octopus-sensing provides a set of default messages for handling different actions like starting and stopping the recording or terminating the program. To identify recorded files, Octopus-sensing needs an experiment ID and stimulus ID Octopus-sensing experiment ID or stimulus ID. The experiment ID and stimulus ID are two strings and can be defined as you want. For example, we use the id of the recorded subject as experiment ID. Defining stimulus ID is essential to identify the recorded data related to each stimulus when we have different stimuli. The following block is the completed code for this example.

```python
from octopus_sensing.devices.openbci_streaming import OpenBCIStreaming
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.common.message_creators import start_message, stop_message

# Creating an instance of sensor
my_openbci = OpenBCIStreaming(name="OpenBCI_sensor", output_path="./output")

# Creating an instance of device coordinator
device_coordinator = DeviceCoordinator()

# Adding sensor to device coordinator
device_coordinator.add_devices([my_openbci])

experiment_id = "p01"
stimuli_id = "S00"

input("Press a button to start data recording")

# Starts data recording
device_coordinator.dispatch(start_message(experiment_id))
time.sleep(5)

# Stops deta recording
device_coordinator.dispatch(stop_message(experiment_id))

# Terminate, This step is necessary to close the connection with added devices
device_coordinator.terminate()
```

By running this code based on the saving_mode option that we considered when creating the sensor instance, the recorded file/s will be different. The default value of saving mode for OpenBCI is continuous. It means if we have several stimuli, all data will be recorded in one file. The name of the recorded file will be "OpenBCI_sensor-p01.csv" and will be saved in path "output/eeg". In this file, OpenBCI data samples have been recorded from when it initialized to when it received the terminate message. In the last column of data, identify the trigger column, which shows in what sample and time the device has received the start and stop triggers (pressing the button and 5 seconds after that). If we change the saving mode to separate (1), it will record one file for each stimulus (For this example, one file), and the name of stimuli will appear in the file name.

#### Troubleshooting
Keep in your mind, before running the code, connect the OpenBCI dongle to the system and turn on the openBci board. If after running the code, it raised an error that the OpenBCI port is busy, stop running, free up the port (sometimes reseting OpenBCI board or reattaching OpenBCI dongle) and then run the program again.

### Adding more sensors and synchronize data collection
To add each sensor, we should first create an instance and then add it to the device coordinator device list. The device coordinator will manage synchronous data recording by sending some markers to all devices in its device_list.

```python
device_coordinator.add_devices([my_openbci, my_shimmer, my_camera])
input("Press a button to start data recording")
device_coordinator.dispatch(start_message(experiment_id))
time.sleep(5)
device_coordinator.dispatch(stop_message(experiment_id))
device_coordinator.terminate()
```

We can have several cameras, an audio recorder, and several shimmer3 sensor and OpenBCI sensors. The following code shows how to add each of these devices.

#### Shimmer3 sensor
Shimmer3 works similar to OpenBCI with similar saving modes and extra column in data for triggers.
```python
from octopus_sensing.devices.shimmer3_streaming import Shimmer3Streaming
my_shimmer = Shimmer3Streaming(name="Shimmer_video", output_path=output_path)
```
#### Camera
The camera device only supports separated saving mode and will save a file for each stimulus. It will start recording when it receives the start trigger and save the file when it receives the stop command. The name of files will have the same pattern as OpenBCI files in separate saving_mode.
We can have several camera devices by identifying the camera number or the physical address of the camera in the system. For example, in the following code camera path has identified in Linux.

```python
from octopus_sensing.devices.camera_streaming import CameraStreaming
webcam_camera_path = "/dev/v4l/by-id/usb-046d_081b_97E6A7D0-video-index0"
my_camera = \
    CameraStreaming(name="camera",
                    camera_path = webcam_camera_path,
                    output_path=output_path)
```
#### Audio recorder
It works in only separaed saving mode. Only linux systems support audio recording.
```python
from octopus_sensing.devices.audio_streaming import AudioStreaming
audio_monitoring = AudioStreaming(name="Audio_monitoring", output_path=output_path)
```
