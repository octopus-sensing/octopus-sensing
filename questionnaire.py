import gi
import csv
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

EMOTION_LIST = [ "anger", "disgust", "fear", "happy", "neutral", "sad","surprise", ]
CONVERSATION = 2
TALKING = 0
PATH = "created_files/answers"
FONT_STYLE = "<span font_desc='Tahoma 16'>{}</span>"

class AfterStimuliQuestionnaire(Gtk.Window):
    def __init__(self, participant_number, stimuli_number):
        self.file_name = \
            "{}/after_stimuli/{}-{}.csv".format(PATH, participant_number, str(time.time()))
        self.stimuli_number = stimuli_number
        self.q1_answer = 5 # Neutral
        self.q2_answer = 3 # mean
        self.q3_answer = 0 # No
        Gtk.Window.__init__(self, title="Questionnaire")
        self.set_border_width(10)
        self.set_default_size(400, 200)
        grid = Gtk.Grid(column_homogeneous=False,
                        column_spacing=10,
                        row_spacing=10)
        self.add(grid)

        # ****************************** Question1 *****************************
        question1_box, question1_options_box = self.__question1()
        grid.attach(question1_box, 0, 1, 1, 1)
        grid.attach(question1_options_box, 0, 2, 1, 1)

        # **************************** Question 2 ******************************
        question2_box, question2_options_box = self.__question2()
        grid.attach(question2_box, 0, 3, 1, 1)
        grid.attach(question2_options_box, 0, 4, 1, 1)

        # ***************************** Question 3 *****************************
        question3_box, question3_options_box = self.__question3()
        grid.attach(question3_box, 0, 5, 1, 1)
        grid.attach(question3_options_box, 0, 6, 1, 1)


        done_button = Gtk.Button.new_with_label("Done")
        done_button.connect("clicked", self.on_click_done_button)
        done_button.get_child().set_markup(FONT_STYLE.format("Done"))
        grid.attach(done_button, 0, 12, 1, 1)

    def __question1(self):
        question1_box = Gtk.Box(spacing=120)
        question1 = Gtk.Label()
        text = "1- Which emotion did you feel while watching the film?"
        question1.set_markup(FONT_STYLE.format(text))
        question1_box.pack_start(question1, False, False, 0)

        emotion_box = Gtk.Box(spacing=80)

        # emotion Radio buttons
        happy = Gtk.RadioButton.new_with_label_from_widget(None, "Happy")
        happy.connect("toggled", self.on_emotion_toggled, "4")
        happy.get_child().set_markup(FONT_STYLE.format("Happiness"))
        happy.set_property("width-request", 50)
        happy.set_property("height-request", 20)
        emotion_box.pack_start(happy, False, False, 0)

        sad = Gtk.RadioButton.new_with_label_from_widget(happy, "Sad")
        sad.connect("toggled", self.on_emotion_toggled, "6")
        sad.get_child().set_markup(FONT_STYLE.format("Sadness"))
        emotion_box.pack_start(sad, False, False, 0)

        surprise = Gtk.RadioButton.new_with_label_from_widget(happy, "Surprise")
        surprise.connect("toggled", self.on_emotion_toggled, "7")
        surprise.get_child().set_markup(FONT_STYLE.format("Surprise"))
        emotion_box.pack_start(surprise, False, False, 0)

        neutral = Gtk.RadioButton.new_with_label_from_widget(happy, "Neutral")
        neutral.connect("toggled", self.on_emotion_toggled, "5")
        neutral.get_child().set_markup(FONT_STYLE.format("Neutral"))
        emotion_box.pack_start(neutral, False, False, 0)
        neutral.set_active(True)

        fear = Gtk.RadioButton.new_with_label_from_widget(happy, "Fear")
        fear.connect("toggled", self.on_emotion_toggled, "3")
        fear.get_child().set_markup(FONT_STYLE.format("Fear"))
        emotion_box.pack_start(fear, False, False, 0)

        angry = Gtk.RadioButton.new_with_label_from_widget(happy, "Angry")
        angry.connect("toggled", self.on_emotion_toggled, "1")
        angry.get_child().set_markup(FONT_STYLE.format("Anger"))
        emotion_box.pack_start(angry, False, False, 0)

        disgust = Gtk.RadioButton.new_with_label_from_widget(happy, "Disgust")
        disgust.connect("toggled", self.on_emotion_toggled, "2")
        disgust.get_child().set_markup(FONT_STYLE.format("Disgust"))
        emotion_box.pack_start(disgust, False, False, 0)
        return question1_box, emotion_box

    def __question2(self):
        question2_box = Gtk.Box(spacing=100)
        text = "2- What is your certainty level? (1=low and 5=high)"
        question2 = Gtk.Label()
        question2.set_markup(FONT_STYLE.format(text))
        question2_box.pack_start(question2, False, False, 0)

        question2_options_box = Gtk.Box(spacing=80)

        # Question 2  Radio buttons
        one = Gtk.RadioButton.new_with_label_from_widget(None, "1")
        one.connect("toggled", self.on_q2_toggled, "1")
        one.get_child().set_markup(FONT_STYLE.format("1"))
        question2_options_box.pack_start(one, False, False, 0)

        two = Gtk.RadioButton.new_with_label_from_widget(one, "2")
        two.connect("toggled", self.on_q2_toggled, "2")
        two.get_child().set_markup(FONT_STYLE.format("2"))
        question2_options_box.pack_start(two, False, False, 0)

        three = Gtk.RadioButton.new_with_label_from_widget(one, "3")
        three.connect("toggled", self.on_q2_toggled, "3")
        three.get_child().set_markup(FONT_STYLE.format("3"))
        question2_options_box.pack_start(three, False, False, 0)
        three.set_active(True)

        four = Gtk.RadioButton.new_with_label_from_widget(one, "4")
        four.connect("toggled", self.on_q2_toggled, "4")
        four.get_child().set_markup(FONT_STYLE.format("4"))
        question2_options_box.pack_start(four, False, False, 0)

        five = Gtk.RadioButton.new_with_label_from_widget(one, "5")
        five.connect("toggled", self.on_q2_toggled, "5")
        five.get_child().set_markup(FONT_STYLE.format("5"))
        question2_options_box.pack_start(five, False, False, 0)

        return question2_box, question2_options_box

    def __question3(self):
        question3_box = Gtk.Box(spacing=100)
        text = "3- Had you seen this film before?"
        question3 = Gtk.Label()
        question3.set_markup(FONT_STYLE.format(text))
        question3_box.pack_start(question3, False, False, 0)

        question3_options_box = Gtk.Box(spacing=80)

        # Question 2  Radio buttons
        q3_no = Gtk.RadioButton.new_with_label_from_widget(None, "No")
        q3_no.connect("toggled", self.on_q3_toggled, "0")
        q3_no.get_child().set_markup(FONT_STYLE.format("No"))
        question3_options_box.pack_start(q3_no, False, False, 0)
        q3_no.set_active(True)

        q3_yes = Gtk.RadioButton.new_with_label_from_widget(q3_no, "Yes")
        q3_yes.connect("toggled", self.on_q3_toggled, "1")
        q3_yes.get_child().set_markup(FONT_STYLE.format("Yes"))
        question3_options_box.pack_start(q3_yes, False, False, 0)
        return question3_box, question3_options_box

    def on_emotion_toggled(self, button, name):
        if button.get_active():
            self.q1_answer = int(name)
    def on_q2_toggled(self, button, name):
        if button.get_active():
            self.q2_answer = int(name)

    def on_q3_toggled(self, button, name):
        if button.get_active():
            self.q3_answer = int(name)

    def on_click_done_button(self, button):
        self.save_answers()
        self.destroy()

    def save_answers(self):
        row = []
        row.append(self.stimuli_number)
        row.append(self.q1_answer)
        row.append(self.q2_answer)
        row.append(self.q3_answer)
        with open(self.file_name, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()

    def show(self):
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

class ConversationQuestionnaire(Gtk.Window):
    def __init__(self, timeout, stimuli_index, eeg_trigger_queue, gsr_trigger_queue):
        self._timeout = timeout
        self._eeg_trigger_queue = eeg_trigger_queue
        self._gsr_trigger_queue = gsr_trigger_queue
        self._stimuli_index = stimuli_index

        Gtk.Window.__init__(self, title="Questionnaire")
        self.set_border_width(10)
        self.set_default_size(400, 200)
        grid = Gtk.Grid(column_homogeneous=False,
                        column_spacing=10,
                        row_spacing=10)
        self.add(grid)

        image = Gtk.Image.new_from_file("images/happiness-s.jpg")
        happy_button = Gtk.Button()
        happy_button.connect("clicked", self.on_click_happy_button)
        happy_button.add(image)

        image = Gtk.Image.new_from_file("images/sadness-s.jpg")
        sad_button = Gtk.Button()
        sad_button.connect("clicked", self.on_click_sad_button)
        sad_button.add(image)

        image = Gtk.Image.new_from_file("images/fear-s.jpg")
        fear_button = Gtk.Button()
        fear_button.connect("clicked", self.on_click_fear_button)
        fear_button.add(image)

        image = Gtk.Image.new_from_file("images/neutral-s.jpg")
        neutral_button = Gtk.Button()
        neutral_button.connect("clicked", self.on_click_neutral_button)
        neutral_button.add(image)

        image = Gtk.Image.new_from_file("images/surprise-s.jpg")
        surprise_button = Gtk.Button()
        surprise_button.connect("clicked", self.on_click_surprise_button)
        surprise_button.add(image)

        image = Gtk.Image.new_from_file("images/disgust-s.jpg")
        disgust_button = Gtk.Button()
        disgust_button.connect("clicked", self.on_click_disgust_button)
        disgust_button.add(image)

        image = Gtk.Image.new_from_file("images/anger-s.jpg")
        anger_button = Gtk.Button()
        anger_button.connect("clicked", self.on_click_anger_button)
        anger_button.add(image)

        inner_box = Gtk.HBox()
        inner_box.pack_start(Gtk.Alignment(), True, True, 0)
        inner_box.pack_start(happy_button, False, False, 0)
        inner_box.pack_start(Gtk.Alignment(), True, True, 0)

        inner_box.pack_start(Gtk.Alignment(), True, True, 0)
        inner_box.pack_start(sad_button, False, False, 0)
        inner_box.pack_start(Gtk.Alignment(), True, True, 0)

        inner_box.pack_start(Gtk.Alignment(), True, True, 0)
        inner_box.pack_start(fear_button, False, False, 0)
        inner_box.pack_start(Gtk.Alignment(), True, True, 0)

        inner_box.pack_start(Gtk.Alignment(), True, True, 0)
        inner_box.pack_start(neutral_button, False, False, 0)
        inner_box.pack_start(Gtk.Alignment(), True, True, 0)

        inner_box.pack_start(Gtk.Alignment(), True, True, 0)
        inner_box.pack_start(surprise_button, False, False, 0)
        inner_box.pack_start(Gtk.Alignment(), True, True, 0)

        inner_box.pack_start(Gtk.Alignment(), True, True, 0)
        inner_box.pack_start(disgust_button, False, False, 0)
        inner_box.pack_start(Gtk.Alignment(), True, True, 0)

        inner_box.pack_start(Gtk.Alignment(), True, True, 0)
        inner_box.pack_start(anger_button, False, False, 0)
        inner_box.pack_start(Gtk.Alignment(), True, True, 0)


        outer_box = Gtk.VBox()
        outer_box.pack_start(inner_box, False, False, 0)

        grid.attach(outer_box, 0, 1, 1, 1)

    def on_click_happy_button(self, button):
        trigger = (CONVERSATION * 1000 +
                   TALKING * 100 +
                   self._stimuli_index * 10 +
                   EMOTION_LIST.index("happy")+1)
        self._eeg_trigger_queue.put(trigger)
        self._gsr_trigger_queue.put(trigger)

    def on_click_neutral_button(self, button):
        trigger = (CONVERSATION * 1000 +
                   TALKING * 100 +
                   self._stimuli_index * 10 +
                   EMOTION_LIST.index("neutral")+1)
        self._eeg_trigger_queue.put(trigger)
        self._gsr_trigger_queue.put(trigger)

    def on_click_sad_button(self, button):
        trigger = (CONVERSATION * 1000 +
                   TALKING * 100 +
                   self._stimuli_index * 10 +
                   EMOTION_LIST.index("sad")+1)
        self._eeg_trigger_queue.put(trigger)
        self._gsr_trigger_queue.put(trigger)

    def on_click_anger_button(self, button):
        trigger = (CONVERSATION * 1000 +
                   TALKING * 100 +
                   self._stimuli_index * 10 +
                   EMOTION_LIST.index("anger")+1)
        self._eeg_trigger_queue.put(trigger)
        self._gsr_trigger_queue.put(trigger)

    def on_click_surprise_button(self, button):
        trigger = (CONVERSATION * 1000 +
                   TALKING * 100 +
                   self._stimuli_index * 10 +
                   EMOTION_LIST.index("surprise")+1)
        self._eeg_trigger_queue.put(trigger)
        self._gsr_trigger_queue.put(trigger)

    def on_click_disgust_button(self, button):
        trigger = (CONVERSATION * 1000 +
                   TALKING * 100 +
                   self._stimuli_index * 10 +
                   EMOTION_LIST.index("disgust")+1)
        self._eeg_trigger_queue.put(trigger)
        self._gsr_trigger_queue.put(trigger)

    def on_click_fear_button(self, button):
        trigger = (CONVERSATION * 1000 +
                   TALKING * 100 +
                   self._stimuli_index * 10 +
                   EMOTION_LIST.index("fear")+1)
        self._eeg_trigger_queue.put(trigger)
        self._gsr_trigger_queue.put(trigger)

    def show(self):
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def show_window(self):
        GLib.timeout_add_seconds(self._timeout, self.destroy)
        self.show()

class AfterConversationQuestionnaire(Gtk.Window):
    def __init__(self, participant_number, stimuli_number):
        self.file_name = \
            "{}/after_conversation/{}-{}.csv".format(PATH, participant_number, str(time.time()))
        self.stimuli_number = stimuli_number
        self.q1_answer = 5 # Neutral
        self.q2_answer = 3 # Mean
        Gtk.Window.__init__(self, title="Questionnaire")
        self.set_border_width(10)
        self.set_default_size(400, 200)
        grid = Gtk.Grid(column_homogeneous=False,
                        column_spacing=10,
                        row_spacing=10)
        self.add(grid)

        # ****************************** Question1 *****************************
        question1_box, question1_options_box = self.__question1()
        grid.attach(question1_box, 0, 1, 1, 1)
        grid.attach(question1_options_box, 0, 2, 1, 1)

        # **************************** Question 2 ******************************
        question2_box, question2_options_box = self.__question2()
        grid.attach(question2_box, 0, 3, 1, 1)
        grid.attach(question2_options_box, 0, 4, 1, 1)


        done_button = Gtk.Button.new_with_label("Done")
        done_button.connect("clicked", self.on_click_done_button)
        done_button.get_child().set_markup(FONT_STYLE.format("Done"))
        grid.attach(done_button, 0, 12, 1, 1)


    def __question1(self):
        question1_box = Gtk.Box(spacing=120)
        question1 = Gtk.Label()
        text = "1- Overall, which emotion did you feel during the conversation?"
        question1.set_markup(FONT_STYLE.format(text))
        question1_box.pack_start(question1, False, False, 0)

        emotion_box = Gtk.Box(spacing=80)

        # emotion Radio buttons
        happy = Gtk.RadioButton.new_with_label_from_widget(None, "Happy")
        happy.connect("toggled", self.on_emotion_toggled, "4")
        happy.get_child().set_markup(FONT_STYLE.format("Happiness"))
        emotion_box.pack_start(happy, False, False, 0)

        sad = Gtk.RadioButton.new_with_label_from_widget(happy, "Sad")
        sad.connect("toggled", self.on_emotion_toggled, "6")
        sad.get_child().set_markup(FONT_STYLE.format("Sadness"))
        emotion_box.pack_start(sad, False, False, 0)

        surprise = Gtk.RadioButton.new_with_label_from_widget(happy, "Surprise")
        surprise.connect("toggled", self.on_emotion_toggled, "7")
        surprise.get_child().set_markup(FONT_STYLE.format("Surprise"))
        emotion_box.pack_start(surprise, False, False, 0)

        neutral = Gtk.RadioButton.new_with_label_from_widget(happy, "Neutral")
        neutral.connect("toggled", self.on_emotion_toggled, "5")
        neutral.get_child().set_markup(FONT_STYLE.format("Neutral"))
        emotion_box.pack_start(neutral, False, False, 0)
        neutral.set_active(True)

        fear = Gtk.RadioButton.new_with_label_from_widget(happy, "Fear")
        fear.connect("toggled", self.on_emotion_toggled, "3")
        fear.get_child().set_markup(FONT_STYLE.format("Fear"))
        emotion_box.pack_start(fear, False, False, 0)

        angry = Gtk.RadioButton.new_with_label_from_widget(happy, "Angry")
        angry.connect("toggled", self.on_emotion_toggled, "1")
        angry.get_child().set_markup(FONT_STYLE.format("Anger"))
        emotion_box.pack_start(angry, False, False, 0)

        disgust = Gtk.RadioButton.new_with_label_from_widget(happy, "Disgust")
        disgust.connect("toggled", self.on_emotion_toggled, "2")
        disgust.get_child().set_markup(FONT_STYLE.format("Disgust"))
        emotion_box.pack_start(disgust, False, False, 0)
        return question1_box, emotion_box

    def __question2(self):
        question2_box = Gtk.Box(spacing=100)
        question2 = Gtk.Label()
        text = "2- What is your certainty level? (1=low and 5=high)"
        question2.set_markup(FONT_STYLE.format(text))
        question2_box.pack_start(question2, False, False, 0)

        question2_options_box = Gtk.Box(spacing=80)

        # Question 2  Radio buttons
        one = Gtk.RadioButton.new_with_label_from_widget(None, "1")
        one.connect("toggled", self.on_q2_toggled, "1")
        one.get_child().set_markup(FONT_STYLE.format("1"))
        question2_options_box.pack_start(one, False, False, 0)

        two = Gtk.RadioButton.new_with_label_from_widget(one, "2")
        two.connect("toggled", self.on_q2_toggled, "2")
        two.get_child().set_markup(FONT_STYLE.format("2"))
        question2_options_box.pack_start(two, False, False, 0)

        three = Gtk.RadioButton.new_with_label_from_widget(one, "3")
        three.connect("toggled", self.on_q2_toggled, "3")
        three.get_child().set_markup(FONT_STYLE.format("3"))
        question2_options_box.pack_start(three, False, False, 0)
        three.set_active(True)

        four = Gtk.RadioButton.new_with_label_from_widget(one, "4")
        four.connect("toggled", self.on_q2_toggled, "4")
        four.get_child().set_markup(FONT_STYLE.format("4"))
        question2_options_box.pack_start(four, False, False, 0)

        five = Gtk.RadioButton.new_with_label_from_widget(one, "5")
        five.connect("toggled", self.on_q2_toggled, "5")
        five.get_child().set_markup(FONT_STYLE.format("5"))
        question2_options_box.pack_start(five, False, False, 0)

        return question2_box, question2_options_box
    def on_emotion_toggled(self, button, name):
        if button.get_active():
            self.q1_answer = int(name)
    def on_q2_toggled(self, button, name):
        if button.get_active():
            self.q2_answer = int(name)

    def on_click_done_button(self, button):
        self.save_answers()
        self.destroy()

    def save_answers(self):
        row = []
        row.append(self.stimuli_number)
        row.append(self.q1_answer)
        row.append(self.q2_answer)
        with open(self.file_name, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()

    def show(self):
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

#import multiprocessing
#win = ConversationQuestionnaire(10, 1,multiprocessing.Queue(), multiprocessing.Queue())
#win.connect("destroy", Gtk.main_quit)
#win.show_all()
#Gtk.main()
