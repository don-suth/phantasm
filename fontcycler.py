from layers.base_layer import BaseLayer
from rgbmatrix import graphics
import os

SHOWCASE_TEXT = "Hello, Unigames!"


class FontCycler(BaseLayer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fonts = []
		for filename in os.listdir("fonts"):
			if filename.endswith(".bdf"):
				self.fonts.append(filename)
		self.current_font = graphics.Font()
		self.x_offset = self.matrix.width
		self.y_offset = self.matrix.height - 10
		self.text_colour = graphics.Color(255, 0, 0)
		self.next_font()
		
	def next_font(self):
		if len(self.fonts) > 0:
			new_font = self.fonts.pop(0)
			print(new_font)
			self.current_font.LoadFont(f"fonts/{new_font}")
			self.x_offset = self.matrix.width
		else:
			self.done = True
			
	def tick(self, canvas):
		text_length = graphics.DrawText(
			canvas, self.current_font, self.x_offset, self.y_offset,
			self.text_colour, SHOWCASE_TEXT
		)
		self.x_offset -= 1
		if self.x_offset == 0:
			input()
		if self.x_offset + text_length < 0:
			self.next_font()
