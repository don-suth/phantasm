from base_layer import BaseLayer
import datetime


class ClockLayer(BaseLayer):
	"""
	Displays the current time.
	"""

	def __init__(self, *args, **kwargs):
		self.text_colour = (255, 0, 0)  # Pure Red

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

		# Draw time
		pass

		if current_sec % 2 == 0:
			# Draw seconds indicator
			pass
