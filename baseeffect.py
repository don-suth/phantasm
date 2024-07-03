from rgbmatrix import RGBMatrix


class BaseEffect:
	def __init__(self, matrix: RGBMatrix, *args, **kwargs):
		self.matrix = matrix
		self.done = False
		self.tick_rate = 0.01
	
	def tick(self):
		"""
		The main logic of the effect should be applied here.
		"""
		raise NotImplemented("Implement your own tick logic.")
	
	