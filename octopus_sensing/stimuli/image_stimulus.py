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
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst

from octopus_sensing.windows import ImageWindow
from octopus_sensing.stimuli.stimulus import Stimulus

Gst.init(None)
Gst.init_check(None)

class ImageStimulus(Stimulus):
    '''
    Attributes
    -----------


    Parameters
    ----------
    id: str
        The id of stimulus

    path: str
        The path of image

    show_time: int
        The time period for displaying the image in seconds

    monitor_no: int, default: 0
        The ID of monitor for displaying of image. It can be 0, 1, ...
    '''

    def __init__(self, id: str, path: str, show_time: int, monitor_no:int =0):
        super().__init__(id, path)
        self._show_time = show_time
        self.image = ImageWindow(path, show_time, monitor_no=monitor_no)

    def show(self):
        '''
        If we have a main Gtk window and want to display image in it, we are using this
        method to display the image. Otherwise we use show_standalone method.
        '''
        self.image.show_window()

    def show_standalone(self):
        '''
        If we don't have a Gtk window and want to display it standalone, we are using this method.
        It may have some miliseconds delay to initialize GTK.
        If these miliseconds are important, don't use this method to display image

        '''
        def gtk_main():
            self.image.show_window()
            self.image.connect("destroy", Gtk.main_quit)
            Gtk.main()

        threading.Thread(target=gtk_main).start()
