from graphics import Screen
from graphics import Window
from map import Fortress
from map import Map


class FortressScreen(Screen):
    def __init__(self, window, fortress: Fortress):
        super().__init__(window)
        self.fortress = fortress
        self.selected_soldier = [self.fortress.guest, 0]

    def up_down_event(self, key):
        if key == 'w':
            new_index = min(0, self.selected_soldier[1] - 1)
        else:
            new_index = max(len(self.selected_soldier[0]) - 1, self.selected_soldier[1] + 1)
        self.selected_soldier[1] = new_index

    def right_left_event(self, key):
        new_squad = self.selected_soldier[0]
        if key == 'a':
            if new_squad == self.fortress.garrison:
                new_squad = self.fortress.guest
            elif new_squad == self.fortress.shop:
                new_squad = self.fortress.garrison
        else:
            if new_squad == self.fortress.guest:
                new_squad = self.fortress.garrison
            elif new_squad == self.fortress.garrison:
                new_squad = self.fortress.shop
        self.selected_soldier[0] = new_squad

    def equip_event(self):
        if self.selected_soldier[0] == self.fortress.shop:
            self.fortress.recruit_soldier(self.selected_soldier[1])
        else:
            self.fortress.move_soldier(
                                       self.selected_soldier[1],
                                       self.selected_soldier[0] == self.fortress.guest
                                       )

    def keyboard_event(self, key):
        if key in ['w', 's']:
            self.up_down_event(key)
        elif key in ['a', 'd']:
            self.right_left_event(key)
        elif key == 'e':
            self.equip_event()

    def draw(self):
        pass


class MapScreen(Screen):
    def __init__(self, window: Window, map_: Map):
        super().__init__(window)
        self.map = map_

    def movement_event(self, key):
        if key == 'w':
            movement = (0, -1)
        elif key == 'a':
            movement = (-1, 0)
        elif key == 's':
            movement = (0, 1)
        else:
            movement = (-1, 0)
        self.map.move_selected_squad(*movement)

    def change_squad_event(self, key):
        if key == 'Right':
            delta = 1
        else:
            delta = -1
        self.map.select_other_squad(delta)

    def keyboard_event(self, key):
        if key in ['w', 'a', 's', 'd']:
            self.movement_event(key)
        elif key in ['Left', 'Right']:
            self.change_squad_event(key)

    def draw(self):
        pass


class EndScreen(Screen):
    def __init__(self, window: Window):
        super().__init__(window)
        self.draw()

    def keyboard_event(self, key):
        pass

    def draw(self):
        pass
