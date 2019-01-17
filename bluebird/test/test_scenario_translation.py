"""
Tests for the scenario_translation module
"""

import json

import pytest

from bluebird.scenario_translation import parse_nats_sector


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


# TODO:
# - test loading of sectors
# 	- areas - done
#		- vertices
#		- coordinates
# - test translation into Trafscript
