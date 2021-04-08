from .json_serializable import *
from .soldier import *

class Squad(IJsonSerializable):
    def __init__(self, player, x=-1, y=-1):
        self.player = player
        self.x = x
        self.y = y
        self.soldiers = []

    def get_info(self):
        player = self.player.map.get_player_code(self.player)
        info = {'player': player,
                'x': self.x,
                'y': self.y,
                'soldiers': []}

        for i in self.soldiers:
            info['soldiers'].append(i.get_info())

        return info

    def __len__(self):
        return len(self.soldiers)

    def reset_from_info(self, info):
        self.x = info['x']
        self.y = info['y']
        self.soldiers = []

        for i in info['soldiers']:
            self.soldiers.append(Soldier(self))
            self.soldiers[-1].reset_from_info(i)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def add_soldier(self, soldier: Soldier):
        self.soldiers.append(soldier)

    def empty(self) -> bool:
        return len(self.soldiers) == 0

    def update(self):
        self.soldiers = [soldier for soldier in self.soldiers if soldier.alive()]

    def size(self) -> int:
        return len(self.soldiers)

    def is_garrison(self) -> bool:
        return self.x == -1

    def fight(self, enemy) -> bool:
        while (not self.empty()) and (not enemy.empty()):
            for i in range(min(self.size(), enemy.size())):
                self.soldiers[i].fight(enemy.soldiers[i])
            self.update()
            enemy.update()
        if self.empty():
            # Defeat
            return False
        else:
            # Victory
            return True

    def unite(self, friend_squad):
        self.soldiers += friend_squad.soldiers
        friend_squad.soldiers = []

    def interact(self, other):
        if self.player == other.player:
            self.unite(other)
        else:
            self.fight(other)
