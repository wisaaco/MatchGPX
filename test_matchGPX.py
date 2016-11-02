# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 16:15:51 2016

@author: isaac
"""
import gpxpy
import MatchGPX


path="gpx/"
route1 = "12488613.gpx"
route2 = "11483076.gpx"

#route1 = "thun_1_even.gpx"
#route2 = "thun_2_even.gpx"

f1 = open(path+route1)
p1 = gpxpy.parse(f1)

f2 = open(path+route2)
p2 = gpxpy.parse(f2)


tolerance = 0.0005

match = MatchGPX.MatchGPX(p1,p2)
match.fit(3,tolerance)


print match.get_matchR1R2()
print match.get_matchR2R1()



match.info()

match.draw()


print "Not overlap segments: %0.2f%% " %match.overlap_degree()