.. _tutorial:

*************
Tutorial
*************


What Are We Building?
----------------------

In this tutorial, we'll show how to design a simple scenario with octopus-sensing step by step.

The example scenario is the most common in emotion recognition research in affective computing. In this scenario, we learn how to record data from different sources synchronously when an event happens and stop data recording by finishing the event. 

**By designing these examples, we learn how to:**

    1. Record data from various sources synchronously.
    2. Being synchronized with other software like Matlab and unity.
    3. Use various kinds of stimuli in octopus-sensing.
    4. Providing some utilities for designing experiments. 
    5. Monitor and data in real-time.
    6. Preprocess and visualize data offline.
    7. How to add new devices to Octopus Sensing

**Prerequisites**

Create a project and install `octopus-sensing` package by following the instructions on :ref:`quick_start`. We recommend using `pipenv` to do so.

1- Record data from various sources synchronously
-------------------------------------------------
The most crucial feature of octopus-sensing is synchronous data recording from different sensors.
Octopus-sensing supports a set of sensors with a python library for data streaming. 
Also, it supports synchronous data recording using other software like Matlab and Unity.
In this section, we learn how to record data from different sensors with internal drivers.
(devices with a python driver for data acquisition).

Adding a sensor
""""""""""""""""
Imagine you want to record physiological data using shimmer3 sensor by pressing a key on the keyboard
and stop recording after 5 seconds.

Firstly we should create a Shimmer3Streaming object with a specific name and an output path for recording data.

>>> my_shimmer = Shimmer3Streaming(name="shimmer",
...                                saving_mode=SavingModeEnum.CONTINIOUS_SAVING_MODE,
...                                output_path="./output")

Then we should add the created object to the `DeviceCoordinator`.  As the name suggests, the device coordinator is responsible for coordination, like starting to record data in all devices at once, stopping data recording, triggering (marking data at a point), and terminating devices. When a device is added to the device coordinator, it will be initialized and prepared for recording.

>>> device_coordinator = DeviceCoordinator()
>>> device_coordinator.add_devices([my_shimmer])

We are now developing a simple code to start data recording by pressing a key and stopping recording after 5 seconds.

>>> input("Press a key to start data recording")
>>> device_coordinator.dispatch(start_message(experiment_id, stimuli_id))
>>> time.sleep(5)
>>> device_coordinator.dispatch(stop_message(experiment_id, stimuli_id))
>>> device_coordinator.terminate()

Octopus-sensing provides a set of default messages for handling different actions like 
starting and stopping the recording or terminating the program. 
To identify recorded files, Octopus-sensing needs an experiment ID and stimulus ID.
They are two strings and can be anything you want.
For example, we use the id of the recorded subject as experiment ID. 
Defining stimulus ID is essential for identifying the recorded data related to each stimulus
when we have different stimuli.

To see the completed example see (octopus_sensing/examples/add_sensors.py).
By running this example, according to the `saving_mode` option that we passed when creating the sensor instance,
the recorded file/s will be different. The default value of saving mode for Shimmer3 is continuous.
It means if we have several stimuli, all data will be recorded in one file.
The name of the recorded file will be `shimmer-{experiment_id}.csv` and will be saved in `output/shimmer` path. In this file, Shimmer3 data samples have been recorded from when it initialized to when it received the terminate message. The last column of data is the trigger column, which shows in what sample and time the device has received the start and stop triggers (pressing the button and 5 seconds after that). If we change the saving mode to separate (`SavingModeEnum.SEPARATED_SAVING_MODE`), it will record one file for each stimulus (For this example, one file), and the name of stimuli will appear in the file name.

**Troubleshooting**

Keep in your mind, before running the code, turn on the Shimmer3 sensor and pair Bluetooth and the serial port.
(Shimmer password: 1234)

For example, in Linux you can do it as follow:
    1. hcitool scan   //It shows the mac-address of the device. for shimmer it is 00:06:66:F0:95:95
    2. vim /etc/bluetooth/rfcomm.conf write the below line in it: rfcomm0{ bind no; device 00:06:66:F0:95:95; channel 1; comment "serial port" } 
    3. sudo rfcomm connect rfcomm0 00:06:66:F0:95:95 // This is for reading bluetooth data from a serial port

Adding several sensors
""""""""""""""""""""""

To add each sensor, we should first create an instance of it and then add it to the device coordinator device list.
The device coordinator will manage synchronous data recording by sending some markers to all devices in its device_list.

