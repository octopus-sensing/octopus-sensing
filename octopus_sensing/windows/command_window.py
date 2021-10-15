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

from screeninfo import get_monitors
from gi.repository import Gtk, GdkPixbuf, GLib, Gst, GObject
import datetime
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')


# Todo change it to config
monitors = get_monitors()
image_width = monitors[0].width
image_height = monitors[0].height


class CommandWindow(Gtk.Window):
    def __init__(self, message_image_path, title):
        print("new one")
        self._destroy = False
        Gtk.Window.__init__(self, title=title)
        self.set_default_size(400, 200)
        grid = Gtk.Grid(column_homogeneous=False,
                        column_spacing=30,
                        row_spacing=30)

        self._button = Gtk.Button.new_with_label("")
        self._button.connect("clicked", self.on_click_button)
        self._button.get_child().set_markup(
            "<span font_desc='Tahoma 40'>Start</span>")
        Gtk.Widget.set_size_request(self._button, 600, 300)
        grid.attach(self._button, 0, 0, 1, 1)
        self.add(grid)
        self.set_keep_above(True)

    # Displays Time

    def show_window(self):
        self.show_all()

    def on_click_button(self, button):
        print("destroy")
        self._destroy = True
        self.destroy()
