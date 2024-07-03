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
		self.effect_queue: list = []
		self.current_effect: BaseEffect | None = None
	
	def run(self):
		print("Running... Press CTRL-C to stop")
		while True:
			if self.current_effect is not None:
				self.current_effect.tick()
				time.sleep(self.current_effect.tick_rate)
				if self.current_effect.done:
					self.current_effect = None
			else:
				if len(self.effect_queue) > 0:
					self.current_effect = self.effect_queue.pop(0)
					continue
				else:
					time.sleep(0.01)
	
	def add_to_queue(self, effect: BaseEffect):
		self.effect_queue.append(effect)

	