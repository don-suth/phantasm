import asyncio
from rgbmatrix import FrameCanvas
from layers.base_layer import BaseLayer
from PIL import Image, ImageDraw


CONNECTED = (0, 255, 0)  # Pure Green
RECONNECTING = (255, 128, 0)  # Orange
FAILED = (255, 0, 0)  # Pure Red


class ConnectionStatusLayer(BaseLayer):
	"""
	This layer displays a status indicator dot in the lower right corner
	to display websocket connection status.
	This dot will display if there is something wrong with the connection,
	or if it only recently was (re)connected.
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.connection_status = FAILED
		self.sleep_task: asyncio.Task | None = None
		self.image = Image.new(mode="RGB", size=(2, 2))
		self.draw = ImageDraw.Draw(self.image)
		self.redraw_image()
		self.visible = True

	def redraw_image(self):
		self.draw.rectangle((0, 0, 1, 1), fill=self.connection_status, outline=self.connection_status)
		if self.sleep_task is not None:
			self.sleep_task.cancel()

	async def set_invisible_soon(self, delay: int = 5):
		await asyncio.sleep(delay)
		self.visible = False
		self.sleep_task = None

	async def set_connected(self):
		self.connection_status = CONNECTED
		self.visible = True
		self.redraw_image()
		self.sleep_task = asyncio.create_task(self.set_invisible_soon(delay=5))

	async def set_reconnecting(self):
		self.connection_status = RECONNECTING
		self.redraw_image()
		self.visible = True

	async def set_failed(self):
		self.connection_status = FAILED
		self.redraw_image()
		self.visible = True

	def tick(self, canvas: FrameCanvas, frame_x_offset: int = 0, frame_y_offset: int = 0):
		if self.visible:
			# Set the pixel in the bottom right to the current status colour
			canvas.SetImage(self.image, canvas.width + frame_x_offset - 2, canvas.height + frame_y_offset - 2)
		else:
			# If invisible, just skip the drawing entirely.
			pass
		return self

