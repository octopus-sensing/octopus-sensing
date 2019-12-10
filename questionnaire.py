import gi
import csv
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Questionnaire(Gtk.Window):
    def __init__(self, participant_number, stimuli_number):
        self.file_name = "created_files/answers/p-{0}-answers.csv".format(participant_number)
        self.stimuli_number = stimuli_number
        self.valence_level = 5
        self.arousal_level = 5
        self.dominance_level = 5
        self.emotion = 5 # Neutral
        Gtk.Window.__init__(self, title="Questionnaire")
        self.set_border_width(10)
        self.set_default_size(400, 200)
        grid = Gtk.Grid(column_homogeneous=False,
                        column_spacing=10,
                        row_spacing=10)
        self.add(grid)

        # Question1
        question1_box = Gtk.Box(spacing=120)
        question1 = Gtk.Label()
        text = "1- Which one describe your emotional state more accurately?"
        question1.set_markup("<span font_desc='Tahoma 12'>%s</span>" % text)
        question1_box.pack_start(question1, False, False, 0)

        # emotion radio buttons
        grid.attach(question1_box, 0, 1, 1, 1)

        emotion_box = Gtk.Box(spacing=80)
        grid.attach(emotion_box, 0, 2, 1, 1)

        # emotion Radio buttons
        happy = Gtk.RadioButton.new_with_label_from_widget(None, "Happy")
        happy.connect("toggled", self.on_emotion_toggled, "4")
        emotion_box.pack_start(happy, False, False, 45)

        sad = Gtk.RadioButton.new_with_label_from_widget(happy, "Sad")
        sad.connect("toggled", self.on_emotion_toggled, "6")
        emotion_box.pack_start(sad, False, False, 0)

        neutral = Gtk.RadioButton.new_with_label_from_widget(happy, "Neutral")
        neutral.connect("toggled", self.on_emotion_toggled, "5")
        emotion_box.pack_start(neutral, False, False, 0)
        neutral.set_active(True)

        fear = Gtk.RadioButton.new_with_label_from_widget(happy, "Fear")
        fear.connect("toggled", self.on_emotion_toggled, "3")
        emotion_box.pack_start(fear, False, False, 0)

        angry = Gtk.RadioButton.new_with_label_from_widget(happy, "Angry")
        angry.connect("toggled", self.on_emotion_toggled, "1")
        emotion_box.pack_start(angry, False, False, 45)

        disgust = Gtk.RadioButton.new_with_label_from_widget(happy, "Disgust")
        disgust.connect("toggled", self.on_emotion_toggled, "2")
        emotion_box.pack_start(disgust, False, False, 45)

        # Question 2
        question2_box = Gtk.Box(spacing=100)
        question2 = Gtk.Label()
        text = "2- Your Valence level: Negative to Positive"
        question2.set_markup("<span font_desc='Tahoma 12'>%s</span>" % text)
        question2_box.pack_start(question2, False, False, 0)
        grid.attach(question2_box, 0, 3, 1, 1)

        valence_image_box = Gtk.Box(spacing=120)
        valence_image = Gtk.Image.new_from_file('images/SAM-V-9-0.png')
        valence_image_box.pack_start(valence_image, False, False, 0)
        grid.attach(valence_image_box, 0, 4, 1, 1)

        valence_box = Gtk.Box(spacing=120)
        grid.attach(valence_box, 0, 5, 1, 1)
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


        # Question 3
        question3_box = Gtk.Box(spacing=120)
        question3 = Gtk.Label()
        text = "3- Your Arousal level: Calm to Excited"
        question3.set_markup("<span font_desc='Tahoma 12'>%s</span>" % text)
        question3_box.pack_start(question3, False, False, 0)
        grid.attach(question3_box, 0, 6, 1, 1)

        arousal_image_box = Gtk.Box(spacing=120)
        arousal_image = Gtk.Image.new_from_file('images/SAM-A-9-0.png')
        arousal_image_box.pack_start(arousal_image, False, False, 0)
        grid.attach(arousal_image_box, 0, 7, 1, 1)

        arousal_box = Gtk.Box(spacing=120)
        grid.attach(arousal_box, 0, 8, 1, 1)

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

        # Question 4
        question4_box = Gtk.Box(spacing=120)
        question4 = Gtk.Label()
        text = "4- Dominance level: Submissive to Dominance (Controlled vs In-controlled)"
        question4.set_markup("<span font_desc='Tahoma 12'>%s</span>" % text)
        question4_box.pack_start(question4, False, False, 0)
        grid.attach(question4_box, 0, 9, 1, 1)

        dominance_image_box = Gtk.Box(spacing=120)
        dominance_image = Gtk.Image.new_from_file('images/SAM-D-9-0.png')
        dominance_image_box.pack_start(dominance_image, False, False, 0)
        grid.attach(dominance_image_box, 0, 10, 1, 1)

        dominance_box = Gtk.Box(spacing=120)
        grid.attach(dominance_box, 0, 11, 1, 1)

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
        grid.attach(done_button, 0, 12, 1, 1)

    def on_emotion_toggled(self, button, name):
        if button.get_active():
            self.emotion = int(name)

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
        row.append(self.emotion)
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

#win = Questionnaire(1,2)
#win.connect("destroy", Gtk.main_quit)
#win.show_all()
#Gtk.main()