>>> my_shimmer = Shimmer3Streaming(name="shimmer",
...                                saving_mode=SavingModeEnum.CONTINIOUS_SAVING_MODE,
...                                output_path="./output")
>>> my_camera = CameraStreaming(camera_no=0,
...                             name="camera",
...                             output_path="./output")
>>> my_openbci =
...     BrainFlowOpenBCIStreaming(name="OpenBCI",
...                               output_path="./output",
...                               board_type="cyton-daisy",
...                               saving_mode=SavingModeEnum.CONTINIOUS_SAVING_MODE,
...                               channels_order=["Fp1", "Fp2", "F7", "F3", 
...                                               "F4", "F8", "T3", "C3",
...                                               "C4", "T4", "T5", "P3", 
...                                               "P4", "T6", "O1", "O2"])
>>> device_coordinator.add_device(my_shimmer)
>>> device_coordinator.add_devices([my_openbci, my_shimmer, my_camera])
>>> input("Press a button to start data recording")
>>> device_coordinator.dispatch(start_message(experiment_id, stimuli_id))
>>> time.sleep(5)
>>> device_coordinator.dispatch(stop_message(experiment_id, stimuli_id))
>>> device_coordinator.terminate()

Octopus Sensing can simultaneously record data from several cameras, an audio recorder, and several Shimmer3 OpenBCI sensors.
To learn more about supported sensors, see :ref:`devices`.

2- Synchronization with other software
---------------------------------------
Octopus Sensing also can send synchronization markers to external devices which record data through other 
software like `Matlab <https://au.mathworks.com/products/matlab.html>`_. 

First, we should create an instance of `SocketNetworkDevice` and allocate an IP address and port.
Then add it to the `DeviceCoordinator` like other devices. By adding it to the `DeviceCoordinator`, it will start
listening on specified IP address and port.

>>> from octopus_sensing.devices.socket_device import SocketNetworkDevice
>>> socket_device = SocketNetworkDevice("0.0.0.0", 5002)
>>> device_coordinator.add_devices([socket_device])

Then a client can connect to this server to receive triggers. In the following code, we created a simple scenario 
that sends several triggers to a simple data recorder in Matlab.

**Server Code in python**

By running the server code, it starts listening. Before to begin sending markers, make sure
that client code is running, and it has connected to the server. 
See the complete example in octopus_sensing.examples.send_trigger_to_remote_device.py

>>> device_coordinator = DeviceCoordinator()
>>> socket_device = SocketNetworkDevice("0.0.0.0", 5002)
>>> device_coordinator.add_devices([socket_device])
>>> time.sleep(2)
>>> input("If a client has connected successfully, press enter to start sending marker")
>>> message = start_message("test", "00")
>>> device_coordinator.dispatch(message)
>>> time.sleep(2)
>>> message = stop_message("test", "00")
>>> device_coordinator.dispatch(message)
>>> time.sleep(2)
>>> message = start_message("test", "01")
>>> device_coordinator.dispatch(message)
>>> time.sleep(2)
>>> message = stop_message("test", "01")
>>> device_coordinator.dispatch(message)
>>> time.sleep(3)
>>> device_coordinator.terminate()

**Client Code in Matlab**

We created a simple data recorder in this example which, in parallel, listens to the network. 
By running matlabRecorder in Matlab, firstly, it tries to connect to the specified server. 
Then it starts listening to specified port asynchronously. Parallel to this, it is recording some numbers in a file.
As soon as it receives a marker, it will add it to the recorded line in the file.
See this example in octopus_sensing.examples.matlabRecorder.m


>>> function matlabRecorder()
>>>     global marker
>>>     marker = "";
>>>     tcpipClient = tcpip('localhost',5002,'NetworkRole','Client');
>>>     tcpipClient.ReadAsyncMode = 'continuous';
>>>     tcpipClient.Terminator = 10;
>>>     tcpipClient.BytesAvailableFcn = @setMarker;
>>>     tcpipClient.BytesAvailableFcnMode = 'terminator';
>>>     fopen(tcpipClient);
>>>     file_out = fopen("file_out.csv", 'w');
>>>     i = double(0);
>>>     while(1)
>>>         if marker == "terminate"
>>>             break
>>>         elseif marker == ""
>>>             fprintf(file_out, "%d, %s\n", i, "");
>>>         else
>>>             fprintf(file_out, "%d,%s\n", i, marker);
>>>             marker = "";
>>>         end
>>>         i =  i + 1;
>>>         pause(0.1);
>>>     end
>>>     fclose(file_out);
>>>     fclose(tcpipClient)
>>>    
>>> end
>>>
>>> function setMarker(obj, event)
>>>     global marker;
>>>     data = fscanf(obj);
>>>     marker = erase(data, char(10));
>>> end


3- Use various kinds of stimuli in octopus-sensing
--------------------------------------------------
In this example, we learn how to record data in parallel with displaying image stimuli.

