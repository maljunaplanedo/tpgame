from abc import abstractmethod
import cairo
import math
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject


# Facade pattern
class GraphicsFacade:
    def __init__(self, window):
        self.window = window

    @abstractmethod
    def iteration(self):
        pass

    @abstractmethod
    def redraw(self):
        pass

    @abstractmethod
    def draw_ground(self, x1, y1, x2, y2):
        pass

    @abstractmethod
    def draw_squad(self, owner, x, y):
        pass

    @abstractmethod
    def draw_fortress(self, owner, x, y):
        pass


class GtkCairoFacade(GraphicsFacade):

    CELL_SIZE = 40
    LINE_HEIGHT = 40
    LINE_WIDTH = 640 / 3

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

    def draw_background(self):
        self.cr.set_source_rgb(1, 1, 1)
        self.cr.fill()

    def draw_ground(self, x1, y1, x2, y2):

        width = (x2 - x1 + 1) * self.CELL_SIZE
        height = (y2 - y1 + 1) * self.CELL_SIZE

        image_surface = cairo.ImageSurface.create_from_png('background.png')
        img_height = image_surface.get_height()
        img_width = image_surface.get_width()

        width_ratio = float(width) / float(img_width)
        height_ratio = float(height) / float(img_height)

        self.cr.save()
        self.cr.translate(x1 * self.CELL_SIZE, y1 * self.CELL_SIZE)
        self.cr.scale(width_ratio, height_ratio)
        self.cr.set_source_surface(image_surface)
        self.cr.paint()
        self.cr.restore()

    def draw_squad(self, owner, x, y):
        if owner == 1:
            self.cr.set_source_rgb(0, 0, 1)
        else:
            self.cr.set_source_rgb(1, 0, 0)

        self.cr.arc(x * self.CELL_SIZE + self.CELL_SIZE / 2,
                    y * self.CELL_SIZE + self.CELL_SIZE / 2,
                    self.CELL_SIZE / 2,
                    0, 2 * math.pi)
        self.cr.fill()

    def draw_fortress(self, owner, x, y):
        if owner == 1:
            self.cr.set_source_rgb(0, 0, 1)
        elif owner == 0:
            self.cr.set_source_rgb(1, 0, 0)
        else:
            self.cr.set_source_rgb(0, 0, 0)

        self.cr.rectangle(x * self.CELL_SIZE, y * self.CELL_SIZE,
                          self.CELL_SIZE, self.CELL_SIZE)
        self.cr.fill()

    def draw_line_background(self, col, row, is_selected):
        if is_selected:
            self.cr.set_source_rgb(1, 1, 1)
        else:
            self.cr.set_source_rgb(0, 0, 0)
        self.cr.rectangle(col * self.LINE_WIDTH, row * self.LINE_HEIGHT,
                          self.LINE_WIDTH, self.LINE_HEIGHT)

    def draw_line_text(self, col, row, text, pos):
        if pos == 0:
            self.cr.set_source_rgb(0, 1, 0)
        elif pos == 1:
            self.cr.set_source_rgb(1, 0, 0)
        elif pos == 2:
            self.cr.set_source_rgb(0, 0, 1)
        else:
            self.cr.set_source_rgb(1, 1, 0)

        self.cr.move_to(col * self.LINE_WIDTH + pos * self.LINE_WIDTH / 4,
                        row * self.LINE_HEIGHT)

        self.cr.show_text(text)


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
        self.screen.keyboard_event(key)
        self.redraw()

    @property
    def width(self):
        return self.WIDTH

    @property
    def height(self):
        return self.HEIGHT
