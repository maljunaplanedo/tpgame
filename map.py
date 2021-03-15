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
