# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 13:09:54 2016

@author: isaac
"""
import scipy.spatial
from matplotlib import pyplot as plt
from geopy.distance import vincenty
import numpy as np
    
    

class MatchGPX:
    """ Matching two GPX-tracks"""
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        self.color = {0:"red",1:"blue"}
        
    def __loadSimplifiedPoints(self,p):
        points_a = []
        p.simplify()
        p.reduce_points(500)
        for track in p.tracks:  # OJO SOLO HAY UN TRACK
            for segment in track.segments:  # OJO SOLO HAY UN SEGMENT
                for iA in range(0,len(segment.points)-1):
                    point = segment.points[iA]
                    points_a.append([point.longitude,point.latitude])
        return np.asarray(points_a)

    def __getSubSequences(self,sequence,window,lenRoute1):
        subseq = []
        regionsstart=len(sequence)
        previousReg = False
        for i in range(0,len(sequence)):
            route = 0
            if i>=lenRoute1: route = 1
            if not sequence[i] and not previousReg:
                regionsstart = i
                previousReg = True
            elif sequence[i] and previousReg:
                if i-regionsstart >= window:
                    subseq.append([regionsstart,i-1,route])
                regionsstart = len(sequence)
                previousReg = False
            
        if not sequence[i] and previousReg:
            if i-regionsstart >= window:
                    subseq.append([regionsstart,i-1,route])
        return subseq
        
    def __distance(self,p1,p2): #No se tiene en cuenta la elevacion
        return vincenty(p1, p2)
        
    def fit(self,steps,tolerance):
        points_a = np.vstack(self.__loadSimplifiedPoints(self.p1))    
        points_b = np.vstack(self.__loadSimplifiedPoints(self.p2))
        
        all_trails = [points_a, points_b]
        self.labelled_pts = np.vstack([np.hstack([a, np.ones((a.shape[0], 1)) * i])
                                  for i, a in enumerate(all_trails)
                                  ])
        tree = scipy.spatial.KDTree(self.labelled_pts[:, :2])
        points_within_tolerance = tree.query_ball_point(self.labelled_pts[:, :2], tolerance)
        vfunc = np.vectorize(lambda a: np.any(self.labelled_pts[a, 2] != self.labelled_pts[a[0], 2]))
        self.matches = vfunc(points_within_tolerance)
    
        regions = self.__getSubSequences(self.matches,steps,len(points_a))
        self.regions = np.array(regions)
        
        self.regions_loop = []
        for region in self.regions:
            if region[0] <=steps or (region[0]>len(points_a) and region[0]<len(points_a)+steps):
                self.regions_loop.append(False)
            elif (region[1] <=len(points_a) and region[1] >=len(points_a)-steps) or (region[1]>=len(self.matches)+steps):
                self.regions_loop.append(False)
            else:
                self.regions_loop.append(True)
                
            
            
        self.regions_length = []
        self.acc_region_1 = 0
        self.acc_region_2 = 0
        for idReg,region in enumerate(self.regions):
            distAcc = 0.0
            point = [self.labelled_pts[region[0]][0],self.labelled_pts[region[0]][1]]
            for idx in range(region[0]+1,region[1]+1):
                point2 = [self.labelled_pts[idx][0],self.labelled_pts[idx][1]]
                dist = self.__distance(point,point2).meters 
                distAcc += dist
                if not self.regions_loop[idReg]:
                    if region[2]==0:
                      self.acc_region_1 += dist
                    else:
                      self.acc_region_2 += dist
                point=point2
            self.regions_length.append(distAcc)
    
        self.regions_info = np.vstack([self.regions[:,2], self.regions_length, self.regions_loop])
        self.regions_info = self.regions_info.T
        
        
        self.length1 = self.p1.tracks[0].length_2d()   
        self.length2 = self.p2.tracks[0].length_2d()   
        self.lengths = [self.length1,self.length2]

    def get_matchR1R2(self):
        return (1-self.acc_region_1/self.length1)*100

    def get_matchR2R1(self):
        return (1-self.acc_region_2/self.length2)*100        

    def overlap_degree(self):
        accOverlap1 = 0    
        for region in self.regions_info:
            if region[0]==0:
                accOverlap1 += region[1]*100/self.length1

        accOverlap2 = 0
        for region in self.regions_info:
            if region[0]==1:
                accOverlap2 += region[1]*100/self.length2
        
        return max(accOverlap1,accOverlap2)  
        
    def draw(self):
        for idx,match in enumerate(self.matches):
            mark = "o"
            if match: mark = "+"
            plt.scatter(self.labelled_pts[idx][0],self.labelled_pts[idx][1], c=self.color[self.labelled_pts[idx][2]],alpha=0.5,marker=mark)
            
    def info(self):
        for idRoute in [0,1]:
            print "Route: %i (%s)" %(idRoute,self.color[idRoute])
            print "\tlength: %d meters" %self.lengths[idRoute]
            print "\tRegions:  " 
            for rInfo in self.regions_info:
                if rInfo[0]==idRoute:
                    print "\t\t Length: %d meters & Loop: %s Perc.: %0.02f%%" %(rInfo[1],rInfo[2],rInfo[1]*100/self.lengths[idRoute])
            