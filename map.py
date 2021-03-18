import random
from network import INetworkEventSubscriber


class Player:
    def __init__(self):
        self.gold = 0


class Fortress:

    def __init__(self, game, x, y):
        self.game = game
        self.guest = None
        self.garrison = None
        self.shop = []
        self.master = None
        self.x = x
        self.y = y
        self.generate_shop()

    def open_fortress_menu(self):
        pass

    def change_master(self, master):
        self.master = master

    def generate_shop(self):
        pass

    def close_fortress_menu(self):
        pass

    def check_garrison_existence(self):
        if self.garrison.empty():
            self.garrison = None

    def accept_visitor(self, squad):
        if (self.master == self.game.map.antagonist
                and self.garrison is not None):

            squad.fight(self.garrison)
            self.check_garrison_existence()
            if squad.empty():
                return

        if self.garrison is None:
            self.garrison = Squad(self.game.map.protagonist, -1, -1)

        self.guest = squad
        self.open_fortress_menu()

    def throw_guest_away(self):
        self.check_garrison_existence()
        if not self.guest.empty():
            self.game.map.move_selected_squad(0, -1)
        self.guest = None
        self.close_fortress_menu()


class Map(INetworkEventSubscriber):
    WIDTH = 128
    HEIGHT = 128
    FORTRESSES_NUMBER = 12
    ONE_TURN_MOVES = 10

    def __init__(self, game):
        self.game = game
        self.squads = []
        self.fortresses = []
        self.protagonist = Player()
        self.antagonist = Player()
        self.turn = None
        self.selected_squad = None
        self.moves_left = 0

        self.game.network.subscribe('connect', self)
        self.game.network.subscribe('map_update', self)

    def handle_network_event(self, type_, event):
        self.game.window.redraw()
        pass

    def on_network_connected(self, event):
        if self.game.network.is_host():
            self.generate_map()
            self.send_state()

    def get_fort_by_garrison(self, squad):
        return [i for i in self.fortresses if i.garrison is squad][0]

    def move_selected_squad(self, dx, dy):
        if self.selected_squad.is_garrison():
            fort = self.get_fort_by_garrison(self.selected_squad)
            fort.open_fortress_menu()
            return

        self.selected_squad.move(dx, dy)
        x = self.selected_squad.x
        y = self.selected_squad.y

        squads_at_cell = self.squads_at_cell(x, y)
        fort_at_cell = self.forts_at_cell(x, y)

        if fort_at_cell:
            fort_at_cell[0].accept_visitor(self.selected_squad)
        elif len(squads_at_cell) == 2:
            other_squad = (squads_at_cell[0] if squads_at_cell[1]
                           is self.selected_squad else squads_at_cell[0])
            self.selected_squad.interact(other_squad)

        self.clear_squads()

        self.moves_left -= 1
        self.check_win()
        self.check_turn_end()

    def check_win(self):
        pass

    def check_turn_end(self):
        if not self.moves_left:
            self.start_turn(self.protagonist
                            if self.turn == self.antagonist
                            else self.antagonist)

    def add_squad(self, player, x, y):
        self.squads.append(Squad(player, x, y))

    def clear_squads(self):
        while self.selected_squad.empty():
            self.select_other_squad()
        self.squads = [squad for squad in self.squads if not squad.empty()]

    def select_other_squad(self):
        index = self.squads.index(self.selected_squad)
        while self.squads[index].owner != self.protagonist:
            index = (index + 1) % len(self.squads)
        self.selected_squad = self.squads[index]

    def send_state(self):
        pass

    def squads_at_cell(self, x, y):
        return [squad for squad in self.squads
                if squad.x == x and squad.y == y]

    def forts_at_cell(self, x, y):
        return [fort for fort in self.fortresses
                if fort.x == x and fort.y == y]

    def is_empty_cell(self, x, y):
        return (x in range(self.WIDTH) and y in range(self.HEIGHT) and
                not self.squads_at_cell(x, y) and
                not self.forts_at_cell(x, y))

    def start_turn(self, player):
        self.moves_left = self.ONE_TURN_MOVES
        self.turn = player

    def generate_map(self):
        self.add_squad(self.protagonist, 0, 0)
        self.squads[-1].add_soldier(Soldier(self.squads[-1]))

        self.add_squad(self.antagonist, self.WIDTH - 1, self.HEIGHT - 1)
        self.squads[-1].add_soldier(Soldier(self.squads[-1]))

        for i in range(self.FORTRESSES_NUMBER):
            fort_x, fort_y = -1, -1
            while True:
                fort_x = random.randrange(self.WIDTH)
                fort_y = random.randrange(self.HEIGHT)
                if (self.is_empty_cell(fort_x, fort_y) and
                        self.is_empty_cell(fort_x, fort_y - 1)):
                    break

            self.fortresses.append(Fortress(self.game, fort_x, fort_y))

        self.start_turn(self.protagonist if random.randrange(1)
                        else self.antagonist)


class Soldier:
    def __init__(self, squad, armor=0, attack=30):
        self.squad = squad
        self.armor = armor
        self.attack = attack
        self.hp = 100

    def alive(self):
        return self.hp > 0

    def fight(self, enemy):
        my_attack = self.attack * (100 - enemy.armor) // 100
        enemy_attack = enemy.attack * (100 - self.armor) // 100
        self.hp -= enemy_attack
        enemy.hp -= my_attack


class Squad:
    def __init__(self, player, x=-1, y=-1):
        self.player = player
        self.x = x
        self.y = y
        self.soldiers = []

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def add_soldier(self, soldier: Soldier):
        self.soldiers.append(soldier)

    def empty(self):
        return len(self.soldiers) == 0

    def update(self):
        self.soldiers = [soldier for soldier in self.soldiers if soldier.alive()]

    def size(self):
        return len(self.soldiers)

    def is_garrison(self) -> bool:
        return self.x == -1

    def fight(self, enemy):
        while (not self.empty()) and (not enemy.empty()):
            for i in range(min(self.size(), enemy.size())):
                self.soldiers[i].fight(enemy.soldiers[i])
            self.update()
            enemy.update()
        if self.empty():
            return 'Defeat'
        else:
            return 'Victory'

    def unite(self, friend_squad):
        self.soldiers += friend_squad.soldiers
        friend_squad.soldiers = []

    def interact(self, other):
        if self.player == other.player:
            self.unite(other)
        else:
            self.fight(other)
