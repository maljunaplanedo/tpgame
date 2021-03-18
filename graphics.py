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
        self.gtk_window.default_size(self.window.WIDTH, self.window.HEIGHT)
        self.gtk_window.set_resizable(False)
        self.gtk_draw_area = Gtk.DrawingArea()
        self.gtk_draw_area.connect('draw', self.draw)
        self.gtk_draw_area.show()
        self.gtk_window.add(self.gtk_draw_area)
        self.gtk_window.present()
        self.cr = None

    def iteration(self):
        while Gtk.events_pending():
            Gtk.main_iteration()

    def close(self, event):
        self.window.close()

    def draw(self, widget, event):
        self.cr = self.gtk_draw_area.get_window().cairo_create()
        self.window.draw()

    def redraw(self):
        rect = self.gtk_draw_area.get_allocation()
        self.gtk_draw_area.get_window().invalidate_rect(rect, True)

    def draw_circle(self):
        self.cr.set_source_rgb(.5, .5, .5)
        self.cr.arc(50, 50, 50, 0, 2 * math.pi)
        self.cr.fill()


class Screen:

    def __init__(self, game):
        self.game = game

    def open_(self):
        self.game.window.change_screen(self)

    @abstractmethod
    def keyboard_event(self):
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
        self.graphics_facade.draw_circle()

    def keyboard_event(self, key):
        if self.screen is not None:
            self.screen.keyboard_event(key)
        self.redraw()
