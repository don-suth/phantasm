import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from baseeffect import BaseEffect


class MatrixController:
	def __init__(self):
		options = RGBMatrixOptions()
		
		# Specific options for our board
		options.hardware_mapping = "adafruit-hat"
		options.rows = 32
		options.cols = 64
		options.chain_length = 1
		options.parallel = 1
		options.row_address_type = 0
		options.multiplexing = 0
		options.pwm_bits = 11
		options.brightness = 100
		options.pwm_lsb_nanoseconds = 130
		options.led_rgb_sequence = "RGB"
		options.pixel_mapper_config = ""
		options.panel_type = ""
		options.show_refresh_rate = 0
		options.gpio_slowdown = 4
		options.drop_privileges = True
		options.disable_hardware_pulsing = False
		
		self.matrix = RGBMatrix(options=options)
		self.effect_layers: list[BaseEffect] = []
		self.tick_rate = 0.02
	
	def run(self):
		print("Running... Press CTRL-C to stop")
		frame_canvas = self.matrix.CreateFrameCanvas()
		while True:
			for layer in self.effect_layers:
				layer.tick(frame_canvas)
			frame_canvas = self.matrix.SwapOnVSync(frame_canvas)
			frame_canvas.Clear()
			self.effect_layers[:] = [layer for layer in self.effect_layers if not layer.done]
			time.sleep(self.tick_rate)
	
	def add_to_layers(self, effect_class: type[BaseEffect], *args, **kwargs):
		self.effect_layers.append(effect_class(self.matrix, *args, **kwargs))

	