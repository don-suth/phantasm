from layers.base_layer import BaseLayer
import datetime

from rgbmatrix import graphics


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

	def tick(self, canvas):
		current_time = datetime.datetime.now()
		current_hou = current_time.hour
		current_min = current_time.minute
		current_sec = current_time.second

		if current_hou >= 12:
			current_hou -= 12
			am_pm = "PM"
		else:
			am_pm = "AM"
		
		if current_sec % 2 == 0:
			# Draw seconds indicator
			seconds_indicator = True
		else:
			seconds_indicator = False
		
		# Draw time
		graphics.DrawText(
			canvas, self.font, 6, 23, self.text_colour,
			text=f"{current_hou: >2}"
		)
		if seconds_indicator:
			graphics.DrawText(
				canvas, self.font, 26, 20, self.text_colour,
				text=":"
			)
		graphics.DrawText(
			canvas, self.font, 34, 23, self.text_colour,
			text=f"{current_min:0>2}"
		)
		graphics.DrawText(
			canvas, self.small_font, 1, 31, self.text_colour,
			text=f"{current_time:%a %d %B}"
		)
		
		
