from graphics import Screen
from graphics import Window
import mapobj


class FortressScreen(Screen):
    def __init__(self, window, fortress):
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
    WINDOW_CELL_WIDTH = 16
    WINDOW_CELL_HEIGHT = 12

    def __init__(self, window: Window, map_):
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
        if self.map.turn is None:
            pass

        if self.map.selected_squad.is_garrison():
            fort = self.map.get_fort_by_garrison(self.map.selected_squad)
            camera_x = fort.x
            camera_y = fort.y
        else:
            camera_x = self.map.selected_squad.x
            camera_y = self.map.selected_squad.y

        diff_x = camera_x - self.WINDOW_CELL_WIDTH // 2 + 1
        diff_y = camera_y - self.WINDOW_CELL_HEIGHT // 2 + 1

        self.window.graphics_facade.draw_ground(-diff_x, -diff_y,
                                                self.map.WIDTH - diff_x,
                                                self.map.HEIGHT - diff_y)

        for i in self.map.fortresses:
            player_code = self.map.get_player_code(i.master)
            self.window.graphics_facade.draw_fortress(player_code,
                                                      i.x - diff_x,
                                                      i.y - diff_y)

        for i in self.map.squads:
            player_code = self.map.get_player_code(i.player)
            if not i.is_garrison():
                self.window.graphics_facade.draw_squad(player_code,
                                                       i.x - diff_x,
                                                       i.y - diff_y)


class EndScreen(Screen):
    def __init__(self, window: Window, result: int):
        super().__init__(window)
        self.result = result

    def keyboard_event(self, key):
        pass

    def draw(self):
        pass
