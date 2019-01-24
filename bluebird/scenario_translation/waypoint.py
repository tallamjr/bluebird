"""
Contains logic to map NATS waypoint data into the BlueSky format
"""

class Waypoint:
	"""
	Waypoint or fix in a scenario
	"""

	def __init__(self, lat_dir, lat_degrees, lat_minutes, lat_min_hundredth, \
	lon_dir, lon_degrees, lon_minutes, lon_min_hundredth):

		self.lat_dir = lat_dir
		self.lat_degrees = int(lat_degrees)
		self.lat_minutes = int(lat_minutes)
		self.lat_min_hundredth = int(lat_min_hundredth)
		self.lon_dir = lon_dir
		self.lon_degrees = int(lon_degrees)
		self.lon_minutes = int(lon_minutes)
		self.lon_min_hundredth = int(lon_min_hundredth)

	def trafscript(self):
		"""
		Returns the Trafscript string representation of this :Coordinates: object
		:return:
		"""

		traf_str = self.lat_dir + str(self.lat_degrees) + "'" + str(self.lat_minutes) + "'" + \
							 str(self.lat_min_hundredth / 100 * 60) + "\"," + self.lon_dir + str(self.lon_degrees) +\
               "'" + str(self.lon_minutes) + "'" + str(self.lon_min_hundredth / 100 * 60) + "\""

		return traf_str