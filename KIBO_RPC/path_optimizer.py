#kill me
#why did i do this
#hudson you're an idiot
#ya i know that already

import math
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
from sklearn import discriminant_analysis

width = 0.25
length = 0.25
height = 0.25
radius = math.sqrt(width**2+length**2+height**2) #The robot also rotates so we should treat it as a sphere

loc_astrobee = [0, 0, 0]
point_1 = [10.71, -7.5-0.2725783682, 4.48]
point_2 = [11.2746-0.0713120911,-9.92284, 5.29881+0.1626665617]

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D([point_1[0], point_2[0]], [point_1[1], point_2[1]], [point_1[2], point_2[2]], cmap='Greens');
def detectCollision(loc_astrobee):
    #corners[x,y,z=left/right, bottom/top, floor/ceil]: floor bottom left, floor top left, floor top right, floor bottom right, ceil bottom left, etc.
    #find which corner is the closest
    corners = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
    dist_corners = []
    for i in corners:
        dist_corners.append(math.sqrt(
            (i[0]-loc_astrobee[0])**2 +
            (i[1]-loc_astrobee[1])**2 +
            (i[2]-loc_astrobee[2])**2
            ))

    closest = np.argsort(dist_corners)[0]
    """
    cursor = corners[closest]
    cursors = [[cursor[0] + 0.1, cursor[1], cursor[2]],
              [cursor[0], cursor[1] + 0.1, cursor[2]],
              [cursor[0], cursor[1], cursor[2] + 0.1]]
    
    #find which direction to raverse
    dist_direc = []
    for i in cursors:
        dist_direc.append(math.sqrt(
            (i[0]-loc_astrobee[0])**2 +
            (i[1]-loc_astrobee[1])**2 +
            (i[2]-loc_astrobee[2])**2
            ))

    direct = np.argsort(dist_direc)[0] #0 = x, 1 = y, 2 = z
    """

    cursor = corners[closest]
    if (cursor == closest):

