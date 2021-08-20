
from windows.message_window import MessageWindow
from windows.image_window import ImageWindow
import argparse
from screeninfo import get_monitors
from gi.repository import Gtk, GdkPixbuf, GLib
import os
import time
import datetime
import sys  # nopep8
sys.path.append('../octopus-sensing/')  # nopep8

from stimuli_loader import load_stimuli
from questionnaires import get_video_questionnaire
from octopus_sensing.common.message_creators import start_message, stop_message
from octopus_sensing.devices.camera_streaming import CameraStreaming
from octopus_sensing.devices.openbci_streaming import OpenBCIStreaming
from octopus_sensing.devices.shimmer3_streaming import Shimmer3Streaming
from octopus_sensing.device_coordinator import DeviceCoordinator
from octopus_sensing.devices.network_devices.socket_device import SocketNetworkDevice
import logging
import gi
gi.require_version('Gtk', '3.0')


stimuli_path = "examples/stimuli/"
FIXATION_CROSS_SHOW_TIME = 3
GAP_TIME = 2


class MainWindow(Gtk.Window):
    def __init__(self, experiment_id, stimuli_list, device_coordinator):
        time_str = datetime.datetime.strftime(datetime.datetime.now(),
                                              "%Y-%m-%dT%H-%M-%S")
        logging.basicConfig(filename='examples/logs/watching_video_log_{0}_{1}.log'.format(experiment_id, time_str),
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
        background_path = "examples/images/gray_image.jpg"
        pixbuf = \
            GdkPixbuf.Pixbuf.new_from_file_at_scale(background_path,
                                                    image_width,
                                                    image_height, False)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        image_box.pack_start(image, False, False, 0)
        self.add(image_box)

    def show(self):
        '''
        Shows the background window (A gray image)
        '''
        logging.info("Start time {0}".format(datetime.datetime.now()))
        message = start_message(self._experiment_id, 0)
        # self._monitoring_device_coordinator.dispatch(message)

        self.connect("destroy", Gtk.main_quit)
        self.fullscreen()
        self.show_all()

        GLib.timeout_add_seconds(5, self._show_fixation_cross)
        Gtk.main()

    def _show_fixation_cross(self, *args):
        '''
        Showing fixation cross before each stimuli
        '''
        logging.info("Fixation cross {0}".format(datetime.datetime.now()))
        fixation_cross = \
            ImageWindow("examples/images/fixation_cross.jpg", FIXATION_CROSS_SHOW_TIME)
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
        After stimuli questionnaire
        '''
        logging.info("Questionnaire start {0}".format(datetime.datetime.now()))
        questionnaire = \
            get_video_questionnaire("self-report",
                                    self._experiment_id,
                                    self._stimuli_list[self._stimuli_index].id,
                                    "Questionnaire")
        questionnaire.show()
        questionnaire.connect("destroy", self._relaxation)

    def _relaxation(self, *args):
        GLib.timeout_add_seconds(GAP_TIME, self._show_next)

    def _show_next(self, *args):
        self._stimuli_index += 1
        if self._stimuli_index >= len(self._stimuli_list):
            self._done()
        else:
            self._show_fixation_cross()

    def _pause(self, *args):
        pause_window = \
            MessageWindow("examples/images/pause_image.jpg")
        pause_window.show_window()
        pause_window.connect("destroy", self._show_fixation_cross)

    def _done(self, *args):
        message = stop_message(self._experiment_id, 0)
        # self._monitoring_device_coordinator.dispatch(message)
        logging.info("End time {0}".format(datetime.datetime.now()))
        self._device_coordinator.terminate()
        done_window = \
            ImageWindow("examples/images/done_image.jpg", 2)
        done_window.show_window()
        done_window.connect("destroy", self._terminate)

    def _terminate(self, *args):
        # self._monitoring_device_coordinator.terminate()
        self.destroy()


def get_input_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subject_id", help="The subject ID", default=0)
    #parser.add_argument("-t", "--task_id", help="The task ID", default=0)
    args = parser.parse_args()
    subject_id = args.subject_id
    task_id = 0  # args.task_id
    return subject_id, task_id


def main():   
    subject_id, task_id = get_input_parameters()
    experiment_id = str(subject_id).zfill(2) + "-" + str(task_id).zfill(2)
    output_path = "examples/output/video/p{0}".format(subject_id)
    os.makedirs(output_path, exist_ok=False)


    ####### Create video device ###########
    #webcam_camera_path = "/dev/v4l/by-id/usb-046d_081b_97E6A7D0-video-index0"
    #main_camera = \
    #    CameraStreaming(name="camera",
    #                    output_path=output_path,
    #                   camera_path=webcam_camera_path,
    #                    image_width=640,
    #                   image_height=360)

    ####### Create OpenBCI device ###########
    #openbci = OpenBCIStreaming(name="OpenBCI_video", output_path=output_path)

    ####### Create Shimmer3 device ###########
    #shimmer = Shimmer3Streaming(name="Shimmer_video", output_path=output_path)

    ####### Create Network device ###########
    socket_device = SocketNetworkDevice("localhost", 5003)

    # Add to device coordinator for synchronous data recording
    device_coordinator = DeviceCoordinator()
    device_coordinator.add_devices([socket_device])#, openbci, shimmer, main_camera])

    stimuli_list = load_stimuli(stimuli_path)
    # Make delay for initializing all processes
    time.sleep(5)

    main_window = \
        MainWindow(experiment_id,
                   stimuli_list,
                   device_coordinator)
    main_window.show()


main()
