# MatchGPX
Compute the overlapping and the relationship between two GPX trajectories

It uses KDTree algorithm to compute the overlap degree of two gpx tracks. The result degree is a percentage based on the distance of 
different segments and total distance.

+ Draw both trajectories and it highlights the different segments.
+ Give a descriptive information of each track, and segments.
+ Give the relationship between route1 and route2, and viceversa.
+ Give a percentage value of the degree of overlapped segments

![alt tag](https://github.com/wisaaco/MatchGPX/blob/master/images/ex1.png)

Requires:
+ GPXPY library
+ Scipy - KDTree
+ geopy.distance
+ numpy
