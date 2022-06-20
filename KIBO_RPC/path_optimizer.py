#This code is mostly physical labor of smashing my fingers against the keyboard and very little actual programming
#TODO: Make this code not bad

import math
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
import random
import time
from tqdm import tqdm, trange

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
    
def generatePath(point1, point2, goal_reach, reach, r):
    unsuccessful = True
    fails = 0
    #Keeps trying until it's able to create a path under 20000 datapoints
    while unsuccessful:
        path = [point1]
        
        #Keeps randomly iterating until it reaches the final point
        #while distanceToPoint(path[i], point2) >= goal_reach:
        for i in trange(50000):
            invalid = True
            while invalid: #Keeps generating possible new waypoints until it finds a valid one
                new_point = generateRandomPoint(path[i], reach)
                invalid = detectCollision(new_point, r)
            path.append(new_point)
            if distanceToPoint(path[i], point2) <= goal_reach: #this has to run in order for the path to be successful
                unsuccessful = False
                break
            i += 1
        
        #Prints this message every time the loop repeats
        if unsuccessful:
            fails += 1
            print("\nFAILURE " + str(fails) + ": Path exceeded iteration number, attempting to generate another path...", flush=True)
            
    return path

def distanceToPoint(point1, point2):
    sum = 0
    n_dim = 3
    for i in range(n_dim):
        sum += (point1[i] - point2[i])**2 #does this for each dimension so you get 3d euclidean distance
    distance = math.sqrt(sum)
    return distance

def generateRandomPoint(loc_astrobee, reach): #reach is how far the point is from the original point
    #get random coordinates using gaussian distribution
    mu = 0
    sigma = 10
    coord = [0.0, 0.0, 0.0]
    for index in range(len(coord)):
        coord[index] = random.gauss(mu, sigma)
    
    #Find the normalization factor thingy
    temp = math.sqrt(coord[0]**2+coord[1]**2+coord[2]**2)
    if temp == 0:
        print("The normalization divisor somehow equaled zero, shit's boutta go down")
        normalizer = 1
    else:
        normalizer = 1/temp
    
    #Normalize all the coordinates
    for index in range(len(coord)):
        coord[index] = coord[index] * normalizer * reach
    
    #Add current positional value
    for index in range(len(loc_astrobee)):
        coord[index] += loc_astrobee[index]
        
    return coord

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
scatterPlotPoints(axis, point_1, point_2, loc_astrobee)
plotKOZ(axis)
plotAstrobee(axis, loc_astrobee, r)

#TODO: REMOVE THIS, purely for debugging purposes
#temp = []
#for i in tqdm(range(1000), desc="generating random points"):
#    temp.append(generateRandomPoint(loc_astrobee, 5))#5 is extreme, the real value is ~0.01, this is just for demo purposes
#scatterPlotList(axis, temp)
path = generatePath(point_1, point_2, 0.2, 0.01, r)
scatterPlotList(axis, path)
