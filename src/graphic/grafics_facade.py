from abc import abstractmethod
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

    @abstractmethod
    def draw_background(self, black=False):
        pass

    @abstractmethod
    def draw_line_background(self, col, row, is_selected):
        pass

    @abstractmethod
    def draw_line_text(self, col, row, text, pos):
        pass

    @abstractmethod
    def draw_end_text(self, text):
        pass

    @abstractmethod
    def draw_panel_background(self):
        pass

    @abstractmethod
    def draw_gold(self, gold):
        pass

    @abstractmethod
    def draw_moves_left(self, moves):
        pass

    @abstractmethod
    def draw_target(self, row, col):
        pass




