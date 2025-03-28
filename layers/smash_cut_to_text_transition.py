import asyncio
from layers.transition_base import BaseTransition
from rgbmatrix import FrameCanvas, RGBMatrix, graphics


class SmashCutTextTransition(BaseTransition):
	def __init__(self, matrix: RGBMatrix, from_layer, to_layer, *args, **kwargs):
		super().__init__(matrix, from_layer, to_layer, *args, **kwargs)
		self.font = graphics.Font()
		self.font.LoadFont("fonts/9x15B.bdf")
		self.countdown_task = asyncio.create_task(self.delay_transition())
		self.transition_complete = False

	async def delay_transition(self):
		await asyncio.sleep(2)
		self.transition_complete = True

	def tick(self, canvas: FrameCanvas, frame_x_offset: int = 0, frame_y_offset: int = 0):
		if self.transition_complete is False:
			canvas.Clear()
			graphics.DrawText(
				canvas, self.font, frame_x_offset + 7, frame_y_offset + 13,
				graphics.Color(255, 255, 255), text="Ring"
			)
			graphics.DrawText(
				canvas, self.font, frame_x_offset + 18, frame_y_offset + 27,
				graphics.Color(255, 255, 255), text="Ring!"
			)
			return self
		else:
			return self.to_layer.tick(canvas, frame_x_offset, frame_y_offset)
