from rgbmatrix import RGBMatrix, FrameCanvas


class BaseEffect:
	def __init__(self, matrix: RGBMatrix, *args, **kwargs):
		self.matrix = matrix
		self.done = False
	
	def tick(self, canvas: FrameCanvas):
		"""
		The main logic of the effect should be applied here.
		"""
		raise NotImplemented("Implement your own tick logic.")
	
	