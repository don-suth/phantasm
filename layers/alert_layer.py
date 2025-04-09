import asyncio
from layers.base_layer import BaseLayer
from rgbmatrix import graphics, FrameCanvas
from PIL import Image, ImageDraw


class AlertLayer(BaseLayer):
	"""
	Initially flashes the display, then displays text for 30 seconds.
	Flashes the display by expanding a rectangle out from the edges
	of the display.
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.message = "???"
		self.location = "???"

		self.font = graphics.Font()
		self.font.LoadFont("fonts/10x20.bdf")
		self.small_font = graphics.Font()
		self.small_font.LoadFont("fonts/6x13.bdf")
		self.smaller_font = graphics.Font()
		self.smaller_font.LoadFont("fonts/6x9.bdf")

		self.message_width = 0
		self.message_x_offset = 0
		self.message_scrolling = False
		self.message_wrap = False

		self.location_x_offset = 0
		self.text_change_task = asyncio.create_task(self.text_changer())
		self.location_change_task = asyncio.create_task(self.location_changer())


	async def text_changer(self):
		text_strings = [
			"Jarl Vetreiði", "áàãâä éèêë íìîï óòõôö úùûü ç ñ", "日本語"
		]
		while True:
			for text in text_strings:
				self.message = text
				self.message_width = len(text) * 6
				if self.message_width > 64:
					self.message_x_offset = 63
					self.message_scrolling = True
					self.message_wrap = True
				else:
					self.message_x_offset = (64 - (len(text) * 6)) // 2
					self.message_scrolling = False
				await asyncio.sleep(30)

	async def location_changer(self):
		locations = [
			"Tav", "Guild",
		]
		while True:
			for location in locations:
				self.location = location
				self.location_x_offset = (64 - (len(location) * 10)) // 2
				await asyncio.sleep(5)

	def tick(self, canvas: FrameCanvas, frame_x_offset: int = 0, frame_y_offset: int = 0):
		# Draw the message
		graphics.DrawText(
			canvas, self.small_font, self.message_x_offset + frame_x_offset, frame_y_offset + 10, graphics.Color(255, 255, 255),
			text=self.message,
		)

		# If the message is wrapped, draw it again behind it
		if self.message_wrap:
			graphics.DrawText(
				canvas, self.small_font, self.message_x_offset + frame_x_offset + self.message_width + 20, frame_y_offset + 10,
				graphics.Color(255, 255, 255),
				text=self.message,
			)

		# Draw the location
		graphics.DrawText(
			canvas, self.font, self.location_x_offset + frame_x_offset, frame_y_offset + 25, graphics.Color(255, 255, 255),
			text=self.location
		)

		# Draw the word "ENTRANCE"
		graphics.DrawText(
			canvas, self.smaller_font, 8 + frame_x_offset, frame_y_offset + 32, graphics.Color(255, 255, 0),
			text="ENTRANCE"
		)

		# Scroll the text to the left
		if self.message_scrolling:
			self.message_x_offset -= 1

			# If the text is wrapped, stop it scrolling once the second instance
			# reaches the left edge
			if self.message_wrap:
				if self.message_x_offset == -self.message_width - 20:
					self.message_scrolling = False

		return self
