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
from gi.repository import Gtk, GdkPixbuf, GLib, Gst
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')


Gst.init(None)
Gst.init_check(None)


class ImageWindow(Gtk.Window):
    '''
    Creates a Gtk window with a message for informing the participant about something
    It has a continue button which by clicking on it, the window will be destroyed

    Attributes
    ----------

    Parameters
    ----------

    image_path: str
        The path of image
    
    timeout: int
        The time period for displaying the image
    
    monitor_no: int, default: 0
        The ID of monitor for displaying of image. It can be 0, 1, ...

    '''
    def __init__(self, image_path, timeout, monitor_no=0):
        Gtk.Window.__init__(self, title="")

        self._timeout = timeout
        image_box = Gtk.Box()
        monitors = get_monitors()
        image_width = monitors[monitor_no].width
        image_height = monitors[monitor_no].height
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            image_path, image_width, image_height, False)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        image_box.pack_start(image, False, False, 0)
        self.add(image_box)

        self.modal = True
        self.fullscreen()
        
        image_box.show()
        image.show()

    def show_window(self):
        GLib.timeout_add_seconds(self._timeout, self.destroy)
        self.show()

