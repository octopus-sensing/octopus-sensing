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

FONT_STYLE = "<span font_desc='Tahoma 18'>{}</span>"

class MessageWindow(Gtk.Window):

    '''
    Creating a message window using Gtk
    It has a button which by clicking on it, The window will be closed

    Attributes
    -----------

    Parameters
    ----------
    title: str
        Window title
    
    message: str
        The message text
    
    width: int, default: 500
        The width of questionnaire window in pixel
    
    height: int, default: 200
        The height of questionnaire window in pixel

    '''
    def __init__(self, title: str, message: str, button_label: str = "Ok",
                 width: int = 500, height: int = 200):
        Gtk.Window.__init__(self, title=title)
        self.set_border_width(10)
        self.set_default_size(width, height)
        self._message = message
        self._width = width
        self._height = height
        self._button_label = button_label


    def show(self) -> None:
        '''
        Shows the message
        '''
        grid = Gtk.Grid(column_homogeneous=False,
                        column_spacing=10,
                        row_spacing=10)
        self.add(grid)

        message_label_box = Gtk.Box(spacing=120)
        message_label = Gtk.Label()
        message_label.set_markup(FONT_STYLE.format(self._message))
        Gtk.Widget.set_size_request(message_label, self._width, (self._height - 50))
        message_label_box.pack_start(message_label, False, False, 0)

        grid.attach(message_label_box, 0, 0, 1, 1)


        ok_button = Gtk.Button.new_with_label("Ok")
        ok_button.connect("clicked", self._on_click_ok_button)
        ok_button.get_child().set_markup("<span font_desc='Tahoma 14'>{}</span>".format(self._button_label))
        Gtk.Widget.set_size_request(ok_button, self._width, 50)
        grid.attach(ok_button, 0, 1, 1, 1)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def _on_click_ok_button(self, button: Gtk.Button) -> None:
        '''
        Close the message dialog

        Parameters
        ----------
        button: Gtk.Button
            by clicking this button, this method will be called

        '''
        self.destroy()