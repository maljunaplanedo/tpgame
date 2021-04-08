from abc import abstractmethod
from .gtk_facade import * 


# Screen is class for Screen events ( like fortress menu , win screen, lose screen)
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

    def keyboard_event(self, key):
        self.screen.keyboard_event(key)
        self.redraw()

    @property
    def width(self):
        return self.WIDTH

    @property
    def height(self):
        return self.HEIGHT
