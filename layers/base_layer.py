from rgbmatrix import RGBMatrix, FrameCanvas


class BaseLayer:
	def __init__(self, matrix: RGBMatrix, *args, **kwargs):
		self.matrix = matrix
		self.done = False
	
	def tick(self, canvas: FrameCanvas, x_offset: int = 0, y_offset: int = 0):
		"""
		The main logic of the effect should be applied here.
		"""
		raise NotImplemented("Implement your own tick logic.")
	
	