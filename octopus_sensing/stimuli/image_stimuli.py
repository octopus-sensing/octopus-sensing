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

import threading
from gi.repository import Gtk, Gst
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')

from octopus_sensing.windows.image_window import ImageWindow

Gst.init(None)
Gst.init_check(None)

def show_image_standalone(image_path, timeout, monitor_no=0):
    '''
    It may have some miliseconds delay to initialize GTK.
    If these miliseconds are important, don't use this method to display image

    Parameters
    ----------

    image_path: str
        The path of image
    
    timeout: int
        The time period for displaying the image
    
    monitor_no: int, default: 0
        The ID of monitor for displaying of image. It can be 0, 1, ...
    '''
    def gtk_main():
        image_window = ImageWindow(image_path, timeout, monitor_no=monitor_no)
        image_window.show_window()
        image_window.connect("destroy", Gtk.main_quit)
        Gtk.main()

    threading.Thread(target=gtk_main).start()