"""
Contains logic to map NATS scenario data into the BlueSky format
"""


class Coordinates:
	"""
	Coordinates of vertices that specify sector areas
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


class Area:
	"""
	Area is a part of a sector defined by a set of vertices, and top and bottom levels (in ft)
	"""

	def __init__(self, name, top_level, bottom_level, vertices):
		self.name = name
		self.top_level = top_level
		self.bottom_level = bottom_level
		self.vertices = vertices

	def trafscript(self, sector_prefix=""):
		"""

		:param sector_prefix:
		:return:
		"""

		vert_loc = [str(self.top_level), str(self.bottom_level)]
		horz_loc = list(map(lambda c: c.trafscript(), self.vertices))

		traf_str = ','.join(["00:00:00.00>POLYALT " + sector_prefix + self.name] + vert_loc + horz_loc)

		return traf_str


class Sector:
	"""
	Sector is defined by a contiguous set of areas
	"""

	def __init__(self, name, areas):
		"""

		:param name:
		:param areas:
		"""

		self.name = name
		self.areas = areas

	def trafscript(self):
		"""

		:return:
		"""

		return list(map(lambda area: area.trafscript(self.name + "-"), self.areas))


def parse_nats_coordinates(vert):
	"""
	Maps a set of NATS coordinates into a :Coordinates: object
	:param vert:
	:return:
	"""

	coord = Coordinates(vert['latDir'], vert['latDeg'], vert['latMin'], vert['latMinHundredth'],
	                    vert['lngDir'], vert['lngDeg'], vert['lngMin'], vert['lngMinHundredth'])

	return coord


def parse_nats_area(nats_area):
	"""
	Converts a NATS area to an :Area: object
	:param a:
	:return:
	"""

	vertices = list(map(parse_nats_coordinates, nats_area['vertices']))
	area = Area(nats_area['ID'], int(nats_area['CEIL_FT']), int(nats_area['FLOOR_FT']), vertices)

	return area


def parse_nats_sector(name, nats_data):
	"""
	Converts a NATS sector to a :Sector: object
	:param name:
	:param nats_data:
	:return:
	"""

	areas = list(map(parse_nats_area, nats_data))
	return Sector(name, areas)

# TODO
# Compute polygon covering the entire set of sectors and create it as AREA in Trafscript
