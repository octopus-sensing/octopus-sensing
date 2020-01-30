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

class MessageWindow(Gtk.Window):
    def __init__(self, image_path):
        Gtk.Window.__init__(self, title="")

        self.set_default_size(400, 200)
        grid = Gtk.Grid(column_homogeneous=False,
                        column_spacing=30,
                        row_spacing=30)

        self.add(grid)
        image_box = Gtk.Box()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        image_box.pack_start(image, False, False, 0)
        grid.attach(image_box, 0, 0, 1, 1)

        continue_button = Gtk.Button.new_with_label("Continue")
        continue_button.connect("clicked", self.on_click_continue_button)
        continue_button.get_child().set_markup("<span font_desc='Tahoma 14'>Continue</span>")
        grid.attach(continue_button, 0, 1, 1, 1)

        self.modal = True
        #self.fullscreen()

        image_box.show()
        image.show()

    def show_window(self):
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def on_click_continue_button(self, button):
        self.destroy()
