# This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
# Copyright © Nastaran Saffaryazdi 2020
#
# Octopus Sensing is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
#  either version 3 of the License, or (at your option) any later version.
#
# Octopus Sensing is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Octopus Sensing.
# If not, see <https://www.gnu.org/licenses/>.

import os

from typing import List
import csv
import gi
gi.require_version('Gtk', '3.0')  # nopep8
from gi.repository import Gtk  # nopep8

from octopus_sensing.questionnaire.question import Question  # nopep8


class Questionnaire(Gtk.Window):
    '''
    Creating a questionnaire using Gtk
    It has a Done button which by clicking on it, the answers will be saved and window will be destroyed

    Attributes
    -----------

    Parameters
    ----------
    name: str
        Questionnaire name
    
    experiment_id: str
        The unique ID of the experiment

    stimulus_id: str
        The unique ID of the stimulus
    
    title: str
        Questionnaire title
    
    width: int, default: 400
        The width of questionnaire window in pixel
    
    height: int, default: 200
        The height of questionnaire window in pixel
    
    output_path: str
        The output path for recording answers
    
    Examples
    --------
    Creating an opinion question, a text question and adding it to the questionnaire

    >>> emotions = {"Happiness": 4, "Sadness": 6, "Neutral": 5, "Fear": 3, "Anger": 1}
    >>> question_1 = OpinionQuestion("q1",
    ...                              "1- What emotion did you feel the most?",
    ...                              options=emotions,
    ...                              default_answer=5)
    >>> question_2 = TextQuestion("q2",
    ...                           "1- Was your feelings positive or negative?",
    ...                           default_answer="Positive")
    >>> questionnaire = Questionnaire("after_stimuli",
    ...                               "study01_p10",
    ...                               "stimuli00",
    ...                               "After Stimulus Questionnaire")
    >>> questionnaire.add_questions([question_1, question_2])

    See Also
    -----------
    :class:`octopus_sensing.questionnaire.text_question`
    :class:`octopus_sensing.questionnaire.opinion_question`

    '''
    def __init__(self, name: str, experiment_id: str, stimulus_id: str,
                 title: str, width: int = 400, height: int = 200, output_path="output/self_report"):
        Gtk.Window.__init__(self, title=title)
        self.set_border_width(10)
        self.set_default_size(width, height)
        self._name = name
        self._questions: List[Question] = []
        self._experiment_id = experiment_id
        self.stimulus_id = stimulus_id
        self._output_path = output_path
        if not os.path.exists(self._output_path):
            os.mkdir(self._output_path)

    def add_question(self, question: Question) -> None:
        '''
        Adds a question to the questionnaire

        Parameters
        -----------
        question Question: a question
        '''
        assert isinstance(question, Question)
        if question.id in self._questions:
            raise RuntimeError(
                "The question ID {0} already exists in the questionnaire".format(question.id))
        self._questions.append(question)

    def add_questions(self, questions: List[Question]) -> None:
        '''
        Adds a list of questions to the questionnaire

        Parameters
        ----------
        questions: List(Question)
            a list of questions

        '''
        for question in questions:
            self.add_question(question)

    def show(self) -> None:
        '''
        Shows the questionnaire
        '''
        grid = Gtk.Grid(column_homogeneous=False,
                        column_spacing=10,
                        row_spacing=10)
        self.add(grid)
        i = 0
        for question in self._questions:
            row = question.render(grid, i)
            i += row
        done_button = Gtk.Button.new_with_label("Done")
        done_button.connect("clicked", self._on_click_done_button)
        done_button.get_child().set_markup("<span font_desc='Tahoma 14'>Done</span>")
        grid.attach(done_button, 0, i, 1, 1)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def _on_click_done_button(self, button: Gtk.Button) -> None:
        '''
        Saves answers and close the questionnaire

        Parameters
        ----------
        button: Gtk.Button
            by clicking this button, this method will call

        '''
        self._save_answers()
        self.destroy()

    def _save_answers(self) -> None:
        '''
        Saves answers
        '''
        file_name = \
            "{0}/{1}-{2}.csv".format(self._output_path,
                                     self._name,
                                     self._experiment_id)
        if not os.path.exists(file_name):
            csv_file = open(file_name, 'a')
            header = ["stimulus ID"]
            for question in self._questions:
                header.append(question.id)
            writer = csv.writer(csv_file)
            writer.writerow(header)
            csv_file.flush()
            csv_file.close()

        row = [self.stimulus_id]
        for question in self._questions:
            row.append(question.get_answer())

        with open(file_name, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(row)
