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

    def __init__(self, game):
        self.game = game
        self.squads = []
        self.fortresses = []
        self.protagonist = Player()
        self.antagonist = Player()
        self.turn = -1

        if game.network.is_host():
            self.generate_map()
            self.send_state()
        else:
            self.get_state()

    def send_state(self):
        pass

    def get_state(self):
        pass

    def generate_map(self):
        pass


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
    def __init__(self, player=0, x=0, y=0):
        self.player = player
        self.x = x
        self.y = y
        self.soldiers = []

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def invade_fortress(self, fortress):
        if fortress.garisson:
            self.fight(fortress.garisson)

    def __del__(self):
        self.soldiers.clear()

    def add_soldier(self, soldier: Soldier):
        self.soldiers.append(soldier)

    def empty(self):
        return len(self.soldiers) == 0

    def update(self):
        self.soldiers = [soldier for soldier in self.soldiers if soldier.alive()]

    def size(self):
        return len(self.soldiers)

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

    def interact(self, other):
        if self.player == other.player:
            self.unite(other)
        else:
            self.fight(other)
