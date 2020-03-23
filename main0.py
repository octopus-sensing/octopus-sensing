import os
import csv
import time
import datetime
import random
import gi
import logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib
import multiprocessing
from screeninfo import get_monitors
from questionnaire import AfterStimuliQuestionnaire, ConversationQuestionnaire, \
                          AfterConversationQuestionnaire
from video import VideoStreaming
from audio import AudioStreaming
from gsr import GSRStreaming
from eeg import EEGStreaming
import argparse
#from open_vibe_trigger import OpenVibeTrigger
from windows import ImageWindow, MessageWindow

from pydub import AudioSegment
from pydub.playback import play

time_str = datetime.datetime.strftime(datetime.datetime.now(),
                                     "%Y-%m-%dT%H-%M-%S")

logging.basicConfig(filename='logs/log_file-{}.log'.format(time_str),
                    level=logging.DEBUG)

STOP_SOUND = AudioSegment.from_wav('stop.wav')

monitors = get_monitors()
image_width = monitors[0].width
image_height = monitors[0].height
STIMULI_PATH = "stimuli-mock/"
Fixation_CROSS_IMAGE_PATH = "images/fixation_cross.jpg"
PAUSE_IMAGE_PATH = "images/pause_image.jpg"
CONVERSATION_START_IMAGE_PATH = "images/conversation_start_image.jpg"
AFTER_CONVERSATION_IMAGE_PATH = "images/after_conversation_image.jpg"
GRAY_IMAGE_PATH = "images/gray_image.jpg"
DONE_IMAGE_PATH = "images/done_image.jpg"
CONVERSATION_TIME = 10
FIXATION_CROSS_SHOW_TIME = 1
GRAY_IMAGE_SHOW_TIME = 2
# These constants are for making trigger in different conditions
STIMULI = 1
CONVERSATION = 2
START = 1
STOP = 2

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--subject_number", help="The subject number")
args = parser.parse_args()
subject_number = args.subject_number

logging.info('Start for participant {}'.format(subject_number))
logging.info("stimuli path : {}".format(STIMULI_PATH))
logging.info("CONVERSATION_TIME = {}".format(CONVERSATION_TIME))
logging.info("FIXATION_CROSS_SHOW_TIME = {}".format(FIXATION_CROSS_SHOW_TIME))
logging.info("GRAY_IMAGE_SHOW_TIME = {}".format(GRAY_IMAGE_SHOW_TIME))

