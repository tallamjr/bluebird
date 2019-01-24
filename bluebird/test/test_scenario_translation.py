"""
Tests for the scenario_translation module
"""

import json

import pytest

from bluebird.scenario_translation import parse_nats_sector
import bluebird.scenario_translation.coordinates as coord


@pytest.fixture
def sector_description_json():
	"""
	Returns JSON document with description of a sector
	"""

	file = "./data/dummy-scenarios/airspace/Sector 00.json"

	with open(file, "r") as json_file:
		data = json.load(json_file)
		return data

@pytest.fixture
def sector_areas(sector_description_json):
	"""
	Returns first area from a parsed sector file
	"""
	sector = parse_nats_sector("", sector_description_json)
	return sector.areas

@pytest.mark.parametrize('idx', [0, 1, 2])
def test_area(sector_areas, idx):
	"""
	Tests if an area can be successfully parsed
	"""
	area = sector_areas[idx]
	assert area.top_level >= 0
	assert area.top_level < 50000
	assert area.top_level > area.bottom_level
	assert area.bottom_level >= 0
	assert area.vertices

def test_sector(sector_description_json):
	"""
	Tests if a sector can be successfully parsed
	:param sector_description_json:
	:return:
	"""

	parsed = parse_nats_sector("dummy sector", sector_description_json)
	assert parsed.areas  # number of parsed areas is non-zero

def test_coordinate_formats():
	"""
	Testing translation between individual geographic coordinate formats 
	"""
	lat, lon = 51.5254607, -0.12926379999999998   # The British Library location
	lat1, mlat1 = coord.ddeg2degdmin(lat)
	lat2, mlat2, slat2 = coord.ddeg2degminsec(lat)
	lat3, mlat3, slat3 = coord.degdmin2degminsec(lat1, mlat1)
	lat4, mlat4 = coord.degminsec2degdmin(lat2, mlat2, slat2)

	dlat_trans1 = coord.degdmin2ddeg(lat1, mlat1)
	dlat_trans2 = coord.degminsec2ddeg(lat2, mlat2, slat2)
	dlat_trans3 = coord.degminsec2ddeg(lat3, mlat3, slat3)
	dlat_trans4 = coord.degdmin2ddeg(lat4, mlat4)

	assert lat == pytest.approx(dlat_trans1)
	assert lat == pytest.approx(dlat_trans2)
	assert lat == pytest.approx(dlat_trans3)
	assert lat == pytest.approx(dlat_trans4)


# TODO:
# - test loading of sectors
# 	- areas - done
#		- vertices
#		- coordinates
# - test translation into Trafscript
