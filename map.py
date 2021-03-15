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


class Solider:
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
