import pytest
import json
import os

import bluebird.scenario_translation.sector as ts

@pytest.fixture
def sector_description_json():
  '''Returns JSON document with description of a sector'''
  file = "./scenarios/airspace/Sector 31.json"
  with open(file, "r") as json_file:
    data = json.load(json_file)
    return data

def test_sector(sector_description_json):
  parsed = ts.parse_nats_sector("tmp", sector_description_json)
  assert 1 == 1

# TODO: 
# - test loading of sectors - all expected fields are parsed
# - test translation into Trafscript  