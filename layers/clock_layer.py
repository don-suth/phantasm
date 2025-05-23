from layers.base_layer import BaseLayer
import datetime

from rgbmatrix import graphics, FrameCanvas


class ClockLayer(BaseLayer):
	"""
	Displays the current time.
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.font = graphics.Font()
		self.font.LoadFont("my_fonts/spleen-12x24.bdf")
		self.small_font = graphics.Font()
		self.small_font.LoadFont("fonts/5x7.bdf")
		self.text_colour = graphics.Color(255, 255, 0)  # Yellow
		self.alternate_seconds_indicator = True

	def tick(self, canvas: FrameCanvas, frame_x_offset: int = 0, frame_y_offset: int = 0):
		current_time = datetime.datetime.now()
		current_hou = current_time.hour
		current_min = current_time.minute
		current_sec = current_time.second

		seconds_indicator = True
		if self.alternate_seconds_indicator and current_sec % 2 != 0:
			seconds_indicator = False

		# Draw time
		graphics.DrawText(
			canvas, self.font, frame_x_offset + 6, frame_y_offset + 21, self.text_colour,
			text=f"{current_hou:0>2}"
		)
		if seconds_indicator:
			graphics.DrawText(
				canvas, self.font, frame_x_offset + 26, frame_y_offset + 18, self.text_colour,
				text=":"
			)
		graphics.DrawText(
			canvas, self.font, frame_x_offset + 34, frame_y_offset + 21, self.text_colour,
			text=f"{current_min:0>2}"
		)
		if 4 <= current_time.day <= 20 or 24 <= current_time.day <= 30:
			day_suffix = "th"
		else:
			day_suffix = ["st", "nd", "rd"][current_time.day % 10 - 1]
		
		graphics.DrawText(
			canvas, self.small_font, frame_x_offset + 4, frame_y_offset + 30, self.text_colour,
			text=f"{current_time:%a}"
		)
		graphics.DrawText(
			canvas, self.small_font, frame_x_offset + 23, frame_y_offset + 30, self.text_colour,
			text=f"{current_time.day: >2}{day_suffix}"
		)
		graphics.DrawText(
			canvas, self.small_font, frame_x_offset + 46, frame_y_offset + 30, self.text_colour,
			text=f"{current_time:%b}"
		)
		return self
		
		
