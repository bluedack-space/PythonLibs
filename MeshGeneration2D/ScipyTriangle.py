import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
 
# x and y from 0 to 1 in n steps
n=10
x=np.linspace(0,1,n)
y=np.linspace(0,1,n)
 
xx,yy=np.meshgrid(x,y)
# reshape meshgrid and stack them to get the right shape for
# delaunay ([x1,y1], [x2,y2], .....
points= np.dstack(np.meshgrid(x, y)).reshape(-1, 2)
 
## Delaunay triangulation and plot
tri = Delaunay(points,incremental='True')

# Access Each Points
print(tri.points)
# Access Node-to-Node Pointers
print(tri.neighbors)
# Access Face-to-Node Pointers
print(tri.simplices)

plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
plt.plot(points[:,0], points[:,1], 'o')
plt.show()
