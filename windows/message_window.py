import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gtk, GdkPixbuf, GLib, Gst

from screeninfo import get_monitors
# Todo change it to config
monitors = get_monitors()
image_width =monitors[0].width
image_height =monitors[0].height

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
