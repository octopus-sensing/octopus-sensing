# This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
# Copyright © Zahra Saffaryazdi 2020
#
# Octopus Sensing is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
#  either version 3 of the License, or (at your option) any later version.
#
# Octopus Sensing is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Foobar.
# If not, see <https://www.gnu.org/licenses/>.

import gi
import csv
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

EMOTION_LIST = [ "anger", "disgust", "fear", "happy", "neutral", "sad","surprise", ]
PATH = "created_files"
FONT_STYLE = "<span font_desc='Tahoma 16'>{}</span>"

class AfterStimuliQuestionnaire(Gtk.Window):
    def __init__(self, participant_number, stimuli_number,
                 emotion=False, arousal=True, valence=True, dominance=True):
        self.file_name = \
            "{}/self_report/sam_{}.csv".format(PATH, participant_number)
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


        # ***************************** Question 1 ****************************
        question1_box, valence_image_box, valence_box = self.__question1()
        grid.attach(question1_box, 0, 1, 1, 1)
        grid.attach(valence_image_box, 0, 2, 1, 1)
        grid.attach(valence_box, 0, 3, 1, 1)

        # ***************************** Question 2 ****************************
        question2_box, arousal_image_box, arousal_box = self.__question2()
        grid.attach(question2_box, 0, 4, 1, 1)
        grid.attach(arousal_image_box, 0, 5, 1, 1)
        grid.attach(arousal_box, 0, 6, 1, 1)

        # ***************************** Question 3 **********************8*****
        question3_box, dominance_image_box, dominance_box = self.__question3()
        grid.attach(question3_box, 0, 7, 1, 1)
        grid.attach(dominance_image_box, 0, 8, 1, 1)
        grid.attach(dominance_box, 0, 9, 1, 1)

        done_button = Gtk.Button.new_with_label("Done")
        done_button.connect("clicked", self.on_click_done_button)
        done_button.get_child().set_markup(FONT_STYLE.format("Done"))
        grid.attach(done_button, 0, 10, 1, 1)

    def __question1(self):
        question1_box = Gtk.Box(spacing=100)
        question1 = Gtk.Label()
        text = "1- How positive was the emotion that you felt? (Neutral=5)"
        question1.set_markup(FONT_STYLE.format(text))
        question1_box.pack_start(question1, False, False, 0)

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

        return question1_box, valence_image_box, valence_box

    def __question2(self):
        question2_box = Gtk.Box(spacing=120)
        question2 = Gtk.Label()
        text = "2- What was your arousal level: Calm to Excited? (Neutral=5)"
        question2.set_markup(FONT_STYLE.format(text))
        question2_box.pack_start(question2, False, False, 0)

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
        return question2_box, arousal_image_box, arousal_box

    def __question3(self):
        # Question 3
        question3_box = Gtk.Box(spacing=120)
        question3 = Gtk.Label()
        text = "3- Dominance level: Submissive to Dominance (Controlled vs In-controlled)"
        question3.set_markup(FONT_STYLE.format(text))
        question3_box.pack_start(question3, False, False, 0)

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
        return question3_box, dominance_image_box, dominance_box

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
