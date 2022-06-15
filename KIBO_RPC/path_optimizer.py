#This code is mostly physical labor of smashing my fingers against the keyboard and very little actual programming
#TODO: Make this code not bad

import math
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from sklearn import discriminant_analysis

def detectCollision(loc_astrobee): #detects if astrobee's location is within KOZ
    koz_1 = [[9.8585,-9.45,4.82],[12.0085,-8.5,4.8706]]
    koz_2 = [[9.8673,-9.18813,3.81957],[10.767,-8.288,4.82]]
    koz_3 = [[11.1067,-9.44819,4.87385],[12.0067,-8.89819,5.87385]]

    if ((not doesCubeIntersectSphere(koz_1, loc_astrobee)) and (not doesCubeIntersectSphere(koz_2, loc_astrobee)) and (not doesCubeIntersectSphere(koz_3, loc_astrobee))):
        return False #no collision
    else:
        return True #oopsie u done messed up

#True means they intersect, False means that they don't (if you didn't realize that already you probably shouldn't be reading this code)
def doesCubeIntersectSphere(koz, s):
    width = 0.25
    length = 0.25
    height = 0.25
    r = math.sqrt(width**2+length**2+height**2) #The robot also rotates so we should treat it as a sphere

    c1 = koz[0]
    c2 = koz[1]

    dist_sqr = r**2
    if (s[0] < c1[0]):
        dist_sqr -= (s[0] - c1[0])**2
    elif (s[0] > c2[0]):
        dist_sqr -= (s[0] - c2[0])**2
    
    if (s[1] < c1[1]):
        dist_sqr -= (s[1] - c1[1])**2
    elif (s[1] > c2[1]):
        dist_sqr -= (s[1] - c2[1])**2
    
    if (s[2] < c1[2]):
        dist_sqr -= (s[2] - c1[2])**2
    elif (s[2] > c2[2]):
        dist_sqr -= (s[2] - c2[2])**2

    print(dist_sqr)
    return dist_sqr > 0

def plotKOZ(ax):
    koz_1 = [[9.8585,-9.45,4.82],[12.0085,-8.5,4.8706]]
    koz_2 = [[9.8673,-9.18813,3.81957],[10.767,-8.288,4.82]]
    koz_3 = [[11.1067,-9.44819,4.87385],[12.0067,-8.89819,5.87385]]
    
    plotRectangle(koz_1[0], koz_1[1], ax)
    plotRectangle(koz_2[0], koz_2[1], ax)
    plotRectangle(koz_3[0], koz_3[1], ax)

#i'm stealing so much code from google that it should be considered robbery
def plotRectangle(c1, c2, ax):
    all_c = calculateOtherCorners(c1, c2)
    np_c = np.array(all_c)
    r = [-1, 1]
    X, Y = np.meshgrid(r, r)
    print(np_c)
    ax.scatter3D(np_c[:, 0], np_c[:, 1], np_c[:, 2])
    verts = [[np_c[0],np_c[1],np_c[2],np_c[3]], #dear anyone with eyes
    [np_c[4],np_c[5],np_c[6],np_c[7]], #i apologize
    [np_c[0],np_c[1],np_c[5],np_c[4]],
    [np_c[2],np_c[3],np_c[7],np_c[6]],
    [np_c[1],np_c[2],np_c[6],np_c[5]],
    [np_c[4],np_c[7],np_c[3],np_c[0]]]
    ax.add_collection3d(Poly3DCollection(verts, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.20))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

#Behold: The Hudson-wants-to-kill-himself-inator
def calculateOtherCorners(c1, c2): #Calculates all the other corners of a rectangle formed from two opposite corners
    all_c = [0,0,0,0,0,0,0,0]

    #floor
    all_c[0] = [c1[0], c1[1], c1[2]]
    all_c[1] = [c1[0], c2[1], c1[2]]
    all_c[2] = [c2[0], c2[1], c1[2]]
    all_c[3] = [c2[0], c1[1], c1[2]]
    
    #ceil
    all_c[4] = [c1[0], c1[1], c2[2]]
    all_c[5] = [c1[0], c2[1], c2[2]]
    all_c[6] = [c2[0], c2[1], c2[2]]
    all_c[7] = [c2[0], c1[1], c2[2]]
    
    return all_c

def scatterPlotPoints(ax, *args):
    x = []
    y = []
    z = []
    for point in args:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax.scatter3D(x, y, z, cmap='Greens')

loc_astrobee = [0,0,0]
point_1 = [10.71, -7.5-0.2725783682, 4.48]
point_2 = [11.2746-0.0713120911,-9.92284, 5.29881+0.1626665617]

fig = plt.figure()
axis = fig.add_subplot(111, projection='3d')
scatterPlotPoints(axis, point_1, point_2, loc_astrobee)

collide = detectCollision(loc_astrobee)
plotKOZ(axis)
