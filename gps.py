#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import json
import urllib2
from math import pi

import ephem

def loadTLE(path):
    """ Loads a TLE file and creates a list of satellites."""
    f = urllib2.urlopen(path)
    satlist = []
    l1 = f.readline()
    while l1:
        l2 = f.readline()
        l3 = f.readline()
        sat = ephem.readtle(l1,l2,l3)
        satlist.append(sat)
        # print sat.name
        l1 = f.readline()

    f.close()
    # print "%i satellites loaded into list"%len(satlist)
    return satlist

def return_json(observer):
    satellites = loadTLE('http://www.celestrak.com/NORAD/elements/gps-ops.txt')

    # glonass = satellites.extend(loadTLE('http://www.celestrak.com/NORAD/elements/glo-ops.txt'))
    # galileo = satellites.extend(loadTLE('http://www.celestrak.com/NORAD/elements/galileo.txt'))

    structure = []
    for sat in satellites:
        sat.compute(observer)
        structure.append({'name': sat.name, 
                          'lat': sat.sublat*(180/pi), 
                          'lon': sat.sublong*(180/pi), 
                          'alt': sat.alt,
                          'az': sat.az})
    
    return json.dumps(structure)
    
sf = ephem.Observer()
sf.lon, sf.lat = '-122.7', '37.7'

print return_json(sf)
