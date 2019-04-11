"""
Provides logic for the DEFWPT (define waypoint) API endpoint
"""

import logging

from flask import jsonify
from flask_restful import Resource, reqparse

import bluebird.client

_LOGGER = logging.getLogger('bluebird')

PARSER = reqparse.RequestParser()
PARSER.add_argument('wpname', type=str, location='json', required=True)
PARSER.add_argument('lat', type=float, location='json', required=True)
PARSER.add_argument('lon', type=float, location='json', required=True)
PARSER.add_argument('type', type=str, location='json', required=False)


class DefWpt(Resource):
	"""
	BlueSky DEFWPT (define waypoint) command
	"""

	@staticmethod
	def post():
		"""
		Logic for POST events. If the request contains valid waypoint information, then a request is
		sent to the simulator to create it.
		:return: :class:`~flask.Response`
		"""

		parsed = PARSER.parse_args(strict=True)

		if not parsed['wpname']:
			resp = jsonify('Waypoint name must be provided')
			resp.status_code = 400
			return resp

		wp_type = parsed['type'] if parsed['type'] else ''
		cmd_str = f'DEFWPT {parsed["wpname"]} {parsed["lat"]} {parsed["lon"]} {wp_type}'

		_LOGGER.info(f'Sending stack command: {cmd_str}')
		reply = bluebird.client.CLIENT_SIM.send_stack_cmd(cmd_str, response_expected=True)

		if not reply:
			resp = jsonify('Error: No route data received from BlueSky')
			resp.status_code = 500
			return resp

		resp = jsonify(''.join(reply))
		resp.status_code = 200
		return resp