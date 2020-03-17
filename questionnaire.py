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
            "{}/after_stimuli/{}.csv".format(PATH, participant_number)
        self.stimuli_number = stimuli_number
        self.q1_answer = 5 # Neutral
        self.q2_answer = 3 # mean
        self.q3_answer = 0 # No
        self.valence_level = 5 # middle
        self.arousal_level = 5 # middle
        self.dominance_level = 5 # middle
        Gtk.Window.__init__(self, title="Questionnaire")
        self.set_border_width(10)
        self.set_default_size(400, 200)
        grid = Gtk.Grid(column_homogeneous=False,
                        column_spacing=10,
                        row_spacing=10)
        self.add(grid)

        # ****************************** Question1 ****************************
        question1_box, question1_options_box = self.__question1()
        grid.attach(question1_box, 0, 1, 1, 1)
        grid.attach(question1_options_box, 0, 2, 1, 1)

        # **************************** Question 2 *****************************
        question2_box, question2_options_box = self.__question2()
        grid.attach(question2_box, 0, 3, 1, 1)
        grid.attach(question2_options_box, 0, 4, 1, 1)

        # ***************************** Question 3 ****************************
        question3_box, question3_options_box = self.__question3()
        grid.attach(question3_box, 0, 5, 1, 1)
        grid.attach(question3_options_box, 0, 6, 1, 1)

        # ***************************** Question 4 **********************8*****
        question4_box, valence_image_box, valence_box = self.__question4()
        grid.attach(question4_box, 0, 7, 1, 1)
        grid.attach(valence_image_box, 0, 8, 1, 1)
        grid.attach(valence_box, 0, 9, 1, 1)

        # ***************************** Question 5 **********************8*****
        question5_box, arousal_image_box, arousal_box = self.__question5()
        grid.attach(question5_box, 0, 10, 1, 1)
        grid.attach(arousal_image_box, 0, 11, 1, 1)
        grid.attach(arousal_box, 0, 12, 1, 1)

        # ***************************** Question 6 **********************8*****
        question6_box, dominance_image_box, dominance_box = self.__question6()
        grid.attach(question6_box, 0, 13, 1, 1)
        grid.attach(dominance_image_box, 0, 14, 1, 1)
        grid.attach(dominance_box, 0, 15, 1, 1)

        done_button = Gtk.Button.new_with_label("Done")
        done_button.connect("clicked", self.on_click_done_button)
        done_button.get_child().set_markup(FONT_STYLE.format("Done"))
        grid.attach(done_button, 0, 17, 1, 1)

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

    def __question4(self):
        question4_box = Gtk.Box(spacing=100)
        question4 = Gtk.Label()
        text = "4- Your Valence level: Negative to Positive"
        question4.set_markup(FONT_STYLE.format(text))
        question4_box.pack_start(question4, False, False, 0)

        valence_image_box = Gtk.Box(spacing=120)
        valence_image = Gtk.Image.new_from_file('images/SAM-V-9-0.png')
        valence_image_box.pack_start(valence_image, False, False, 0)

        valence_box = Gtk.Box(spacing=120)
        # Valence Radio buttons
        v_button1 = Gtk.RadioButton.new_from_widget(None)
        v_button1.connect("toggled", self.on_valence_toggled, "1")
        valence_box.pack_start(v_button1, False, False, 45)

        v_button2 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button2.connect("toggled", self.on_valence_toggled, "2")
        valence_box.pack_start(v_button2, False, False, 0)

        v_button3 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button3.connect("toggled", self.on_valence_toggled, "3")
        valence_box.pack_start(v_button3, False, False, 0)

        v_button4 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button4.connect("toggled", self.on_valence_toggled, "4")
        valence_box.pack_start(v_button4, False, False, 0)

        v_button5 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button5.connect("toggled", self.on_valence_toggled, "5")
        valence_box.pack_start(v_button5, False, False, 0)
        v_button5.set_active(True)

        v_button6 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button6.connect("toggled", self.on_valence_toggled, "6")
        valence_box.pack_start(v_button6, False, False, 0)

        v_button7 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button7.connect("toggled", self.on_valence_toggled, "7")
        valence_box.pack_start(v_button7, False, False, 0)

        v_button8 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button8.connect("toggled", self.on_valence_toggled, "8")
        valence_box.pack_start(v_button8, False, False, 0)

        v_button9 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button9.connect("toggled", self.on_valence_toggled, "9")
        valence_box.pack_start(v_button9, False, False, 0)

        return question4_box, valence_image_box, valence_box

    def __question5(self):
        question5_box = Gtk.Box(spacing=120)
        question5 = Gtk.Label()
        text = "5- Your Arousal level: Calm to Excited"
        question5.set_markup(FONT_STYLE.format(text))
        question5_box.pack_start(question5, False, False, 0)

        arousal_image_box = Gtk.Box(spacing=120)
        arousal_image = Gtk.Image.new_from_file('images/SAM-A-9-0.png')
        arousal_image_box.pack_start(arousal_image, False, False, 0)

        arousal_box = Gtk.Box(spacing=120)

        # Arousal Radio buttons
        a_button1 = Gtk.RadioButton.new_from_widget(None)
        a_button1.connect("toggled", self.on_arousal_toggled, "1")
        arousal_box.pack_start(a_button1, False, False, 45)

        a_button2 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button2.connect("toggled", self.on_arousal_toggled, "2")
        arousal_box.pack_start(a_button2, False, False, 0)

        a_button3 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button3.connect("toggled", self.on_arousal_toggled, "3")
        arousal_box.pack_start(a_button3, False, False, 0)

        a_button4 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button4.connect("toggled", self.on_arousal_toggled, "4")
        arousal_box.pack_start(a_button4, False, False, 0)

        a_button5 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button5.connect("toggled", self.on_arousal_toggled, "5")
        arousal_box.pack_start(a_button5, False, False, 0)
        a_button5.set_active(True)

        a_button6 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button6.connect("toggled", self.on_arousal_toggled, "6")
        arousal_box.pack_start(a_button6, False, False, 0)

        a_button7 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button7.connect("toggled", self.on_arousal_toggled, "7")
        arousal_box.pack_start(a_button7, False, False, 0)

        a_button8 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button8.connect("toggled", self.on_arousal_toggled, "8")
        arousal_box.pack_start(a_button8, False, False, 0)

        a_button9 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button9.connect("toggled", self.on_arousal_toggled, "9")
        arousal_box.pack_start(a_button9, False, False, 0)
        return question5_box, arousal_image_box, arousal_box

    def __question6(self):
        # Question 4
        question6_box = Gtk.Box(spacing=120)
        question6 = Gtk.Label()
        text = "6- Dominance level: Submissive to Dominance (Controlled vs In-controlled)"
        question6.set_markup(FONT_STYLE.format(text))
        question6_box.pack_start(question6, False, False, 0)

        dominance_image_box = Gtk.Box(spacing=120)
        dominance_image = Gtk.Image.new_from_file('images/SAM-D-9-0.png')
        dominance_image_box.pack_start(dominance_image, False, False, 0)

        dominance_box = Gtk.Box(spacing=120)

        # Dominance Radio buttons
        d_button1 = Gtk.RadioButton.new_from_widget(None)
        d_button1.connect("toggled", self.on_dominance_toggled, 1)
        dominance_box.pack_start(d_button1, False, False, 45)

        d_button2 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button2.connect("toggled", self.on_dominance_toggled, "2")
        dominance_box.pack_start(d_button2, False, False, 0)

        d_button3 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button3.connect("toggled", self.on_dominance_toggled, "3")
        dominance_box.pack_start(d_button3, False, False, 0)

        d_button4 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button4.connect("toggled", self.on_dominance_toggled, "4")
        dominance_box.pack_start(d_button4, False, False, 0)

        d_button5 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button5.connect("toggled", self.on_dominance_toggled, "5")
        dominance_box.pack_start(d_button5, False, False, 0)
        d_button5.set_active(True)

        d_button6 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button6.connect("toggled", self.on_dominance_toggled, "6")
        dominance_box.pack_start(d_button6, False, False, 0)

        d_button7 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button7.connect("toggled", self.on_dominance_toggled, "7")
        dominance_box.pack_start(d_button7, False, False, 0)

        d_button8 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button8.connect("toggled", self.on_dominance_toggled, "8")
        dominance_box.pack_start(d_button8, False, False, 0)

        d_button9 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button9.connect("toggled", self.on_dominance_toggled, "9")
        dominance_box.pack_start(d_button9, False, False, 0)

        done_button = Gtk.Button.new_with_label("Done")
        done_button.connect("clicked", self.on_click_done_button)
        done_button.get_child().set_markup("<span font_desc='Tahoma 14'>Done</span>")
        return question6_box, dominance_image_box, dominance_box

    def on_emotion_toggled(self, button, name):
        if button.get_active():
            self.q1_answer = int(name)

    def on_q2_toggled(self, button, name):
        if button.get_active():
            self.q2_answer = int(name)

    def on_q3_toggled(self, button, name):
        if button.get_active():
            self.q3_answer = int(name)

    def on_valence_toggled(self, button, name):
        if button.get_active():
            self.valence_level = int(name)

    def on_arousal_toggled(self, button, name):
        if button.get_active():
            self.arousal_level = int(name)

    def on_dominance_toggled(self, button, name):
        if button.get_active():
            self.dominance_level = int(name)

    def on_click_done_button(self, button):
        self.save_answers()
        self.destroy()

    def save_answers(self):
        row = []
        row.append(self.stimuli_number)
        row.append(self.q1_answer)
        row.append(self.q2_answer)
        row.append(self.q3_answer)
        row.append(self.valence_level)
        row.append(self.arousal_level)
        row.append(self.dominance_level)
        with open(self.file_name, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()

    def show(self):
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

class ConversationQuestionnaire_first(Gtk.Window):
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

class ConversationQuestionnaire(Gtk.Window):
    def __init__(self, participant_number, stimuli_number):
        self.file_name = \
            "{}/after_stimuli/{}.csv".format(PATH, participant_number)
        self.stimuli_number = stimuli_number
        self.q1_answer = 5 # Neutral
        self.q2_answer = 3 # mean
        self.valence_level = 5 # middle
        self.arousal_level = 5 # middle
        self.dominance_level = 5 # middle
        Gtk.Window.__init__(self, title="Questionnaire")
        self.set_border_width(10)
        self.set_default_size(400, 200)
        grid = Gtk.Grid(column_homogeneous=False,
                        column_spacing=10,
                        row_spacing=10)
        self.add(grid)

        # ****************************** Question1 ****************************
        question1_box, question1_options_box = self.__question1()
        grid.attach(question1_box, 0, 1, 1, 1)
        grid.attach(question1_options_box, 0, 2, 1, 1)

        # **************************** Question 2 *****************************
        question2_box, question2_options_box = self.__question2()
        grid.attach(question2_box, 0, 3, 1, 1)
        grid.attach(question2_options_box, 0, 4, 1, 1)

        # ***************************** Question 3 ****************************
        question3_box, question3_options_box = self.__question3()
        grid.attach(question3_box, 0, 5, 1, 1)
        grid.attach(question3_options_box, 0, 6, 1, 1)

        # ***************************** Question 4 **********************8*****
        question4_box, valence_image_box, valence_box = self.__question4()
        grid.attach(question4_box, 0, 7, 1, 1)
        grid.attach(valence_image_box, 0, 8, 1, 1)
        grid.attach(valence_box, 0, 9, 1, 1)

        # ***************************** Question 5 **********************8*****
        question5_box, valence_image_box, valence_box = self.__question5()
        grid.attach(question5_box, 0, 10, 1, 1)
        grid.attach(valence_image_box, 0, 11, 1, 1)
        grid.attach(valence_box, 0, 12, 1, 1)

        done_button = Gtk.Button.new_with_label("Done")
        done_button.connect("clicked", self.on_click_done_button)
        done_button.get_child().set_markup(FONT_STYLE.format("Done"))
        grid.attach(done_button, 0, 14, 1, 1)

    def __question1(self):
        question1_box = Gtk.Box(spacing=120)
        question1 = Gtk.Label()
        text = "1- Which emotion did you feel during the conversation?"
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
        question3 = Gtk.Label()
        text = "3- Your Valence level: Negative to Positive"
        question3.set_markup(FONT_STYLE.format(text))
        question3_box.pack_start(question3, False, False, 0)

        valence_image_box = Gtk.Box(spacing=120)
        valence_image = Gtk.Image.new_from_file('images/SAM-V-9-0.png')
        valence_image_box.pack_start(valence_image, False, False, 0)

        valence_box = Gtk.Box(spacing=120)
        # Valence Radio buttons
        v_button1 = Gtk.RadioButton.new_from_widget(None)
        v_button1.connect("toggled", self.on_valence_toggled, "1")
        valence_box.pack_start(v_button1, False, False, 45)

        v_button2 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button2.connect("toggled", self.on_valence_toggled, "2")
        valence_box.pack_start(v_button2, False, False, 0)

        v_button3 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button3.connect("toggled", self.on_valence_toggled, "3")
        valence_box.pack_start(v_button3, False, False, 0)

        v_button4 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button4.connect("toggled", self.on_valence_toggled, "4")
        valence_box.pack_start(v_button4, False, False, 0)

        v_button5 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button5.connect("toggled", self.on_valence_toggled, "5")
        valence_box.pack_start(v_button5, False, False, 0)
        v_button5.set_active(True)

        v_button6 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button6.connect("toggled", self.on_valence_toggled, "6")
        valence_box.pack_start(v_button6, False, False, 0)

        v_button7 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button7.connect("toggled", self.on_valence_toggled, "7")
        valence_box.pack_start(v_button7, False, False, 0)

        v_button8 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button8.connect("toggled", self.on_valence_toggled, "8")
        valence_box.pack_start(v_button8, False, False, 0)

        v_button9 = Gtk.RadioButton.new_from_widget(v_button1)
        v_button9.connect("toggled", self.on_valence_toggled, "9")
        valence_box.pack_start(v_button9, False, False, 0)

        return question3_box, valence_image_box, valence_box

    def __question4(self):
        question4_box = Gtk.Box(spacing=120)
        question4 = Gtk.Label()
        text = "4- Your Arousal level: Calm to Excited"
        question4.set_markup(FONT_STYLE.format(text))
        question4_box.pack_start(question4, False, False, 0)

        arousal_image_box = Gtk.Box(spacing=120)
        arousal_image = Gtk.Image.new_from_file('images/SAM-A-9-0.png')
        arousal_image_box.pack_start(arousal_image, False, False, 0)

        arousal_box = Gtk.Box(spacing=120)

        # Arousal Radio buttons
        a_button1 = Gtk.RadioButton.new_from_widget(None)
        a_button1.connect("toggled", self.on_arousal_toggled, "1")
        arousal_box.pack_start(a_button1, False, False, 45)

        a_button2 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button2.connect("toggled", self.on_arousal_toggled, "2")
        arousal_box.pack_start(a_button2, False, False, 0)

        a_button3 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button3.connect("toggled", self.on_arousal_toggled, "3")
        arousal_box.pack_start(a_button3, False, False, 0)

        a_button4 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button4.connect("toggled", self.on_arousal_toggled, "4")
        arousal_box.pack_start(a_button4, False, False, 0)

        a_button5 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button5.connect("toggled", self.on_arousal_toggled, "5")
        arousal_box.pack_start(a_button5, False, False, 0)
        a_button5.set_active(True)

        a_button6 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button6.connect("toggled", self.on_arousal_toggled, "6")
        arousal_box.pack_start(a_button6, False, False, 0)

        a_button7 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button7.connect("toggled", self.on_arousal_toggled, "7")
        arousal_box.pack_start(a_button7, False, False, 0)

        a_button8 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button8.connect("toggled", self.on_arousal_toggled, "8")
        arousal_box.pack_start(a_button8, False, False, 0)

        a_button9 = Gtk.RadioButton.new_from_widget(a_button1)
        a_button9.connect("toggled", self.on_arousal_toggled, "9")
        arousal_box.pack_start(a_button9, False, False, 0)
        return question4_box, arousal_image_box, arousal_box

    def __question5(self):
        question5_box = Gtk.Box(spacing=120)
        question5 = Gtk.Label()
        text = "5- Dominance level: Submissive to Dominance (Controlled vs In-controlled)"
        question5.set_markup(FONT_STYLE.format(text))
        question5_box.pack_start(question5, False, False, 0)

        dominance_image_box = Gtk.Box(spacing=120)
        dominance_image = Gtk.Image.new_from_file('images/SAM-D-9-0.png')
        dominance_image_box.pack_start(dominance_image, False, False, 0)

        dominance_box = Gtk.Box(spacing=120)

        # Dominance Radio buttons
        d_button1 = Gtk.RadioButton.new_from_widget(None)
        d_button1.connect("toggled", self.on_dominance_toggled, 1)
        dominance_box.pack_start(d_button1, False, False, 45)

        d_button2 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button2.connect("toggled", self.on_dominance_toggled, "2")
        dominance_box.pack_start(d_button2, False, False, 0)

        d_button3 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button3.connect("toggled", self.on_dominance_toggled, "3")
        dominance_box.pack_start(d_button3, False, False, 0)

        d_button4 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button4.connect("toggled", self.on_dominance_toggled, "4")
        dominance_box.pack_start(d_button4, False, False, 0)

        d_button5 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button5.connect("toggled", self.on_dominance_toggled, "5")
        dominance_box.pack_start(d_button5, False, False, 0)
        d_button5.set_active(True)

        d_button6 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button6.connect("toggled", self.on_dominance_toggled, "6")
        dominance_box.pack_start(d_button6, False, False, 0)

        d_button7 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button7.connect("toggled", self.on_dominance_toggled, "7")
        dominance_box.pack_start(d_button7, False, False, 0)

        d_button8 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button8.connect("toggled", self.on_dominance_toggled, "8")
        dominance_box.pack_start(d_button8, False, False, 0)

        d_button9 = Gtk.RadioButton.new_from_widget(d_button1)
        d_button9.connect("toggled", self.on_dominance_toggled, "9")
        dominance_box.pack_start(d_button9, False, False, 0)

        done_button = Gtk.Button.new_with_label("Done")
        done_button.connect("clicked", self.on_click_done_button)
        done_button.get_child().set_markup("<span font_desc='Tahoma 14'>Done</span>")
        return question5_box, dominance_image_box, dominance_box

    def on_emotion_toggled(self, button, name):
        if button.get_active():
            self.q1_answer = int(name)

    def on_q2_toggled(self, button, name):
        if button.get_active():
            self.q2_answer = int(name)

    def on_q3_toggled(self, button, name):
        if button.get_active():
            self.q3_answer = int(name)

    def on_valence_toggled(self, button, name):
        if button.get_active():
            self.valence_level = int(name)

    def on_arousal_toggled(self, button, name):
        if button.get_active():
            self.arousal_level = int(name)

    def on_dominance_toggled(self, button, name):
        if button.get_active():
            self.dominance_level = int(name)

    def on_click_done_button(self, button):
        self.save_answers()
        self.destroy()

    def save_answers(self):
        row = []
        row.append(self.stimuli_number)
        row.append(self.q1_answer)
        row.append(self.q2_answer)
        row.append(self.valence_level)
        row.append(self.arousal_level)
        row.append(self.dominance_level)
        with open(self.file_name, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()

    def show(self):
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

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
