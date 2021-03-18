from map import Map
from network import Network
from graphics import Window


class Game:
    def __init__(self):
        self.map = Map(self)
        self.network = Network()
        self.window = Window(self)
        self.main_loop_running = False

    def run(self):
        self.network.check_file_data()
        self.main_loop_running = True
        while self.main_loop_running:
            self.window.iteration()
            self.network.iteration()

    def stop(self):
        self.main_loop_running = False