To display stimuli, Octopus-Sensing provides a set of predefined stimuli, including video and image.
To display image stimuli, we used GTK. We should specify the path of the image stimulus and the duration time
for displaying it.

>>> from octopus_sensing.stimuli import ImageStimulus
>>> stimulus = ImageStimulus(stimuli_id, os.path.join(stimuli_path, stmulus_name), 5)
>>> stimulus.show_standalone()

Similarly we can create an video stimulus. Octopus Sensing uses 
`VLC media player <https://www.videolan.org/vlc/>`_ to display video stimuli. 
You should have VLC installed on your system.

>>> from octopus_sensing.stimuli import VideoStimulus
>>> stimulus = VideoStimulus(stimuli_id, os.path.join(stimuli_path, stmulus_name))
>>> stimulus.show()

The following code is the complete example of recording physiological data using Shimmer3
sensor while a set of images are displaying. See `octopus_sensing/examples/simple_scenario.py`. 
In this example you can have video stimuli with uncommenting video stimuli lines and commenting image stimuli lines.

>>> import time
>>> import os
>>> from octopus_sensing.devices import Shimmer3Streaming
>>> from oc>>> topus_sensing.device_coordinator import DeviceCoordinator
>>> from octopus_sensing.common.message_creators import start_message, stop_message
>>> from octopus_sensing.stimuli import ImageStimulus
>>> 
>>> 
>>> def simple_scenario(stimuli_path):
>>>     # Reading image stimuli and assigning an ID to them based on their alphabetical order
>>>     stimuli_list = os.listdir(stimuli_path)
>>>     stimuli_list.sort()
>>>     stimuli = {}
>>>     i = 0
>>>     for item in stimuli_list:
>>>         stimuli[i] = item
>>>         i += 1
>>> 
>>>     print("initializing")
>>>     # Creating an instance of sensor
>>>     my_shimmer = Shimmer3Streaming(name="Shimmer3_sensor",
>>>                                    output_path="./output")
>>> 
>>>     # Creating an instance of device coordinator
>>>     device_coordinator = DeviceCoordinator()
>>> 
>>>     # Adding sensor to device coordinator
>>>     device_coordinator.add_devices([my_shimmer])
>>> 
>>>     experiment_id = "p01"
>>> 
>>>     # A delay to be sure initialing devices have finished
>>>     time.delay(3)
>>> 
>>>     input("\nPress a key to run the scenario")
>>> 
>>>     for stimuli_id, stmulus_name in stimuli.items():
>>>         # Starts data recording by displaying the image
>>>         device_coordinator.dispatch(start_message(experiment_id, stimuli_id))
>>> 
>>>         # Displaying an image may start with some milliseconds delay after data recording because of GTK       initialization in show_image_standalone. If this delay is important to you, use other tools for displaying image stimuli
>>>         stimulus = ImageStimulus(stimuli_id, os.path.join(stimuli_path, stmulus_name), 5)
>>>         stimulus.show_standalone()
>>> 
>>>         # Stops data recording by closing image
>>>         device_coordinator.dispatch(stop_message(experiment_id, stimuli_id))
>>>         input("\nPress a key to continue")
>>> 
>>>     # Terminate, This step is necessary to close the connection with added devices
>>>     device_coordinator.terminate()


Since the default saving mode is continuous, Shimmer3 will record all data in one file.
For each stimulus, the device records two triggers in the file, one for the start of stimulus and one for the end of the stimulus. 


4- Utilities for designing experiments
--------------------------------------

5- Monitoring
--------------
See :ref:`octopus_sensing_monitoring` to know more about monitoring and how to use it.

6- Preprocess and visualize data offline
----------------------------------------

If you used continuous `saving_mode` and want to split them into several files for processing,
Octopus Sensing provides this feature by adding only one line to the end of the previous example.

>>> from octopus_sensing.preprocessing.preprocess_devices import preprocess_devices
>>> preprocess_devices(device_coordinator,
...                    output_path,
...                    shimmer3_sampling_rate=128,
...                    signal_preprocess=True):

By passing the instance of `DeviceCoordinator` as a parameter to `preprocess_devices` function,
it will apply preprocessing step on all added devices that implemented preprocessing. 
For audio and video, we don't need any general preparation. 
But, the OpenBCI and Shimmer3 sensor will apply three or two preprocessing steps according to the passed parameters. 
It will resample the recorded data for Shimmer3 in this example to a sampling rate of 128 Hz.
Then it will split data based on start and stop triggers. 
Then, since `signal_preprocess` is True, it will apply bandpass filtering and cleaning noises.
Finally, this data will be recorded in the specified output path and ready to be used for analysis.

See :ref:`octopus_sensing_visualizer` to know more about visualizer and how to use it.
