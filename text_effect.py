from baseeffect import BaseEffect
from rgbmatrix import graphics


class TextEffect(BaseEffect):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.messages = []
		self.active_message = None
		self.font = graphics.Font()
		self.font.LoadFont("fonts/9x15B.bdf")
		self.x_offset = self.matrix.width
		self.y_offset = 2
		self.total_text_length = 0
		self.author_colour = graphics.Color(88, 101, 242)
		self.text_colour = graphics.Color(255, 255, 255)
	
	async def add_message(self, author, text):
		self.messages.append((author, text))
	
	def tick(self, canvas):
		if self.active_message is None and len(self.messages) > 0:
			self.active_message = self.messages.pop(0)
		if self.active_message is not None:
			author_length = graphics.DrawText(
				canvas, self.font, self.x_offset, self.y_offset,
				self.author_colour, f"{self.active_message[0]}: "
			)
			self.total_text_length = author_length + graphics.DrawText(
				canvas, self.font, self.x_offset + author_length, self.y_offset,
				self.text_colour, self.active_message[1]
			)
			self.x_offset -= 1
			if self.x_offset + self.total_text_length < 0:
				self.active_message = None
