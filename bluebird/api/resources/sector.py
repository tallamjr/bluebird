"""
Provides logic for the sector API endpoint
"""
from http import HTTPStatus

import geojson
from aviary.sector.sector_element import SectorElement
from flask_restful import reqparse
from flask_restful import Resource

import bluebird.api.resources.utils.responses as responses
import bluebird.api.resources.utils.utils as utils
from bluebird.utils.properties import Sector as SectorWrapper
from bluebird.utils.sector_validation import validate_geojson_sector


_PARSER = reqparse.RequestParser()
_PARSER.add_argument("name", type=str, location="json", required=True)
_PARSER.add_argument("content", type=dict, location="json", required=False)


class Sector(Resource):
    """Contains logic for the SECTOR endpoint"""

    @staticmethod
    def get():
        """Returns the sector defined in the current simulation"""

        sector: SectorWrapper = utils.sim_proxy().simulation.sector

        if not sector:
            return responses.bad_request_resp("No sector has been set")

        # TODO (RKM 2019-12-20) Check what exceptions this can throw
        try:
            geojson_str = geojson.dumps(sector.element)
        except Exception as exc:
            return responses.internal_err_resp(f"Couldn't get sector geojson: {exc}")

        return responses.ok_resp({"name": sector.name, "content": geojson_str})

    @staticmethod
    def post():
        """Upload a new sector definition"""

        req_args = utils.parse_args(_PARSER)

        sector_name = req_args["name"]

        if not sector_name:
            return responses.bad_request_resp("Sector name must be provided")

        sector_json = req_args["content"]

        if sector_json:
            sector_element = validate_geojson_sector(sector_json)
            if not isinstance(sector_element, SectorElement):
                return responses.bad_request_resp(
                    f"Invalid sector content: {sector_element}"
                )
        else:
            sector_element = None

        sector = SectorWrapper(sector_name, sector_element)
        err = utils.sim_proxy().simulation.load_sector(sector)

        return responses.checked_resp(err, HTTPStatus.CREATED)
