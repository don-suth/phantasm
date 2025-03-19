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
		self.message = ""
		self.font = graphics.Font()
		self.font.LoadFont("fonts/9x15B.bdf")
		self.alert_bg_colour = (255, 0, 0)  # Red
		self.alert_fg_colour = (255, 255, 255)  # White
		self.image = Image.new(mode="RGB", size=(64, 32))
		self.draw = ImageDraw.Draw(self.image)
		self.flashing = True
		self.flash_border = 1
		self.redraw_image()

	def redraw_image(self):
		self.draw.rectangle(xy=(0, 0, 63, 31), fill=None, outline=self.alert_bg_colour, width=self.flash_border)

	def tick(self, canvas: FrameCanvas):
		if self.flashing is True:
			canvas.SetImage(self.image, 0, 0)
			self.flash_border += 1
			self.redraw_image()
		if self.flash_border == 100:
			self.done = True



