from baseeffect import BaseEffect
import random


def get_random_colour():
	r = random.randint(0, 255)
	g = random.randint(0, 255)
	b = random.randint(0, 255)
	return r, g, b


class PingPongEffect(BaseEffect):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tick_rate = 0.01
		self.x = random.randint(1, self.matrix.width - 2)
		self.y = random.randint(1, self.matrix.height - 2)
		self.x_mod = random.choice([-1, 1])
		self.y_mod = random.choice([-1, 1])
		self.r, self.g, self.b = get_random_colour()
	
	def tick(self):
		# self.matrix.SetPixel(self.x, self.y, self.r, self.g, self.b)
		# self.x += self.x_mod
		# self.y += self.y_mod
		# if (self.x == 0 or self.x
		self.matrix.Clear()
		self.matrix.SetPixel(self.x, self.y, self.r, self.g, self.b)
		self.x += self.x_mod
		self.y += self.y_mod
		if self.x == 0 or self.x == self.matrix.width - 1:
			self.r, self.g, self.b = get_random_colour()
			self.x_mod *= -1
		if self.y == 0 or self.y == self.matrix.height - 1:
			self.r, self.g, self.b = get_random_colour()
			self.y_mod *= -1
		