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
        self.degree = -1
        
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

    def __getSubSequences(self,sequence,window,codeRoute):
        groups = np.bincount(sequence)
        degree =-1
        #A QUICK value to identify extrem cases: 0 and 100%
        if len(groups)==1 or (len(groups)==2 and groups[0]==0):
            if sequence[0]==False:
                degree =100 #Nothing in common
    
        subseq = []
        regionsstart=len(sequence)
        regionroute = -1
        previousReg = False
        for i in range(0,len(sequence)):
            if not sequence[i] and not previousReg:
                regionsstart = i
                regionroute = codeRoute[i]
                previousReg = True
            elif not sequence[i] and previousReg:
                if i-regionsstart >= window and regionroute != codeRoute[i]:
                     subseq.append([regionsstart,i-1,regionroute])
                     regionsstart = i
                     regionroute = codeRoute[i]
                     previousReg = True
            elif sequence[i] and previousReg:
                if i-regionsstart >= window and regionroute == codeRoute[i]:
                    subseq.append([regionsstart,i-1,regionroute])
                regionsstart = len(sequence)
                previousReg = False
                regionroute = -1
            
        if not sequence[i] and previousReg:
            if i-regionsstart >= window and regionroute == codeRoute[i]:
                    subseq.append([regionsstart,i-1,regionroute])
        subseq = np.array(subseq)            
        return degree,subseq
        
    def __distance(self,p1,p2): #No se tiene en cuenta la elevacion
        return vincenty(p1, p2)
        
    def fit(self,steps,tolerance):
        points_a = np.vstack(self.__loadSimplifiedPoints(self.p1))    
        points_b = np.vstack(self.__loadSimplifiedPoints(self.p2))
        
        all_trails = [points_a, points_b]
        self.all_pts = np.vstack([np.hstack([a, np.ones((a.shape[0], 1)) * i])
                                  for i, a in enumerate(all_trails)
                                  ])
        tree = scipy.spatial.KDTree(self.all_pts[:, :2])
        points_within_tolerance = tree.query_ball_point(self.all_pts[:, :2], tolerance)
        vfunc = np.vectorize(lambda a: np.any(self.all_pts[a, 2] != self.all_pts[a[0], 2]))
        self.matches = vfunc(points_within_tolerance)
    
        self.degree, self.regions = self.__getSubSequences(self.matches,steps,self.all_pts[:,2])

        self.regions_loop = []
        for region in self.regions:
            if region[0] <=steps or (region[0]>=len(points_a) and region[0]<len(points_a)+steps):
                self.regions_loop.append(False)
            elif (region[1] <=len(points_a) and region[1] >=len(points_a)-steps) or (region[1]>=len(self.matches)-steps):
                self.regions_loop.append(False)
            else:
                self.regions_loop.append(True)
                
            
            
        self.regions_length = []
        self.acc_region_1 = 0
        self.acc_region_2 = 0
        for idReg,region in enumerate(self.regions):
            distAcc = 0.0
            point = [self.all_pts[region[0]][0],self.all_pts[region[0]][1]]
            for idx in  range(int(region[0]+1),int(region[1]+1)):
                point2 = [self.all_pts[idx][0],self.all_pts[idx][1]]
                dist = self.__distance(point,point2).meters 
                distAcc += dist
                if not self.regions_loop[idReg]:
                    if region[2]==0:
                      self.acc_region_1 += dist
                    else:
                      self.acc_region_2 += dist
                point=point2
            self.regions_length.append(distAcc)
        self.regions_info = []
        if len(self.regions):
            self.regions_info = np.vstack([self.regions[:,2], self.regions_length, self.regions_loop])
            self.regions_info = self.regions_info.T
        
        
        self.length1 = self.p1.tracks[0].length_2d()   
        self.length2 = self.p2.tracks[0].length_2d()   
        self.lengths = [self.length1,self.length2]

#    def get_matchR1R2(self):
#        return (1-self.acc_region_1/self.length1)*100
#
#    def get_matchR2R1(self):
#        return (1-self.acc_region_2/self.length2)*100        
    """
    Get information of a sequence
    Return Init Point, End Point, Distance, Loop
    """
    def get_sequence(self,idRegion):
        if idRegion <=len(self.regions):
            iPoint = self.all_pts[self.regions[idRegion]]
            ePoint = self.all_pts[self.regions[idRegion]]
            return iPoint,ePoint,self.regions_info[idRegion][1],self.regions_info[idRegion][2]
        return None 
        
    """
    Get the overlap degree (percentage) between the routes
    """
    def overlap_degree(self):
        if self.degree >=0: return 100-self.degree
        accOverlap1 = 0    
        for region in self.regions_info:
            if region[0]==0:
                accOverlap1 += region[1]*100/self.length1

        accOverlap2 = 0
        for region in self.regions_info:
            if region[0]==1:
                accOverlap2 += region[1]*100/self.length2
 
        if max(accOverlap1,accOverlap2)>100:  return 0
        else: return 100-max(accOverlap1,accOverlap2)  
        
    def draw(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for idx,match in enumerate(self.matches):
            mark = "o"
            if match: mark = "+"
            ax.scatter(self.all_pts[idx][0],self.all_pts[idx][1], c=self.color[self.all_pts[idx][2]],alpha=0.5,marker=mark)
        for idx,region in enumerate(self.regions):
            intPoint = self.all_pts[int(region[0]+(region[1]-region[0])/2)]
            ax.annotate("R%i"%idx, xy=(intPoint[0], intPoint[1]), xytext=(intPoint[0]+0.001, intPoint[1]+0.001),color=self.color[intPoint[2]])
        plt.show()
    
            
    def info(self):
        rId = 0
        for idRoute in [0,1]:
            print "Route: %i (%s)" %(idRoute,self.color[idRoute])
            print "\tlength: %d meters" %self.lengths[idRoute]
            print "\tRegions:  " 
            for rInfo in self.regions_info:
                if rInfo[0]==idRoute:
                    print "\t\t R%i -- Length: %d meters & Loop: %s Perc.: %0.02f%%" %(rId,rInfo[1],rInfo[2],rInfo[1]*100/self.lengths[idRoute])
                    rId +=1