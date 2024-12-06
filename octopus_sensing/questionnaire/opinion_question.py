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
import gi
gi.require_version('Gtk', '3.0')  # nopep8
from gi.repository import Gtk  # nopep8
from typing import List, Union, Any

from octopus_sensing.questionnaire.question import Question

FONT_STYLE = "<span font_desc='Tahoma 16'>{}</span>"


class Option():
    '''
    The class for creating opinions

    Attributes
    ----------

    Parameters
    ----------

    id: int
        A unique ID for the opinion
    
    label: str
        The text of opinion
    
    value: Any
        The value of opinion

    '''

    def __init__(self, id: int, label: str="", value: Any=None):
        self.id = id
        self.label = label
        if self.label is None:
            self.label = str(id)
        self.value = value
        if self.value is None:
            self.value = id


class OpinionQuestion(Question):
    '''
    The class for creating opinion questions using Gtk 3.0


    Attributes
    ----------

    Parameters
    ----------
    id: str
        A unique ID for the question

    text: str
        The text of question
    
    options: Union[dict, int]

    image_path: str, default: None
        The path to an image which will be showed with the question.
    

    default_answer: Union[int, str], default: 0
        The default checked option
    '''
    def __init__(self, id: str, text: str, options: Union[dict, int],
                 image_path: str = "", default_answer: int = 0):
        super().__init__(id, text)

        self._options = []
        if isinstance(options, int):
            for i in range(options):
                option = Option(i, label=str(i), value=i)
                self._options.append(option)
        else:
            i = 0
            for key, value in options.items():
                option = Option(i, label=key, value=value)
                self._options.append(option)
                i += 1

        self._image_path = image_path
        self.answer = default_answer
    
    def render(self, grid: Gtk.Grid, grid_row: int):
        '''
        renders a question for adding to a questionnaire

        Parameters
        ----------
        grid: Gtk.Grid
            a Gtk grid object that this question will be added to it
            
        grid_row: int
            The row number of grid that the question will be added to it
        
        Returns
        -------
        row_counter: int
            The grid's row for adding the next object after adding this question
        
        Examples
        --------
        Creating an opinion question and adding it to the questionnaire

        >>> emotions = {"Happiness": 4, "Sadness": 6, "Neutral": 5, "Fear": 3, "Anger": 1}
        >>> question_1 = OpinionQuestion("q1",
        ...                              "1- What emotion did you feel the most?",
        ...                              options=emotions,
        ...                              default_answer=5)
        >>> questionnaire = Questionnaire("after_stimuli",
        ...                               "study01_p10",
        ...                               "stimuli00",
        ...                               "After Stimulus Questionnaire")
        >>> questionnaire.add_questions([question_1])

        See Also
        -----------
        :class:`octopus_sensing.questionnaire.questionnaire`

        '''

        row_counter = grid_row

        # Question box
        question_label_box = Gtk.Box(spacing=120)
        question_label = Gtk.Label()
        question_label.set_markup(FONT_STYLE.format(self._text))
        question_label_box.pack_start(question_label, False, False, 0)

        grid.attach(question_label_box, 0, row_counter, 1, 1)
        row_counter += 1

        # Image box
        image_box = None
        if self._image_path is not None:
            image_box = Gtk.Box(spacing=120)
            image = Gtk.Image.new_from_file(self._image_path)
            image_box.pack_start(image, False, False, 0)
            grid.attach(image_box, 0, row_counter, 1, 1)
            row_counter += 1

        # Options box
        options_box = Gtk.Box(spacing=120)
        option_buttons: List[Gtk.RadioButton] = []
        for i, option in enumerate(self._options):
            if i == 0:
                option_button = \
                    Gtk.RadioButton.new_with_label_from_widget(None, str(option.id))
            else:
                option_button = \
                    Gtk.RadioButton.new_with_label_from_widget(option_buttons[0],
                                                               str(option.id))
            option_button.connect("toggled",
                                  self.__on_option_button_toggled,
                                  option.value)
            option_button.get_child().set_markup(FONT_STYLE.format(option.label))
            option_buttons.append(option_button)
            options_box.pack_start(option_button, False, False, 0)
            if option.value == self.answer:
                option_button.set_active(True)
        grid.attach(options_box, 0, row_counter, 1, 1)
        row_counter += 1
        return row_counter

    def __on_option_button_toggled(self, button, name):
        if button.get_active():
            self.answer = name

    def get_answer(self) -> int:
        '''
        Gets selected answer

        Returns
        -------

        answer: int
            answer
        '''
        return self.answer
