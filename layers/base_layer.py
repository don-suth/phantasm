import asyncio
from rgbmatrix import RGBMatrix, FrameCanvas


class BaseLayer:
	def __init__(self, matrix: RGBMatrix, *args, **kwargs):
		self.matrix = matrix
		self.done = False
	
	def tick(self, canvas: FrameCanvas, frame_x_offset: int = 0, frame_y_offset: int = 0):
		"""
		The main logic of the effect should be applied here.
		"""
		raise NotImplemented("Implement your own tick logic.")

	async def is_done(self):
		while not self.done:
			await asyncio.sleep(0)
		return True
	
	