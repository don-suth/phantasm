import asyncio
from layers.base_layer import BaseLayer
from rgbmatrix import FrameCanvas, graphics


class SleepingLayer(BaseLayer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.font = graphics.Font()
		self.font.LoadFont("my_fonts/spleen-12x24.bdf")
		self.state = 0
		self.countdown_task = asyncio.create_task(self.delay_state_change())

	async def delay_state_change(self):
		while not self.done:
			await asyncio.sleep(1.5)
			self.state = (self.state + 1) % 6
			if self.state == 0:
				await asyncio.sleep(8)

	def tick(self, canvas: FrameCanvas, frame_x_offset: int = 0, frame_y_offset: int = 0):
		canvas.Clear()
		message = ("z"*self.state).capitalize()
		graphics.DrawText(
			canvas, self.font, frame_x_offset + 2, frame_y_offset + 23,
			graphics.Color(255, 255, 255), text=message
		)
		return self
