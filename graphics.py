from abc import abstractmethod
import cairo
import math
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject


class GraphicsFacade:
    def __init__(self, window):
        self.window = window

    @abstractmethod
    def iteration(self):
        pass

    @abstractmethod
    def redraw(self):
        pass


class GtkCairoFacade(GraphicsFacade):
    def __init__(self, window):
        super().__init__(window)
        self.gtk_window = Gtk.Window()
        self.gtk_window.connect('destroy', self.close)
        self.gtk_window.set_default_size(self.window.WIDTH, self.window.HEIGHT)
        self.gtk_window.set_resizable(False)
        self.gtk_window.connect('key-press-event', self.keyboard_event)
        self.gtk_draw_area = Gtk.DrawingArea()
        self.gtk_draw_area.connect('draw', self.draw)
        self.gtk_draw_area.show()
        self.gtk_window.add(self.gtk_draw_area)
        self.gtk_window.present()
        self.cr = None

    def iteration(self):
        while Gtk.events_pending():
            Gtk.main_iteration()

    def keyboard_event(self, widget, event):
        key = Gdk.keyval_name(event.keyval)
        self.window.keyboard_event(key)

    def close(self, event):
        self.window.close()

    def draw(self, widget, event):
        self.cr = self.gtk_draw_area.get_window().cairo_create()
        self.window.draw()

    def redraw(self):
        rect = self.gtk_draw_area.get_allocation()
        self.gtk_draw_area.get_window().invalidate_rect(rect, True)


class Screen:

    def __init__(self, window):
        self.window = window

    def open_(self):
        self.window.change_screen(self)

    @abstractmethod
    def keyboard_event(self, key):
        pass

    @abstractmethod
    def draw(self):
        pass


class Window:
    WIDTH = 640
    HEIGHT = 480

    UsedGraphicsFacade = GtkCairoFacade

    def __init__(self, game):
        self.screen = None
        self.game = game
        self.graphics_facade = self.UsedGraphicsFacade(self)

    def iteration(self):
        self.graphics_facade.iteration()

    def redraw(self):
        self.graphics_facade.redraw()

    def change_screen(self, screen):
        self.screen = screen

    def close(self):
        self.game.stop()

    def draw(self):
        self.screen.draw()
        pass

    def keyboard_event(self, key):
        print(key)
        self.screen.keyboard_event(key)
        self.redraw()
