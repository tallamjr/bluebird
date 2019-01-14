"""
Contains the BlueSky client class for our API
"""

import msgpack
import zmq

from bluebird.cache import AC_DATA
from bluebird.utils import TIMERS, Timer
from bluebird.utils.debug import errprint
from bluesky.network.client import Client
from bluesky.network.npcodec import decode_ndarray

# TODO Figure out what we topics we need to subscribe to. Is there a list of possible events?
ACTIVE_NODE_TOPICS = [b'ACDATA', b'SIMINFO']  # Also available: ROUTEDATA

# Same rate as GuiClient polls for its data
POLL_RATE = 50  # Hz


class ApiClient(Client):
	"""
	Client class for the BlueSky simulator
	"""

	def __init__(self):
		super(ApiClient, self).__init__(ACTIVE_NODE_TOPICS)

		# Continually poll for the sim state
		self.timer = Timer(self.receive, int(1 / POLL_RATE))
		self.timer.start()

		TIMERS.append(self.timer)

	def stop(self):
		"""
		Stop the client and disconnect.
		"""

		# TODO Send quit signal properly
		self.timer.stop()

	def stream(self, name, data, sender_id):
		"""
		Method called to process data received on a stream
		:param name:
		:param data:
		:param sender_id:
		"""

		# Fill the cache with the aircraft data
		if name == b'ACDATA':
			AC_DATA.fill(data)

		elif name == b'SIMINFO':
			# TODO Figure out what data is provided here
			errprint('SIMINFO {}'.format(data))

		self.stream_received.emit(name, data, sender_id)

	def send_stackcmd(self, data=None, target=b'*'):
		"""
		Send a command to the BlueSky simulation command stack
		:param data:
		:param target:
		"""

		self.send_event(b'STACKCMD', data, target)

	# TODO This is the same as the base method except for debugging code. Can remove when unused.
	def receive(self, timeout=0):
		try:
			socks = dict(self.poller.poll(timeout))
			if socks.get(self.event_io) == zmq.POLLIN:

				msg = self.event_io.recv_multipart()

				# Remove send-to-all flag if present
				if msg[0] == b'*':
					msg.pop(0)

				route, eventname, data = msg[:-2], msg[-2], msg[-1]

				self.sender_id = route[0]
				route.reverse()
				pydata = msgpack.unpackb(data, object_hook=decode_ndarray, encoding='utf-8')

				errprint('EVT :: {} :: {}'.format(eventname, pydata))

				if eventname == b'NODESCHANGED':
					self.servers.update(pydata)
					self.nodes_changed.emit(pydata)

					# If this is the first known node, select it as active node
					nodes_myserver = next(iter(pydata.values())).get('nodes')
					if not self.act and nodes_myserver:
						self.actnode(nodes_myserver[0])

				# TODO Handle simulation exit before client
				elif eventname == b'QUIT':
					errprint('Received sim exit')
					self.signal_quit.emit()
				else:
					self.event(eventname, pydata, self.sender_id)

			if socks.get(self.stream_in) == zmq.POLLIN:
				msg = self.stream_in.recv_multipart()

				strmname = msg[0][:-5]
				sender_id = msg[0][-5:]
				pydata = msgpack.unpackb(msg[1], object_hook=decode_ndarray, encoding='utf-8')

				self.stream(strmname, pydata, sender_id)

			# If we are in discovery mode, parse this message
			if self.discovery and socks.get(self.discovery.handle.fileno()):
				dmsg = self.discovery.recv_reqreply()
				if dmsg.conn_id != self.client_id and dmsg.is_server:
					self.server_discovered.emit(dmsg.conn_ip, dmsg.ports)

			return True

		except zmq.ZMQError as exc:
			errprint(exc)
			return False
