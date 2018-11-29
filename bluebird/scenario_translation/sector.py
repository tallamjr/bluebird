import json

class Coordinates:
  """ Coordinates of vertices that specify sector areas """
  
  def __init__(self, lat_dir, lat_degrees, lat_minutes, lat_min_hundredth, 
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
    s = self.lat_dir + str(self.lat_degrees) + "'" + str(self.lat_minutes) + "'" + \
        str(self.lat_min_hundredth/100*60) + "\"," + \
        self.lon_dir + str(self.lon_degrees) + "'" + str(self.lon_minutes) + "'" + \
        str(self.lon_min_hundredth/100*60) + "\""
    return(s)

class Area:   
  """ Area is a part of a sector defined by a set of vertices, and top and bottom levels (in ft) """
  
  def __init__(self, name, top_level, bottom_level, vertices):
    self.name = name
    self.top_level = top_level
    self.bottom_level = bottom_level
    self.vertices = vertices
  
  def trafscript(self, sector_prefix = ""):
    vert_loc = [str(self.top_level), str(self.bottom_level)]
    horz_loc = list(map(lambda c: c.trafscript(), self.vertices))
    s = ','.join(["00:00:00.00>POLYALT " + sector_prefix + self.name] + vert_loc + horz_loc)
    return(s)    


class Sector:
  """ Sector is defined by a contiguous set of areas """
  
  def __init__(self, name, areas):
    self.name = name
    self.areas = areas
  
  def trafscript(self):
    areas = list(map(lambda area: area.trafscript(self.name + "-"), self.areas))  
    return(areas)



def parse_nats_coordinates(v):
  c = Coordinates(v['latDir'], v['latDeg'], v['latMin'], v['latMinHundredth'], \
                  v['lngDir'], v['lngDeg'], v['lngMin'], v['lngMinHundredth'])
  return(c)

def parse_nats_area(a):
  vertices = list(map(parse_nats_coordinates, a['vertices']))
  area = Area(a['ID'], a['CEIL_FT'], a['FLOOR_FT'], vertices)      
  return(area)

def parse_nats_sector(name, nats_data):
  areas = list(map(parse_nats_area, nats_data))
  return(Sector(name, areas))


