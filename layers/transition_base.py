from rgbmatrix import RGBMatrix, FrameCanvas


class BaseTransition:
	def __init__(self, matrix: RGBMatrix, from_layer, to_layer, *args, **kwargs):
		self.matrix = matrix
		self.from_layer = from_layer
		self.to_layer = to_layer
		self.done = False

	def tick(self, canvas: FrameCanvas, frame_x_offset: int = 0, frame_y_offset: int = 0):
		"""
		The main logic of the transition should be applied here.
		"""
		raise NotImplemented("Implement your own logic here.")
