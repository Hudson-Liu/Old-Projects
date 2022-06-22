#This code is mostly physical labor of smashing my fingers against the keyboard and very little actual programming
#TODO: Make this code not bad

import math
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
import random
import time
from tqdm import tqdm, trange
import itertools

def detectCollision(loc_astrobee, r): #detects if astrobee's location is within KOZ
    koz_1 = [[9.8585,-9.45,4.82],[12.0085,-8.5,4.8706]]
    koz_2 = [[9.8673,-9.18813,3.81957],[10.767,-8.288,4.82]]
    koz_3 = [[11.1067,-9.44819,4.87385],[12.0067,-8.89819,5.87385]]

    if ((not doesCubeIntersectSphere(koz_1, loc_astrobee, r)) and (not doesCubeIntersectSphere(koz_2, loc_astrobee, r)) and (not doesCubeIntersectSphere(koz_3, loc_astrobee, r))):
        return False #no collision
    else:
        return True #u done messed up

#True means they intersect, False means that they don't (if you didn't realize that already you probably shouldn't be reading this code)
def doesCubeIntersectSphere(koz, s, r):
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

#The link below is the poor guy i stole this code from
#https://stackoverflow.com/questions/40460960/how-to-plot-a-sphere-when-we-are-given-a-central-point-and-a-radius-size
def plotAstrobee(ax, loc_astrobee, r, n_meridians = 20, n_circles_latitude = None):
    if n_circles_latitude is None:
        n_circles_latitude = max(n_meridians/2, 4)
    u, v = np.mgrid[0:2*np.pi:n_meridians*1j, 0:np.pi:n_circles_latitude*1j]
    sphere_x = loc_astrobee[0] + r * np.cos(u) * np.sin(v)
    sphere_y = loc_astrobee[1] + r * np.sin(u) * np.sin(v)
    sphere_z = loc_astrobee[2] + r * np.cos(v)
    ax.plot_surface(sphere_x, sphere_y, sphere_z, color="w", edgecolor="r")
    #ax.plot_surface(sphere_x, sphere_y, sphere_z, color="r", alpha=0.5)

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

#Just a simple plotting function that automatically converts a variable sized list of points into 5
def scatterPlotPoints(ax, *args):
    x = []
    y = []
    z = []
    for point in args:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax.scatter3D(x, y, z, cmap='Greens')

#Overloading the function to also support lists of points instead of just variable sized parameter lists
def scatterPlotList(ax, points):
    x = []
    y = []
    z = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax.scatter3D(x, y, z, cmap='Greens')
    
def distanceToPoint(point1, point2):
    sum = 0
    n_dim = 3
    for i in range(n_dim):
        sum += (point1[i] - point2[i])**2 #does this for each dimension so you get 3d euclidean distance
    distance = math.sqrt(sum)
    return distance

def generatePath(loc_astrobee, point2, jump_dist): #jump_dist is how far the astrobee can move per iteration of A*, this is essentially a measure of resolution
    MARGIN = 0.001 #margin of error for float calculations
    open = [[[]]] #[[[coordinate], f_cost]]
    closed = []
    g_cost = 0
    h_cost = 0
    f_cost = 0

    open[0][0] = loc_astrobee #first currentNode is startNote of astrobee

    while len(open) != 0: #while there are still more nodes to check
        # Finds the index of the best open node with the least f_cost
        best_f = open[0][0]
        best_index = 0
        for index in range(len(open)):
            if open[index][1] <= best_f: #point 1 is the f_cost of the point
                best_f = open[index][1]
                best_index = index
        
        #Appends this node to closed and removes it from open
        selected_node = open[best_index]
        open.pop(best_index)
        closed.append(selected_node)

        #Tests if selected node is goal
        if pointsAreEqual(selected_node, point2, MARGIN):
            #insert shit
            print("placeholder for backtracing code")
        
        #Generate children of current node (neighbors of current node)
        neighbors = generateNeighbors(selected_node[0], jump_dist)
        for child in neighbors:
            #Calculates g, h, and f cost
            child_g = g_cost + distanceToPoint(selected_node[0], child) 
            child_h = distanceToPoint(selected_node[0], point2) 
            child_f = child_g + child_h

            #Check if child is on closed
            for point in closed:
                if pointsAreEqual(child, point, MARGIN): #add if child g is better than past g
                    continue #Skip the point and move onto the next one

            #Check if the child is on open already
            
            #Appends child to open
            open.append([child, child_f]) #both the coordinates and the f_cost


def pointsAreEqual(point1, point2, margin): #this accomodates for the intrinsic inaccuracy of floats
    for i in range(len(point1)):
        if (abs(point1[i] - point2[i]) >= margin): #If a single of the x, y, or z coordinates are off then return false
            return False
    return True

def generateNeighbors(current_node, jump_dist):
    neighbors = []
    
    #positive jump dist
    translator = list(itertools.product([0, jump_dist, -1*jump_dist], repeat=3))[1:] #the slice removes the first entry which is just empty
    for translate in translator:
        neighbors.append([current_node[0] + translate[0], #x
                          current_node[1] + translate[1], #y
                          current_node[2] + translate[2]])#z
    return neighbors

loc_astrobee = [12.0067,-8.89819,5.87385]
point_1 = [10.71, -7.5-0.2725783682, 4.48]
point_2 = [11.2746-0.0713120911,-9.92284, 5.29881+0.1626665617]

#astrobee bounding box definition
width = 0.25
length = 0.25
height = 0.25
r = math.sqrt(width**2+length**2+height**2) #The robot also rotates so we should treat it as a sphere

collide = detectCollision(loc_astrobee, r)

fig = plt.figure()
axis = fig.add_subplot(111, projection='3d')

#visualizing everything
"""
scatterPlotPoints(axis, point_1, point_2, loc_astrobee)
plotKOZ(axis)
plotAstrobee(axis, loc_astrobee, r)
"""

#TODO: REMOVE THIS, purely for debugging purposes
#temp = []
#for i in tqdm(range(1000), desc="generating random points"):
#    temp.append(generateRandomPoint(loc_astrobee, 5))#5 is extreme, the real value is ~0.01, this is just for demo purposes
#scatterPlotList(axis, temp)

#TODO: REMOVE THIS
#Testing the generateneighbors function
#neighbors = generateNeighbors(point_1, 1)
#scatterPlotList(axis, neighbors)
