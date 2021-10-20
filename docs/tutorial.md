# Octopus Sensing Tutorial
------------------------

## What Are We Building?

In this tutorial, we'll show how to design a simple scenario with octopus-sensing step by step.

The example scenario is the most common in emotion recognition research in affective computing. In this scenario, we learn how to record data from different sources synchronously when an event happen, and stop data recording by finishing the event. 

#### By designing these examples, we learn how to:

1. Use various kinds of stimuli in octopus-sensing.
2. Record data from various sources synchronously in python.
3. Being synchronized with other softwares like Matlab and unity.
4. Design self-report questionnaires.
5. Monitor and Visualize data in real-time.
6. Preprocess and visualize data offline.

## Prerequisites

Create a project and install `octopus-sensing` package by following the instructions on [Octopus Sensing Home Page](https://octopus-sensing.nastaran-saffar.me/). We recommend using `pipenv` to do so.

## Adding sensors and synchronous data recording
The most important feature of octopus-sensing is synchronous data recording from different sensors. Octopus-sensing supports a set of sensors with a python library for data streaming. Also, it supports synchronous data recording using other software like Matlab and Unity. In this section, we learn how to record data from different sensors with internal or external drivers.

### Adding a sensor
Imagine you want to record physiological data using shimmer3 sensor by pressing a key on keyboard and stop recording after 5 seconds.

Firstly we should create a Shimmer3Streaming object with a specific name and an output path for recording data.

```python
my_shimmer = Shimmer3Streaming(name="Shimmer3_sensor", output_path="./output")
```

Then we should add the created object to the `DeviceCoordinator`. As the name suggests, device coordinator is responsible for coordination, like start recording in all devices at once, stop recording, triggering (marking data at point), and terminating devices. When a device is added to the device coordinator, it will be initialized and prepared for data recording.

```python
device_coordinator = DeviceCoordinator()
device_coordinator.add_devices([my_shimmer])
```

Now, we are developing a simple code to start data recording by pressing a key and stop recording after 5 seconds.
```python
input("Press a key to start data recording")
device_coordinator.dispatch(start_message(experiment_id, stimuli_id))
time.sleep(5)
device_coordinator.dispatch(stop_message(experiment_id, stimuli_id))
device_coordinator.terminate()
```
Octopus-sensing provides a set of default messages for handling different actions like starting and stopping the recording or terminating the program. To identify recorded files, Octopus-sensing needs an experiment ID and stimulus ID. They are two strings and can be anything you want. For example, we use the id of the recorded subject as experiment ID. Defining stimulus ID is essential to identify the recorded data related to each stimulus when we have different stimuli.

The following block is the completed code for this example (examples/add_sensors.py).

```python
from octopus_sensing.devices.shimmer3_streaming import Shimmer3Streaming
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.common.message_creators import start_message, stop_message

# Creating an instance of sensor
my_shimmer = Shimmer3Streaming(name="Shimmer3_sensor", output_path="./output")

# Creating an instance of device coordinator
device_coordinator = DeviceCoordinator()

# Adding sensor to device coordinator
device_coordinator.add_devices([my_shimmer])

experiment_id = "p01"
stimuli_id = "S00"

input("Press a button to start data recording")

# Starts data recording
device_coordinator.dispatch(start_message(experiment_id, stimuli_id))
time.sleep(5)

# Stops deta recording
device_coordinator.dispatch(stop_message(experiment_id, stimuli_id))

# Terminate, This step is necessary to close the connection with added devices
device_coordinator.terminate()
```

By running this code based on the `saving_mode` option that we passed when creating the sensor instance, the recorded file/s will be different. The default value of saving mode for Shimmer3 is continuous. It means if we have several stimuli, all data will be recorded in one file. The name of the recorded file will be `Shimmer3_sensor-{experiment_id}.csv` and will be saved in `output/eeg` path. In this file, Shimmer3 data samples have been recorded from when it initialized to when it received the terminate message. The last column of data is the trigger column, which shows in what sample and time the device has received the start and stop triggers (pressing the button and 5 seconds after that). If we change the saving mode to separate (`SavingModeEnum.SEPARATED_SAVING_MODE`), it will record one file for each stimulus (For this example, one file), and the name of stimuli will appear in the file name.

#### Troubleshooting
Keep in your mind, before running the code, turn on the Shimmer3 sensor and pair bluetooth and the serial port. (Shimmer password: 1234)

For example in linux you can do it as follow:
1- hcitool scan   //It shows the macaddress of device. for shimmer it is 00:06:66:F0:95:95

2- vim /etc/bluetooth/rfcomm.conf write the below line in it: 
rfcomm0{ bind no; device 00:06:66:F0:95:95; channel 1; comment "serial port" } 

3- sudo rfcomm connect rfcomm0 00:06:66:F0:95:95 // This is for reading bluetooth data from a serial port

### Adding more sensors and synchronize data collection
To add each sensor, we should first create an instance and then add it to the device coordinator device list. The device coordinator will manage synchronous data recording by sending some markers to all devices in its device_list.

```python
device_coordinator.add_devices([my_openbci, my_shimmer, my_camera])
input("Press a button to start data recording")
device_coordinator.dispatch(start_message(experiment_id, stimuli_id))
time.sleep(5)
device_coordinator.dispatch(stop_message(experiment_id, stimuli_id))
device_coordinator.terminate()
```

We can have several cameras, an audio recorder, and several Shimmer3 sensor and OpenBCI sensors. To learn more about available sensors, see [Devices](https://octopus-sensing.nastaran-saffar.me/devices).

### Displaying some images consequently as stimuli and data recording
In this example, we learn how to record data in parallel with displaying image stimuli.

To display image stimuli, Octopus-Sensing provides a set of predefined stimuli, inclusing video and image. To display image stimuli, we used GTK. We should path the path of image stimulus and the display time to Octopus-sensing to display the saved image in the specified path for the specified time.

```python
from octopus_sensing.windows.image_window import show_image_standalone
show_image_standalone(os.path.join(stimuli_path, stmulus_name), display_time)
```

The following code is the complete example of recording physiological data using Shimmer3 sensor while a set of images are displaying.(examples/simple_scenario.py)

```python
import time
import os
from octopus_sensing.devices.shimmer3_streaming import Shimmer3Streaming
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.common.message_creators import start_message, stop_message
from octopus_sensing.windows.image_window import show_image_standalone


def simple_scenario(stimuli_path):
    # Reading image stimuli and assigning an ID to them based on their alphabetical order
    stimuli_list = os.listdir(stimuli_path)
    stimuli_list.sort()
    stimuli = {}
    i = 0
    for item in stimuli_list:
        stimuli[i] = item
        i += 1

    # The time for displaying each image stimulus
    display_time = 5

    print("initializing")
    # Creating an instance of sensor
    my_shimmer = Shimmer3Streaming(name="Shimmer3_sensor",
                                   output_path="./output")

    # Creating an instance of device coordinator
    device_coordinator = DeviceCoordinator()

    # Adding sensor to device coordinator
    device_coordinator.add_devices([my_shimmer])

    experiment_id = "p01"

    # A delay to be sure initialing devices have finished
    time.delay(3)

    input("\nPress a key to run the scenario")

    for stimuli_id, stmulus_name in stimuli.items():
        # Starts data recording by displaying the image
        device_coordinator.dispatch(start_message(experiment_id, stimuli_id))

        # Displaying an image may start with some milliseconds delay after data recording because of GTK       initialization in show_image_standalone. If this delay is important to you, use other tools for displaying image stimuli
        show_image_standalone(os.path.join(stimuli_path, stmulus_name), display_time)

        # Stops data recording by closing image
        device_coordinator.dispatch(stop_message(experiment_id, stimuli_id))
        input("\nPress a key to continue")

    # Terminate, This step is necessary to close the connection with added devices
    device_coordinator.terminate()
```

Since the default saving mode is continuous, Shimmer3 will record all data in one file. For each stimulus, it records two trigger with stimuli ID in the file, one for start and one for the end of displaying stimulus.

### Preparing data for processing
If you used continuous `saving_mode` and want to split them into several files for processing, Octopus-Sensing provides this feature by adding only one line to the end of the previous example.

```python
from octopus_sensing.preprocessing.preprocess_devices import preprocess_devices
preprocess_devices(device_coordinator,
                   output_path,
                   shimmer3_sampling_rate=128,
                   signal_preprocess=True):
```

By passing the `DeviceCoordinator` instance to preprocess_devices, it will apply preprocessing on all added devices that implemented preprocessing. For audio and video, we don't need any general preparation. But, for OpenBCI and Shimmer3 sensor, it will apply three or two steps according to the passed parameters. It will resample the recorded data for Shimmer3 in this example to a sampling rate 128 Hz. Then it will split data based on start and stop triggers. Then, since `signal_preprocess` is True, it will apply bandpass filtering and cleaning noises. Finally, this data will be recorded in the specified output path and ready to be used for analysis.
