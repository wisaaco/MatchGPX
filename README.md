# MatchGPX

This algorithm computes the overlapping through the number of common segments between two GPS trajectories.

It uses KDTree algorithm to compute the overlap degree of two GPX tracks. The result is a percentage based on the distance of different segments per the total distance.

+ It draws both trajectories and highlights the segments.
+ It returns a descriptive information of each track, and sequences: length, and loop.
+ It returns a list of segments between route1 and route2, and viceversa.
+ It returns a percentage value of the degree of each overlapped segment.

Note: In the code, the usual term is sequence but I prefer to use the term region.

## Example
Overlap degree: 67.84% 

![alt tag](https://github.com/wisaaco/MatchGPX/blob/master/images/ex1.png)
```text
Route: 0 (red)
        length: 22964 meters
        Regions:  
                 R0 -- Length: 5677 meters & Loop: 0.0 Perc.: 24.72%
Route: 1 (blue)
        length: 26537 meters
        Regions:  
                 R1 -- Length: 6474 meters & Loop: 0.0 Perc.: 24.40%
                 R2 -- Length: 330 meters & Loop: 1.0 Perc.: 1.25%
                 R3 -- Length: 135 meters & Loop: 1.0 Perc.: 0.51%
                 R4 -- Length: 50 meters & Loop: 1.0 Perc.: 0.19%
                 R5 -- Length: 64 meters & Loop: 1.0 Perc.: 0.24%
                 R6 -- Length: 1478 meters & Loop: 1.0 Perc.: 5.57%
```               
### More cases:                 
Overlap degree: 12.0640%
![alt tag](https://github.com/wisaaco/MatchGPX/blob/master/images/ex2.png)

Overlap degree: 0%
![alt tag](https://github.com/wisaaco/MatchGPX/blob/master/images/ex3.png)

Overlap degree: 0%
![alt tag](https://github.com/wisaaco/MatchGPX/blob/master/images/ex4.png)


# It requires:
+ GPXPY library
+ Scipy - KDTree
+ geopy.distance
+ numpy
