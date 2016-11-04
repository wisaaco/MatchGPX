# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 16:15:51 2016

@author: isaac
"""
import gpxpy
import MatchGPX


path="gpx/"


route1 = "5057009.gpx"
route2 = "7221030.gpx"

f1 = open(path+route1)
p1 = gpxpy.parse(f1)

f2 = open(path+route2)
p2 = gpxpy.parse(f2)


tolerance = 0.0005

match = MatchGPX.MatchGPX(p1,p2)
match.fit(3,tolerance)

match.info()
match.draw()

print "Overlap degree: %0.2f%% " %match.overlap_degree()