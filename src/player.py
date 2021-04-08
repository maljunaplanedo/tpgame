from .json_serializable import *
class Player(IJsonSerializable):
    def __init__(self, map_):
        self.gold = 500
        self.map = map_

    def get_info(self):
        info = {'gold': self.gold}
        return info

    def reset_from_info(self, info):
        self.gold = info['gold']
