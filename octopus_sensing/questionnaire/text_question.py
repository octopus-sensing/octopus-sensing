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
from typing import List, Union

from octopus_sensing.questionnaire.question import Question

FONT_STYLE = "<span font_desc='Tahoma 16'>{}</span>"


class TextQuestion(Question):
    '''
    The class for creating text questions using Gtk 3.0

    Attributes
    ----------

    Parameters
    ----------
    id: str
        A unique ID for the question
    
    text: str
        The text of question
    
    default_answer: Union[int, str], default: 0
        The default answer
    
    '''
    def __init__(self, id: str, text: str, default_answer: Union[int, str] = 0):
        super().__init__(id, text)

        self.answer_textbox = Gtk.Entry()
        self.answer_textbox.set_text(default_answer)

    def render(self, grid: Gtk.Grid, grid_row: int) -> int:
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
        Creating a text question and adding it to the questionnaire

        >>> question_1 = TextQuestion("q1",
        ...                           "1- What emotion did you feel the most?",
        ...                           default_answer="Happiness")
        >>> questionnaire = Questionnaire("after_stimuli",
        ...                               "study01_p10",
        ...                               "stimuli00",
        ...                               "After Stimulus Questionnaire")
        >>> questionnaire.add_question(question_1)

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

        # text box
        text_box = Gtk.Box(spacing=120)
        text_box.pack_start(self.answer_textbox, False, False, 0)
        grid.attach(text_box, 1, row_counter, 1, 1)
        row_counter += 1
        return row_counter

    def get_answer(self) -> Union[int, str]:
        '''
        Gets the answer

        Returns
        ----------
        answer: str or int
            answer
        '''
        return self.answer_textbox.get_text()
