from baseeffect import BaseEffect
import random
from PIL import Image, ImageDraw


def get_random_colour():
	r = random.randint(0, 255)
	g = random.randint(0, 255)
	b = random.randint(0, 255)
	return r, g, b


class PingPongEffect(BaseEffect):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ball_width = 2
		self.ball_height = 2
		self.x = random.randint(1, self.matrix.width - self.ball_width - 1)
		self.y = random.randint(1, self.matrix.height - self.ball_height - 1)
		self.x_mod = random.choice([-1, 1])
		self.y_mod = random.choice([-1, 1])
		self.r, self.g, self.b = get_random_colour()
		
		self.image = Image.new("RGB", (self.ball_width, self.ball_height))
		self.draw = ImageDraw.Draw(self.image)
		self.redraw_image()
	
	def redraw_image(self):
		if (self.r, self.g, self.b) == (0, 0, 0):
			self.done = True
			print("Goodbye cruel world!")
		self.draw.rectangle(xy=(0, 0, self.ball_width - 1, self.ball_height - 1), fill=(self.r, self.g, self.b))
	
	def tick(self, canvas):
		# self.matrix.SetPixel(self.x, self.y, self.r, self.g, self.b)
		# self.x += self.x_mod
		# self.y += self.y_mod
		# if (self.x == 0 or self.x
		canvas.SetImage(self.image, self.x, self.y)
		self.x += self.x_mod
		self.y += self.y_mod
		if self.x == 0 or self.x + self.ball_width - 1 == self.matrix.width - 1:
			self.r, self.g, self.b = get_random_colour()
			self.redraw_image()
			self.x_mod *= -1
		if self.y == 0 or self.y + self.ball_height - 1 == self.matrix.height - 1:
			self.r, self.g, self.b = get_random_colour()
			self.redraw_image()
			self.y_mod *= -1
