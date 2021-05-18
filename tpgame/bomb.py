from tpgame.json_serializable import IJsonSerializable
from tpgame.soldier import Soldier


class Bomb(Soldier, IJsonSerializable):
    DEF_ATTACK = 150
    DEF_COST = 100

    def __init__(self):
        super().__init__(attack=150, armor=-1, hp=1)
        self.cost = self.DEF_COST
        pass
