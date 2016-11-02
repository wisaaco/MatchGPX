# MatchGPX
Compute the overlapping and the relationship between two GPX trajectories

It uses KDTree algorithm to compute the overlap degree of two gpx tracks. The result degree is a percentatge based on the distance of 
different segments and total distance.

+ Draw both trajectories and it highlights the different segements.
+ Give a descriptive information of each track, and segments.
+ Give the relationship between route1 and route2, and viceversa.
+ Give a percentatge value of the inverse of not overlapped areas (1-p)

![alt tag](http://url/to/img.png)

Requires:
+ GPXPY library
+ Scipy - KDTree
+ geopy.distance
+ numpy
