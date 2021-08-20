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

from gi.repository import Gtk, GdkPixbuf, GLib, Gst
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')


class MessageWindow(Gtk.Window):
    def __init__(self, message_image_path):
        Gtk.Window.__init__(self, title="")

        self.set_default_size(400, 200)
        grid = Gtk.Grid(column_homogeneous=False,
                        column_spacing=30,
                        row_spacing=30)

        self.add(grid)
        image_box = Gtk.Box()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(message_image_path)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        image_box.pack_start(image, False, False, 0)
        grid.attach(image_box, 0, 0, 1, 1)

        continue_button = Gtk.Button.new_with_label("Start")
        continue_button.connect("clicked", self.on_click_continue_button)
        continue_button.get_child().set_markup("<span font_desc='Tahoma 14'>Continue</span>")
        grid.attach(continue_button, 0, 1, 1, 1)

        self.modal = True
        # self.fullscreen()

        image_box.show()
        image.show()

    def show_window(self):
        self.show_all()

    def on_click_continue_button(self, button):
        self.destroy()
