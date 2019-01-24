"""
Contains logic to map NATS waypoint data into the BlueSky format
"""

class Waypoint:
	"""
	Waypoint or fix in a scenario, determined by its coordinates
	"""

	def __init__(self):
		self.latitude = 0
		self.longitude = 0

	def trafscript(self):
		"""
		Returns the Trafscript string representation of this :Waypoint: object
		:return:
		"""

		traf_str = ""

		return traf_str
