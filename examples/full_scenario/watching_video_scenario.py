'''
Copy full_scenario directory in your system.
cd full_scenario
Install `octopus-sensing` package using `pipenv`.
Install `octopus-sensing-monitorng' using `pipenv` if you like to monitor data
Install `octopus-sensing-visualizer` using `pipenv` if you like to visualize data
Copy some short videos as stimuli in the stimuli directory inside the full_scenario directory
Run `pipenv run python watching_video_scenario.py`
Run `pipenv run octopus-sensing-monitoring` in current directory in another terminal and monitor data on browser
After finishing the scenario, run `pipenv run octopus-sensing-visualizer` and visualize data on browser. 
You can config the `octopus_sensing_visualizer_config.conf` file in your project directory.

'''


import argparse
from screeninfo import get_monitors
from gi.repository import Gtk, GdkPixbuf, GLib
import os
import time
import datetime
import sys  # nopep8
sys.path.insert(0, "../../octopus-sensing")  # nopep8

from stimuli_loader import load_stimuli
from questionnaires import get_video_questionnaire
from octopus_sensing.windows.image_window import ImageWindow
from octopus_sensing.common.message_creators import start_message, stop_message
from octopus_sensing.devices import CameraStreaming
from octopus_sensing.devices import BrainFlowOpenBCIStreaming
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.devices.network_devices.socket_device import SocketNetworkDevice
from octopus_sensing.preprocessing.preprocess_devices import preprocess_devices
from octopus_sensing.monitoring_endpoint import MonitoringEndpoint
import logging
import gi
gi.require_version('Gtk', '3.0')


stimuli_path = 'stimuli'
FIXATION_CROSS_SHOW_TIME = 3
GAP_TIME = 2


class MainWindow(Gtk.Window):
    def __init__(self, experiment_id: str, stimuli_list: list,
                 device_coordinator: DeviceCoordinator,
                 output_path: str="output"):
        time_str = datetime.datetime.strftime(datetime.datetime.now(),
                                              "%Y-%m-%dT%H-%M-%S")
        logging.basicConfig(filename='logs/watching_video_log_{0}_{1}.log'.format(experiment_id, time_str),
                            level=logging.DEBUG)
        self._device_coordinator = device_coordinator
        self._stimuli_list = stimuli_list
        self._stimuli_index = 0
        self._experiment_id = experiment_id

        Gtk.Window.__init__(self, title="")
        image_box = Gtk.Box()
        monitors = get_monitors()
        image_width = monitors[0].width
        image_height = monitors[0].height
        background_path = "images/gray_image.jpg"
        pixbuf = \
            GdkPixbuf.Pixbuf.new_from_file_at_scale(background_path,
                                                    image_width,
                                                    image_height, False)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        image_box.pack_start(image, False, False, 0)
        self.add(image_box)
        self._output_path = output_path

    def show(self):
        '''
        Shows the background window (A gray image)
        '''
        logging.info("Start time {0}".format(datetime.datetime.now()))

        self.connect("destroy", Gtk.main_quit)
        self.fullscreen()
        self.show_all()

        GLib.timeout_add_seconds(5, self._show_fixation_cross)
        Gtk.main()

    def _show_fixation_cross(self, *args):
        '''
        Showing fixation cross before each stimuli
        We start data recording here to later consider these three seconds as baseline data
        '''
        logging.info("images/Fixation cross {0}".format(datetime.datetime.now()))
        fixation_cross = \
            ImageWindow("images/fixation_cross.jpg", FIXATION_CROSS_SHOW_TIME)
        stimulus = self._stimuli_list[self._stimuli_index]
        self._device_coordinator.dispatch(start_message(self._experiment_id,
                                                        stimulus.id))
        fixation_cross.show_window()
        fixation_cross.connect("destroy", self._show_stimuli)

    def _show_stimuli(self, *args):
        '''
        Showing stimuli.
        '''
        logging.info("Stimuli start {0}".format(datetime.datetime.now()))
        stimulus = self._stimuli_list[self._stimuli_index]
        stimulus.show()
        self._device_coordinator.dispatch(stop_message(self._experiment_id,
                                                       stimulus.id))

        GLib.timeout_add_seconds(0, self._show_questionnaire)

    def _show_questionnaire(self, *args):
        '''
        Showing a questionnaire after each stimulus t record self-report data
        '''
        logging.info("Questionnaire start {0}".format(datetime.datetime.now()))
        questionnaire = \
            get_video_questionnaire("self-report",
                                    self._experiment_id,
                                    self._stimuli_list[self._stimuli_index].id,
                                    "Questionnaire",
                                    output_path=self._output_path)
        questionnaire.show()
        questionnaire.connect("destroy", self._relaxation)

    def _relaxation(self, *args):
        '''
        Create a small delay between two round
        '''
        GLib.timeout_add_seconds(GAP_TIME, self._show_next)

    def _show_next(self, *args):
        '''
        Checks for the next step, repeating the process or finishing the scenario
        '''
        self._stimuli_index += 1
        if self._stimuli_index >= len(self._stimuli_list):
            self._done()
        else:
            self._show_fixation_cross()

    def _done(self, *args):
        '''
        Terminating the device coordinator and displaying `Done` window
        '''
        logging.info("End time {0}".format(datetime.datetime.now()))
        self._device_coordinator.terminate()
        done_window = \
            ImageWindow("images/done_image.jpg", 2)
        done_window.show_window()
        done_window.connect("destroy", self._terminate)

    def _terminate(self, *args):
        '''
        Destroys the main Gtk window
        '''
        self.destroy()


