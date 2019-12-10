import os
import csv
import time
import random
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib
import multiprocessing
from screeninfo import get_monitors
from questionnaire import Questionnaire
from video import VideoStreaming
from gsr import GSRStreaming
#from eeg import EEGStreaming
import argparse
from open_vibe_triger import OpenVibeTrigge
from windows import ImageWindow, PauseWindow

monitors = get_monitors()
image_width =monitors[1].width
image_height =monitors[1].height
STIMULI_PATH = "mock_stimuli/"
Fixation_CROSS_IMAGE_PATH = "images/fixation_cross.jpg"
PAUSE_IMAGE_PATH = "images/pause_image.jpg"
GRAY_IMAGE_PATH = "images/gray_image.jpg"
DONE_IMAGE_PATH = "images/done_image.jpg"
STIMULI_SHOW_TIME = 5
FIXATION_CROSS_SHOW_TIME = 2
GRAY_IMAGE_SHOW_TIME = 3

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--subject_number", help="The subject number")
args = parser.parse_args()
subject_number = args.subject_number

class BackgroudWindow(Gtk.Window):
    def __init__(self, image_path, start_delay):
        Gtk.Window.__init__(self, title="")
        self._start_delay = start_delay
        self._next = None

        image_box = Gtk.Box()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, image_width,image_height, False)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        image_box.pack_start(image, False, False, 0)
        self.add(image_box)

        self._image_index = 0
        self._stimuli_list = os.listdir(STIMULI_PATH)
        random.shuffle(self._stimuli_list)

        # Save stimuli list order
        file_name = \
            "created_files/image_index/p{}-t{}.csv".format(subject_number, str(time.time()))
        #with open(file_name, 'w') as csv_file:
        #    writer = csv.writer(csv_file)
        #    for item in self._stimuli_list:
        #        writer.writerow([item])

        # Initializing recorders
        self._video_queue = multiprocessing.Queue()
        self._eeg_queue = multiprocessing.Queue()
        self._gsr_queue = multiprocessing.Queue()
        self._trigger_queue = multiprocessing.Queue()
        self._event_id_queue = multiprocessing.Queue()
        video_streaming = VideoStreaming(self._video_queue)
        #openvibe_trigger = OpenVibeTrigge(self._trigger_queue, self._event_id_queue)
        #gsr_streaming = GSRStreaming(self._gsr_queue)
        #eeg_streaming = EEGStreaming(self._eeg_queue)
        #eeg_streaming.start()
        video_streaming.start()
        #openvibe_trigger.start()
        #gsr_streaming.start()
        time.sleep(3)

    def show(self):
        '''
        Shows the backgroun window (A gray image)
        '''
        self.connect("destroy", Gtk.main_quit)
        self.fullscreen()
        self.show_all()

        GLib.timeout_add_seconds(self._start_delay, self._show_fixation_cross)
        Gtk.main()

    def _show_fixation_cross(self, *args):
        '''
        Showing fixation cross
        '''
        time.sleep(GRAY_IMAGE_SHOW_TIME)
        fixation_cross = \
            ImageWindow(Fixation_CROSS_IMAGE_PATH, FIXATION_CROSS_SHOW_TIME)
        fixation_cross.show_window()
        # This will call the next stimuli showing after disapearing the fixation cross
        fixation_cross.connect("destroy", self._show_image)

    def _show_image(self, *args):
        stimuli = \
            ImageWindow(STIMULI_PATH + self._stimuli_list[self._image_index],
                        STIMULI_SHOW_TIME)

        # Start video recording
        self._video_queue.put("p-{}-s{}-t{}".format(subject_number, self._image_index, str(time.time())))
        # Sending start trigger to OpenVibe
        self._event_id_queue.put(self._image_index)
        self._trigger_queue.put("start")
        # Start EEG recording
        self._eeg_queue.put("p-{}-s{}-t{}-eeg".format(subject_number, self._image_index, str(time.time())))
        # Start GSR and PPG recording
        self._gsr_queue.put("p-{}-s{}-t{}-gsr".format(subject_number, self._image_index, str(time.time())))

        # This will call the questionnaire showing after disapearing the stimili
        stimuli.show_window()
        self._next = self._show_questionnaire
        stimuli.connect("destroy", self._make_delay)

    def _make_delay(self, *args):
        GLib.timeout_add_seconds(0.5, self._next)

    def _show_questionnaire(self, *args):
        '''
        showing questionnaire
        '''
        # Stop video recording
        self._video_queue.put("stop_record")
        # sending stop trigger to OpenVibe
        self._trigger_queue.put("stop")
        # Stop EEG recording
        self._eeg_queue.put("stop_record")
        # Stop GSR and PPG recording
        self._gsr_queue.put("stop_record")

        questionnaire = Questionnaire(subject_number, self._image_index)
        questionnaire.show()
        self._next = self._show_next
        questionnaire.connect("destroy", self._make_delay)

    def _show_next(self, *args):
        self._image_index += 1
        if self._image_index >= len(self._stimuli_list):
            self._video_queue.put("terminate")
            self._eeg_queue.put("terminate")
            self._gsr_queue.put("terminate")
            self._trigger_queue.put("terminate")
            self._done()
            return
        elif self._image_index%2 == 0:
            self._pause()
        else:
            self._show_fixation_cross()

    def _pause(self, *args):
        pause_window = \
            PauseWindow(PAUSE_IMAGE_PATH)
        pause_window.show_window()
        self._next = self._show_fixation_cross
        pause_window.connect("destroy", self._make_delay)

    def _done(self, *args):
        done_window = \
            ImageWindow(DONE_IMAGE_PATH, 2)
        done_window.show_window()
        done_window.connect("destroy", self._terminate)

    def _terminate(self, *args):
        self.destroy()


def main():
    main_window = BackgroudWindow(GRAY_IMAGE_PATH, GRAY_IMAGE_SHOW_TIME)
    main_window.show()

main()
