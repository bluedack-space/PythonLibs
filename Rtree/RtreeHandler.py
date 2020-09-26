import os
import sys
sys.path.append("/usr/local/lib/python3.6/dist-packages")
sys.path.append("/usr/lib/python3/dist-packages")

from rtree import index

class RtreePoint3D():
    
    def __init__(self):
        p           = index.Property()
        p.dimension = 3
        self.idx3d  = index.Index(properties=p)
        self.coords = []
        
    def add(self, id, pnt3d):
        self.idx3d.add(id, pnt3d)
        self.coords.append(pnt3d)
        
    def nearest(self,pnt3d,size):
        return list( self.idx3d.nearest(pnt3d, size) )
    
    def intersection(self,pnt3d):
        return list( self.idx3d.intersection(( pnt3d[0], pnt3d[1], pnt3d[2]
                                              ,pnt3d[0], pnt3d[1], pnt3d[2])) )
    
class RtreePoint2D():
    
    def __init__(self):
        p           = index.Property()
        p.dimension = 2
        self.idx2d  = index.Index(properties=p)
        self.coords = []
        
    def add(self, id, pnt2d):
        self.idx2d.add(id, pnt2d)
        self.coords.append(pnt2d)
        
    def nearest(self,pnt2d,size):
        return list( self.idx2d.nearest(pnt2d, size) )
    
    def intersection(self,pnt2d):
        return list( self.idx2d.intersection(( pnt2d[0], pnt2d[1] 
                                              ,pnt2d[0], pnt2d[1] )) )
    
from random import randrange

if __name__ == '__main__':
    
    # Generation of random scatter points
    import numpy as np
    nmax = 100
    x    = np.random.rand(nmax)
    y    = np.random.rand(nmax)
    
    # Plot to check
    import matplotlib.pyplot as plt
    plt.scatter(x, y)
    plt.show()
    
    # Checkin to RtreeHandler2D
    rt = RtreePoint2D()
    for n in range(nmax):
        coord = (x[n],y[n])
        rt.add( n, coord )
        
    # Check Rtree Function No.1
    for id1 in range(2):
        print("=====================================")
        nearest = rt.nearest(rt.coords[id1], 10)
      # nearest = rt.intersection(coords[id1])
        for i in range(len(nearest)):
            id = nearest[i]
            c1 = rt.coords[id]
            print("id:"+str(id)+" "+str(c1))
        print("=====================================")
        
    # Check Rtree Function No.2
    nearest = rt.nearest(rt.coords[nmax-10], 10)
    for i in range(len(nearest)):
        id = nearest[i]
        c1 = rt.coords[id]
        print("id:"+str(id)+" "+str(c1))
        