def get_input_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subject_id", help="The subject ID", default=0)
    args = parser.parse_args()
    subject_id = args.subject_id
    return subject_id


def main(): 
    '''
    Scenario starts by 
    1- Initialization and displaying a gray screen (Put the cursor on each monitor that 
       you want to the scenario is being displayed)
    2- Displaying a fixation cross for 3 seconds
    3- Displaying a video stimulus and start to record data
    4- Displaying a questionnaire
    5- By answering the questionnaire and closing it, the same process repeat from the step 2.
       It will be repeated for the number of video stimulus in the stimuli directory
    
    Run the code like `pipenv run python watching_video_scenario.py -s 1`
    By running this command it will consider `1` as the subject number and will record data in `p01` directory
    '''  

    subject_id = get_input_parameters()
    experiment_id = str(subject_id).zfill(2)
    output_path = "output/p{0}".format(experiment_id)
    os.makedirs(output_path, exist_ok=True)


    # Create and instance of video device
    camera = \
        CameraStreaming(name="webcam",
                        output_path=output_path,
                        camera_no=0,
                        image_width=640,
                        image_height=360)

    # Create an instance of OpenBCI device
    openbci = BrainFlowOpenBCIStreaming(name="eeg", output_path=output_path, serial_port="/dev/ttyUSB2",
                                        channels_order=["Fp1", "Fp2", "F7", "F3", "F4", "F8", "T3", "C3",
                                                        "C4", "T4", "T5", "P3", "P4", "T6", "O1", "O2"])

    # Create Network device if you want to send triggers to other software and add it to device_coordinator
    #socket_device = SocketNetworkDevice("localhost", 5006)

    # Add to device coordinator for synchronous data recording
    device_coordinator = DeviceCoordinator()
    device_coordinator.add_devices([openbci, camera])

    stimuli_list = load_stimuli(stimuli_path)
    # Make delay for initializing all processes
    print("Initializing")
    time.sleep(5)

    # Creating the main Gtk window 
    main_window = \
        MainWindow(experiment_id,
                   stimuli_list,
                   device_coordinator,
                   output_path=output_path)
    
    # After running this code, Run `pipenv run octopus-sensing-monitoring` in another terminal
    # and then monitor data on browser.
    # (Make sure to install octopus-sensing-monitoring if you want to monitor data in real time)
    monitoring_endpoint = MonitoringEndpoint(device_coordinator)
    monitoring_endpoint.start()

    try:
        # Start the scenario
        main_window.show()
        monitoring_endpoint.stop()

        # After running this code, data will be prepared in preprocessed_output path
        # By configging octopus_sensing_visualizer_config.conf in your project derectory and
        # running `pipenv run octopus-sensing-visualizer` you can visualize data on browser after finishing
        # the data collection (Make sure to install octopus-sensing-visualizer if you want to visualize data)
        preprocess_devices(device_coordinator,
                           "preprocessed_output",
                           openbci_sampling_rate=125,
                           signal_preprocess=True)
    finally:
        device_coordinator.terminate()

main()