class BackgroudWindow(Gtk.Window):
    def __init__(self, image_path, start_delay):
        Gtk.Window.__init__(self, title="")
        self._start_delay = start_delay
        self._next = None

        image_box = Gtk.Box()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, image_width, image_height, False)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        image_box.pack_start(image, False, False, 0)
        self.add(image_box)

        self._film_index = 0
        self._stimuli_list = os.listdir(STIMULI_PATH)
        random.shuffle(self._stimuli_list)
        logging.info("Stimuli order for participant {0} is {1}".format(subject_number,
                                                                       self._stimuli_list))
        # Save stimuli list order
        time_str = datetime.datetime.strftime(datetime.datetime.now(),
                                             "%Y-%m-%dT%H-%M-%S")
        file_name = \
            "created_files/film_index/p-{}-t{}.csv".format(subject_number,
                                                           time_str)
        logging.info("Stimuli file name is {}".format(file_name))
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for item in self._stimuli_list:
                writer.writerow([item])

        # Initializing quesues for passing messages to processes
        self._video_stimuli_queue = multiprocessing.Queue()
        self._video_conv_queue = multiprocessing.Queue()
        self._eeg_trigger_queue = multiprocessing.Queue()
        self._gsr_trigger_queue = multiprocessing.Queue()

        logging.info("Initializing camera 2 for watching video")
        # Creating object for recording video during stimuli showing
        video_streaming_stimuli = VideoStreaming(self._video_stimuli_queue, 2)

        logging.info("Initializing camera 1 for conversation")
        # Creating object for recording video during conversation
        video_streaming_conv = VideoStreaming(self._video_conv_queue, 1)

        # Creating object for sending trigger to OpenVibe
        #openvibe_trigger = OpenVibeTrigger(self._eeg_trigger_queue)
        time_str = datetime.datetime.strftime(datetime.datetime.now(),
                                             "%Y-%m-%dT%H-%M-%S")
        # Creating object for sending trigger to gsr streaming
        gsr_file_name = "p{}-t{}-gsr".format(str(subject_number).zfill(2),
                                             time_str)

        logging.info("Start GSR streaming {}".format(gsr_file_name))
        gsr_streaming = GSRStreaming(gsr_file_name, self._gsr_trigger_queue)

        eeg_file_name = "p{}-t{}-eeg".format(str(subject_number).zfill(2),
                                             time_str)

        logging.info("Start GSR streaming {}".format(eeg_file_name))
        eeg_streaming = EEGStreaming(eeg_file_name, self._eeg_trigger_queue)

        # Audio recorder will initialize in loop. It could run just in thread

        # Starting all processes
        logging.info("Start video streaming process")
        video_streaming_stimuli.start()
        video_streaming_conv.start()
        #openvibe_trigger.start()
        logging.info("Start GSR streaming process")
        gsr_streaming.start()
        logging.info("Start EEG streaming process")
        eeg_streaming.start()

        # Make delay for initializing all processes
        time.sleep(5)
        logging.info("End of initializing {}".format(datetime.datetime.now()))

    def show(self):
        '''
        Shows the background window (A gray image)
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
        fixation_cross.connect("destroy", self._show_film)

    def _show_film(self, *args):
        '''
        Showing stimuli. It uses vlc for showing video
        '''
        time_str = datetime.datetime.strftime(datetime.datetime.now(),
                                              "%Y-%m-%dT%H-%M-%S")
        # Start video recording
        stimuli_recorded_video_file_name = \
            "stimuli/p{}-s{}-t{}".format(str(subject_number).zfill(2),
                                         str(self._film_index).zfill(2),
                                         time_str)
        trigger = STIMULI * 1000 + START * 100 + self._film_index * 10
        # start
        self._video_stimuli_queue.put(stimuli_recorded_video_file_name)

        self.__sending_triggers("Start stimuli",
                                trigger,
                                trigger)

        logging.info("Start showing stimuli {}, time {} ".format(
                     self._stimuli_list[self._film_index],
                     datetime.datetime.now()))
        # Showing stimuli
        os.system("sh play_video.sh {}".format(STIMULI_PATH + self._stimuli_list[self._film_index]))

        self._next = self._stop_stimuli
        GLib.timeout_add_seconds(0, self._next)

    def _stop_stimuli(self, *args):
        trigger = STIMULI * 1000 + STOP * 100 + self._film_index * 10
        self._video_stimuli_queue.put("stop_record")
        self.__sending_triggers("Stop stimuli",
                                trigger,
                                trigger)

        self._next = self._after_stimuli_questionnaire
        self._make_delay()

    def __sending_triggers(self,
                           message,
                           eeg_command,
                           gsr_command):
        logging.info("Sending trigger {}, eeg {}, gsr {}, time {}".format(
                     message,
                     eeg_command,
                     gsr_command,
                     datetime.datetime.now()))
        self._eeg_trigger_queue.put(eeg_command)
        self._gsr_trigger_queue.put(gsr_command)

    def _after_stimuli_questionnaire(self, *args):
        '''
        After stimuli questionnaire
        '''
        logging.info("Stimuli questionnaire, {}".format(datetime.datetime.now()))
        questionnaire = \
            AfterStimuliQuestionnaire(subject_number, self._film_index)
        #questionnaire.set_position(Gtk.WIN_POS_CENTER)
        questionnaire.set_keep_above(True)
        questionnaire.show()
        self._next = self._conversation_start_screen
        questionnaire.connect("destroy", self._make_delay)

    def _conversation_start_screen(self, *args):
        '''
        It opens a window and show some messages to participant to prepare for
         conversation
        '''
        # Showing message
        logging.info("Preparation for conversation, {}".format(datetime.datetime.now()))
        conversation_start_window = \
            MessageWindow(CONVERSATION_START_IMAGE_PATH)
        conversation_start_window.set_keep_above(True)
        conversation_start_window.show_window()
        self._next = self._conversation
        conversation_start_window.connect("destroy", self._make_delay)

    def _conversation(self, *args):
        logging.info("Start conversation, ".format(datetime.datetime.now()))
        i = 0
        time_str = datetime.datetime.strftime(datetime.datetime.now(),
                                             "%Y-%m-%dT%H-%M-%S")
        # Audio recording
        audio_file_name = "p{}-s{}-t{}".format(str(subject_number).zfill(2),
                                               str(self._film_index).zfill(2),
                                               time_str)
        audio_streaming = AudioStreaming(audio_file_name, CONVERSATION_TIME + 3)
        audio_streaming.start()

        video_command = \
            "conversation/p{}-s{}-t{}".format(str(subject_number).zfill(2),
                                              str(self._film_index).zfill(2),
                                              time_str)
        self._video_conv_queue.put(video_command)
        logging.info("Video {}, Audio {}, {}".format(audio_file_name,
                                                     video_command,
                                                     datetime.datetime.now()))
        while i < 3:
            # Sending start trigger to eeg and gsr recording
            trigger = \
                CONVERSATION * 1000 + START * 100 + self._film_index * 10 + i
            self.__sending_triggers("Start conversation part {}".format(i),
                                    trigger,
                                    trigger)

            time.sleep(CONVERSATION_TIME)
            # Sending stop trigger
            trigger = \
                CONVERSATION * 1000 + STOP * 100 + self._film_index * 10 + i
            self.__sending_triggers("Stop conversation part {}".format(i),
                                    trigger,
                                    trigger)
            questionnaire = \
                ConversationQuestionnaire(subject_number,
                                          self._film_index,
                                          i)
            questionnaire.set_keep_above(True)
            questionnaire.show()
            i += 1
        self._video_conv_queue.put("stop_record")
        self._relaxation()

    def _relaxation(self, *args):
        print("relaxation")
        self._next = self._show_next
        GLib.timeout_add_seconds(3, self._next)

    def _make_delay(self, *args):
        GLib.timeout_add_seconds(0.5, self._next)

    def _show_next(self, *args):
        self._film_index += 1
        if self._film_index >= len(self._stimuli_list):
            print("here")
            self._video_conv_queue.put("terminate")
            self._video_stimuli_queue.put("terminate")
            self._eeg_trigger_queue.put("terminate")
            self._gsr_trigger_queue.put("terminate")
            self._done()
            #self.destroy()
            return
        elif self._film_index%3 == 0:
            self._pause()
        else:
            self._prepare_for_next()

    def _prepare_for_next(self, *args):
        prepare_window = \
            MessageWindow(AFTER_CONVERSATION_IMAGE_PATH)
        prepare_window.show_window()
        self._next = self._show_fixation_cross
        prepare_window.connect("destroy", self._make_delay_long)

    def _make_delay_long(self, *args):
        GLib.timeout_add_seconds(3, self._next)

    def _pause(self, *args):
        pause_window = \
            MessageWindow(PAUSE_IMAGE_PATH)
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
