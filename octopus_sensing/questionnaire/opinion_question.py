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
# You should have received a copy of the GNU General Public License along with Foobar.
# If not, see <https://www.gnu.org/licenses/>.
import gi
gi.require_version('Gtk', '3.0')  # nopep8
from gi.repository import Gtk  # nopep8
from typing import List

from octopus_sensing.questionnaire.question import Question

FONT_STYLE = "<span font_desc='Tahoma 16'>{}</span>"


class OpinionQuestion(Question):
    def __init__(self, id: str, text: str, data_range: int,
                 image_path: str = None, default_answer: int = 0):
        super().__init__(id, text)
        self._data_range = data_range
        self._image_path = image_path
        self.answer = default_answer

    def render(self, grid: Gtk.Grid, grid_row: int) -> int:
        '''
        renders a question for adding to a questionnaire

        @param Grid grid: a grid object that this question will add to it
        @param int grid_row: The row that the question will add

        @rtype: int
        @return: the grid's row for adding the next object after adding the question
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
        i = 0
        while i < self._data_range:
            if i == 0:
                option_button = \
                    Gtk.RadioButton.new_with_label_from_widget(None, i)
            else:
                option_button = \
                    Gtk.RadioButton.new_with_label_from_widget(option_buttons[0],
                                                               i)
            option_button.connect("toggled",
                                  self.__on_option_button_toggled,
                                  str(i))
            option_buttons.append(option_button)
            options_box.pack_start(option_buttons[i], False, False, 0)
            if i == self.answer:
                option_button.set_active(True)
            i += 1
        grid.attach(options_box, 0, row_counter, 1, 1)
        row_counter += 1
        return row_counter

    def __on_option_button_toggled(self, button, name):
        if button.get_active():
            self.answer = name

    def get_answer(self) -> int:
        '''
        Gets selected answer

        @rtype: int
        @return: answer
        '''
        return self.answer
