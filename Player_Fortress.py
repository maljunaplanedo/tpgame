class Player:
	def __init__(self):
		self.gold = 0


class Fortress:
	def __init__(self,game,x,y):
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

	def change_master(self,master):
		self.master = master

	def generate_shop(self):
		pass