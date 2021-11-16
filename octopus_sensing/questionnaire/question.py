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


class Question:
    '''
    The base class for creating questions using Gtk 3.0

    Attributes
    ----------

    Parameters
    ----------
    id: str
        A unique ID for the question
    
    text: str
        The text of question
    '''
    def __init__(self, id: str, text: str):
        self._text = text
        self.id = id

    def render(self, grid: Gtk.Grid, grid_row: int):
        raise NotImplementedError()

    def get_answer(self):
        raise NotImplementedError()
