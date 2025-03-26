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

		self.alert_bg_colour = (255, 0, 0)  # Red
		self.alert_fg_colour = (255, 255, 255)  # White
		self.image = Image.new(mode="RGB", size=(64, 32))
		self.draw = ImageDraw.Draw(self.image)
		self.flashing = True
		self.flash_border = 1

		self.x_offset = 0
		self.scrolling = False

		self.location_x_offset = 0
		self.text_change_task = asyncio.create_task(self.text_changer())
		self.location_change_task = asyncio.create_task(self.location_changer())

		self.meta_scrolling = True
		self.meta_x_offset = 64

	def redraw_image(self):
		self.draw.rectangle(xy=(0, 0, 63, 31), fill=None, outline=self.alert_bg_colour, width=self.flash_border)

	async def text_changer(self):
		text_strings = [
			"Jarl Vetreiði", "áàãâä éèêë íìîï óòõôö úùûü ç ñ", "日本語"
		]
		while True:
			for text in text_strings:
				self.message = text
				if len(text) * 6 > 64:
					self.x_offset = 63
					self.scrolling = True
				else:
					self.x_offset = (64 - (len(text) * 6)) // 2
					self.scrolling = False
				await asyncio.sleep(5)

	async def location_changer(self):
		locations = [
			"Tav", "Guild",
		]
		while True:
			for location in locations:
				self.location = location
				self.location_x_offset = (64 - (len(location) * 10)) // 2
				await asyncio.sleep(5)

	def tick(self, canvas: FrameCanvas):
		if self.meta_scrolling:
			for x in range(self.meta_x_offset, 64):
				for y in range(0, 32):
					canvas.SetPixel(x, y, 0, 0, 0)
		else:
			canvas.Clear()

		graphics.DrawText(
			canvas, self.small_font, self.x_offset + self.meta_x_offset, 10, graphics.Color(255, 255, 255),
			text=self.message,
		)
		graphics.DrawText(
			canvas, self.font, self.location_x_offset + self.meta_x_offset, 25, graphics.Color(255, 255, 255),
			text=self.location
		)
		graphics.DrawText(
			canvas, self.smaller_font, 8 + self.meta_x_offset, 32, graphics.Color(255, 255, 0),
			text="ENTRANCE"
		)
		if self.scrolling:
			self.x_offset -= 1
		if self.meta_scrolling:
			self.meta_x_offset -= 1
			if self.meta_x_offset == 0:
				self.meta_scrolling = False

# graphics.DrawText(
#	canvas, self.font, 7, 13, graphics.Color(255,255,255), text="Ring"
# )
# graphics.DrawText(
#	canvas, self.font, 18, 27, graphics.Color(255, 255, 255), text="Ring!"
# )
