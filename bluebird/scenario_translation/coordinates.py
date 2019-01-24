"""
Translation between different geographic coordinate formats

- degrees minutes seconds : 40° 26′ 46″ N 79° 58′ 56″ W
- degrees decimal minutes: 40° 26.767′ N 79° 58.933′ W
- decimal degrees: 40.446° N 79.982° W
"""

from math import floor

def degminsec2ddeg(degrees, minutes, seconds):
	"""
	Converts coordinates in degrees-minutes-seconds to decimal degrees
	:param degrees:
	:param minutes:
	:param seconds:
	:return: degrees
	"""
	return degrees + minutes/60 + seconds/3600

def degdmin2ddeg(degrees, dminutes):
	"""
	Converts coordinates in degrees-decimal minutes to decimal degrees
	:param degrees:
	:param dminutes:
	:return: degrees
	"""
	return degrees + dminutes/60

def degminsec2degdmin(degrees, minutes, seconds):
	"""
	Converts coordinates in degrees-minutes-seconds to degrees-decimal minutes
	:param degrees:
	:param minutes:
	:param seconds:
	:return: degrees, minutes
	"""
	return degrees, minutes + seconds/60

def ddeg2degdmin(degrees):
	"""
	Converts coordinates in decimal degrees to degrees-decimal minutes
	:param degrees:
	:return: degrees, minutes
	"""
	deg = floor(degrees)
	dminutes = (degrees - deg)*60
	return deg, dminutes

def ddeg2degminsec(degrees):
	"""
	Converts coordinates in decimal degrees to degrees-minutes-seconds
	:param degrees:
	:return: degrees, minutes, seconds
	"""
	deg = floor(degrees)
	dminutes = (degrees - deg)*60
	minutes = floor(dminutes)
	seconds = (dminutes - minutes)*60
	return deg, minutes, seconds

def degdmin2degminsec(degrees, dminutes):
	"""
	Converts coordinates in degrees-decimal minutes to degrees-minutes-seconds
	:param degrees:
	:param dminutes:
	:return: degrees, minutes, seconds
	"""
	minutes = floor(dminutes)
	seconds = (dminutes - minutes)*60
	return degrees, minutes, seconds
