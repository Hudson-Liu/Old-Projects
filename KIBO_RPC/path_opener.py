# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 14:53:01 2022

opens path generated by A* algorithm

@author: hudso
"""
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
import pickle
import math

with open('path', 'rb') as f:
    path = pickle.load(f)
with open("closed_points", "rb") as f:
    closed_points = pickle.load(f)
    
def scatterPlotPoints(ax, color, *args):
    x = []
    y = []
    z = []
    for point in args:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax.scatter3D(x, y, z, c=color)


def scatterPlotList(ax, color, points):
    x = []
    y = []
    z = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax.scatter3D(x, y, z, c=color)

def plotKOZ(ax):
    koz_1 = [[9.8585,-9.45,4.82],[12.0085,-8.5,4.8706]]
    koz_2 = [[9.8673,-9.18813,3.81957],[10.767,-8.288,4.82]]
    koz_3 = [[11.1067,-9.44819,4.87385],[12.0067,-8.89819,5.87385]]
    
    xbounds = [10, 13]
    ybounds = [-7, -11]
    zbounds = [4, 6]
    
    plotRectangle(koz_1[0], koz_1[1], ax)
    plotRectangle(koz_2[0], koz_2[1], ax)
    plotRectangle(koz_3[0], koz_3[1], ax)
    plotRectangle([xbounds[0],ybounds[0],zbounds[0]], [xbounds[1],ybounds[1],zbounds[1]], ax)

#i'm stealing so much code from google that it should be considered robbery
def plotRectangle(c1, c2, ax):
    all_c = calculateOtherCorners(c1, c2)
    np_c = np.array(all_c)
    r = [-1, 1]
    X, Y = np.meshgrid(r, r)
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

def distanceToPoint(point1, point2):
    sum = 0
    n_dim = 3
    for i in range(n_dim):
        sum += (point1[i] - point2[i])**2 #does this for each dimension so you get 3d euclidean distance
    distance = math.sqrt(sum)
    return distance

plottable = []
for i in closed_points:
    plottable.append(i[0])
    
fig = plt.figure()
axis = fig.add_subplot(111, projection='3d')

scatterPlotList(axis, "b", path)
#scatterPlotList(axis, "r", plottable)
plotKOZ(axis)

#THE DISTANCE TO BEAT: 2.95 meters from point1 to point2
#A* BEST: 3.61 meters
total_dist = 0
for i in range(len(path) - 1):
    total_dist += distanceToPoint(path[i], path[i+1])

print(total_dist)

axis.set_box_aspect([ub - lb for lb, ub in (getattr(axis, f'get_{a}lim')() for a in 'xyz')])
plt.show()
