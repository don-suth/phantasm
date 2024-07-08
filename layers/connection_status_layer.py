import asyncio
from base_layer import BaseLayer
from PIL import Image, ImageDraw


CONNECTED = (0, 255, 0)  # Pure Green
RECONNECTING = (255, 128, 0)  # Orange
FAILED = (255, 0, 0)  # Pure Red


class ConnectionStatusLayer(BaseLayer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.connection_status = FAILED
		self.sleep_task: asyncio.Task | None = None
		self.image = Image.new(mode="RGB", size=(1, 1))
		self.draw = ImageDraw.Draw(self.image)
		self.visible = True

	def redraw_image(self):
		self.draw.point((0, 0), fill=self.connection_status)

	async def set_invisible_soon(self, delay: int = 5):
		try:
			await asyncio.sleep(delay)
			self.visible = False
			self.sleep_task = None
		except asyncio.CancelledError:
			pass

	async def set_connected(self):
		self.connection_status = CONNECTED
		self.redraw_image()
		if self.sleep_task is not None:
			self.sleep_task.cancel()
		self.sleep_task = asyncio.create_task(self.set_invisible_soon(delay=5))

	async def set_reconnecting(self):
		self.connection_status = RECONNECTING
		self.redraw_image()
		self.visible = True

	async def set_failed(self):
		self.connection_status = FAILED
		self.redraw_image()
		self.visible = True

	def tick(self, canvas):
		if self.visible:
			# Set the pixel in the bottom right to the current status colour
			canvas.SetImage(self.image, canvas.width - 1, canvas.height - 1)
		else:
			# If invisible, just skip the drawing entirely.
			pass

