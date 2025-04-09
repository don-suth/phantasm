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

	def __init__(
			self,
			*args,
			message: str = "",
			location: str = "",
			message_time: int = 30,
			**kwargs,
	):
		super().__init__(*args, **kwargs)
		self.message = message
		self.location = location
		self.message_time = message_time

		# Load and set-up fonts
		self.font = graphics.Font()
		self.font.LoadFont("fonts/10x20.bdf")
		self.small_font = graphics.Font()
		self.small_font.LoadFont("fonts/6x13.bdf")
		self.smaller_font = graphics.Font()
		self.smaller_font.LoadFont("fonts/6x9.bdf")

		# Position initial message text
		self.message_width = len(self.message) * 6
		if self.message_width > 64:
			self.message_x_offset = 63
			self.message_scrolling = True
			self.message_wrap = True
		else:
			self.message_x_offset = (64 - self.message_width) // 2
			self.message_scrolling = False
			self.message_wrap = False

		# Position initial location text
		self.location_x_offset = (64 - (len(location) * 10)) // 2

		# Start the countdown for the layer vanishing
		self.completion_task = asyncio.create_task(self.delay_completion())

	async def delay_completion(self):
		# Ends the layer after a set amount of time
		try:
			await asyncio.sleep(self.message_time)
			self.done = True
		except asyncio.CancelledError:
			# Acknowledging the alert will also cancel this task.
			pass

	async def acknowledge(self):
		# If the alert is acknowledged, clear it early.
		self.completion_task.cancel()
		self.done = True

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
				if self.message_x_offset == -self.message_width - 19:
					self.message_scrolling = False
					self.message_wrap = False
					self.message_x_offset = 1

		return self
