"""
Base logic for any cache classes.
"""

from bluebird.utils.timeutils import DEFAULT_LIFETIME, before, now

VALID_TO = '_validTo'


class Cache:
	"""
	Simple cache implementation. Holds data streamed from the simulation.
	"""

	def __init__(self):
		"""
		Default constructor
		"""

		self.store = {}

	def get(self, key):
		"""
		Get a piece of data given the key
		:param key: Lookup key for the data
		:return:
		"""

		if key in self.store and before(self.store[key][VALID_TO] + DEFAULT_LIFETIME):
			return dict(self.store[key])

		return self.miss(key)

	def fill(self, data):
		"""
		Put data into the store.
		:param data:
		"""

		if not isinstance(data, dict):
			raise TypeError("Unsupported data type for cache: {}".format(type(data)))

		for key in data:
			item = data[key]
			if isinstance(item, dict):
				self.store[key] = {k: v for k, v in item}
				self.store[key][VALID_TO] = now()

	def miss(self, key):
		"""
		Action to take if the requested data is not in the store.
		:param key: Lookup key for the data
		:return: Data or None
		"""

	def clear(self):
		"""
		Clear any data in the store.
		"""

		self.store = {}
