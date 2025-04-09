import asyncio
from layers.transition_base import BaseTransition
from rgbmatrix import FrameCanvas, RGBMatrix, graphics


class SmashCutTextTransition(BaseTransition):
	def __init__(self, matrix: RGBMatrix, from_layer, to_layer, *args, **kwargs):
		super().__init__(matrix, from_layer, to_layer, *args, **kwargs)
		self.font = graphics.Font()
		self.font.LoadFont("fonts/9x15B.bdf")
		self.countdown_task = asyncio.create_task(self.delay_transition())
		self.transition_state = 0

	async def delay_transition(self):
		# Initially show nothing
		await asyncio.sleep(0.01)

		# Show first line of text
		self.transition_state = 1
		await asyncio.sleep(0.3)

		# Show second line of text
		self.transition_state = 2
		await asyncio.sleep(2)

		# Finish the transition
		self.transition_state = -1

	def tick(self, canvas: FrameCanvas, frame_x_offset: int = 0, frame_y_offset: int = 0):
		if self.transition_state >= 0:
			canvas.Clear()
			if self.transition_state >= 1:
				graphics.DrawText(
					canvas, self.font, frame_x_offset + 7, frame_y_offset + 13,
					graphics.Color(255, 255, 255), text="Ring"
				)
			if self.transition_state >= 2:
				graphics.DrawText(
					canvas, self.font, frame_x_offset + 18, frame_y_offset + 27,
					graphics.Color(255, 255, 255), text="Ring!"
				)
			return self
		else:
			return self.to_layer.tick(canvas, frame_x_offset, frame_y_offset)
