import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gtk, GdkPixbuf, GLib, Gst

from screeninfo import get_monitors
monitors = get_monitors()
image_width =monitors[0].width
image_height =monitors[0].height

Gst.init(None)
Gst.init_check(None)

class ImageWindow(Gtk.Window):
    def __init__(self, image_path, timeout):
        Gtk.Window.__init__(self, title="")

        self._timeout = timeout
        image_box = Gtk.Box()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, image_width,image_height, False)
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
