import random

class Player:
    def __init__(self):
        self.gold = 0


class Fortress:
    def __init__(self, game, x, y):
        self.game = game
        self.garisson = None
        self.guest = None
        self.shop = []
        self.master = None
        self.x = x
        self.y = y
        self.generate_shop()

    def open_base_menu(self):
        pass

    def change_master(self, master):
        self.master = master

    def generate_shop(self):
        pass


class Map:
    FREEZE_TURN = -1
    PROTAGONIST_TURN = 0
    ANTAGONIST_TURN = 1

    WIDTH = 128
    HEIGHT = 128

    def __init__(self, game):
        self.game = game
        self.squads = []
        self.fortresses = []
        self.protagonist = Player()
        self.antagonist = Player()
        self.turn = -1
        self.selected_squad = None

        if game.network.is_host():
            self.generate_map()
            self.send_state()
        else:
            self.get_state()

    def move_selected_squad(self, dx, dy):
        self.selected_squad.move(dx, dy)
        x = self.selected_squad.x
        y = self.selected_squad.y

        squads_at_cell = self.squads_at_cell(x, y)
        fort_at_cell = self.forts_at_cell(x, y)

        if fort_at_cell:
            fort_at_cell[0].accept_visitor(self.selected_squad)
        elif len(squads_at_cell) == 2:
            squads_at_cell[0].interact(squads_at_cell[1])

        self.clear_squads()

    def add_squad(self, player, x, y):
        self.squads.append(Squad(player, x, y))

    def clear_squads(self):
        self.squads = [squad for squad in self.squads if not squad.empty()]

    def select_other_squad(self):
        index = self.squads.index(self.selected_squad)
        while self.squads[index].owner != self.protagonist:
            index = (index + 1) % len(self.squads)
        self.selected_squad = self.squads[index]

    def send_state(self):
        pass

    def get_state(self):
        pass

    def squads_at_cell(self, x, y):
        return [squad for squad in self.squads
                if squad.x == x and squad.y == y]

    def forts_at_cell(self, x, y):
        return [fort for fort in self.fortresses
                if fort.x == x and fort.y == y]

    def generate_map(self):
        self.add_squad(self.protagonist, 0, 0)
        self.add_squad(self.antagonist, self.WIDTH - 1, self.HEIGHT - 1)


class Soldier:
    def __init__(self, squad, armor, attack):
        self.squad = squad
        self.armor = armor
        self.attack = attack
        self.hp = 100


class Squad:
    def __init__(self, player, x, y):
        self.owner = player
        self.x = x
        self.y = y
        self.soldiers = []

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def fight(self, other):
        pass

    def invade_fortress(self, fortress):
        pass

    def __del__(self):
        self.soldiers.clear()
