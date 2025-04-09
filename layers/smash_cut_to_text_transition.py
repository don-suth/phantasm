import asyncio
import random
from layers.transition_base import BaseTransition
from rgbmatrix import FrameCanvas, RGBMatrix, graphics

TEXT_NOTIFICATIONS = (
	("Ring", "Ring!"),
	("Ding", "Dong!"),
	("Hello", "there"),
	("Look", "at me"),
)


class SmashCutTextTransition(BaseTransition):
	def __init__(self, matrix: RGBMatrix, from_layer, to_layer, *args, **kwargs):
		super().__init__(matrix, from_layer, to_layer, *args, **kwargs)
		self.font = graphics.Font()
		self.font.LoadFont("fonts/9x15B.bdf")
		self.countdown_task = asyncio.create_task(self.delay_transition())
		self.transition_state = 0
		self.display_texts = TEXT_NOTIFICATIONS[0]

	async def delay_transition(self):
		while True:
			# Initially show nothing
			await asyncio.sleep(0.01)

			# Show first line of text
			self.transition_state = 1
			await asyncio.sleep(0.3)

			# Show second line of text
			self.transition_state = 2
			await asyncio.sleep(2)

			# Reset for testing purposes
			self.display_texts = random.choice(TEXT_NOTIFICATIONS)
			self.transition_state = 0
			await asyncio.sleep(1)

		# Finish the transition
		self.transition_state = -1

	def tick(self, canvas: FrameCanvas, frame_x_offset: int = 0, frame_y_offset: int = 0):
		if self.transition_state >= 0:
			canvas.Clear()
			if self.transition_state >= 1:
				graphics.DrawText(
					canvas, self.font, frame_x_offset + 7, frame_y_offset + 13,
					graphics.Color(255, 255, 255), text=self.display_texts[0],
				)
			if self.transition_state >= 2:
				graphics.DrawText(
					canvas, self.font, frame_x_offset + 18, frame_y_offset + 27,
					graphics.Color(255, 255, 255), text=self.display_texts[1],
				)
			return self
		else:
			return self.to_layer.tick(canvas, frame_x_offset, frame_y_offset)
