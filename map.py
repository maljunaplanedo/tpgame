class Map:
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
