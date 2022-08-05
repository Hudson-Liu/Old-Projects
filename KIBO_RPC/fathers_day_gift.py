#READ THIS:
#THIS IS THE A* VERISON OF THE CODE
#this is meant to have a smaller jump dist but not perfect

#This code is mostly physical labor of smashing my fingers against the keyboard and very little actual programming
#TODO: Make this code not physically hurt my eyes

import math
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
from tqdm import trange, tqdm
import itertools
import pickle
import imageio
import os

def detectCollision(loc_astrobee, r): #detects if astrobee's location is within KOZ
    kozs = [[[0,0,0],[1,1,3]], #H
           [[0,1,1],[1,2,2]],
           [[0,2,0],[1,3,3]],
           [[-3,4,0],[-2,5,3]], #A
           [[-3,5,2.5],[-2,6,3]],
           [[-3,5,1],[-2,6,1.5]],
           [[-3,6,0],[-2,7,3]],
           [[-5,8,0],[-4,8.5,3]], #N
           [[-5,8.5,2],[-4,9,3]],
           [[-5,9,1],[-4,9.5,2]],
           [[-5,9.5,0],[-4,10,1]],
           [[-5,10,0],[-4,10.5,3]]]
    
    #Detect collision w/ KOZ
    for zone in kozs:
        if doesCubeIntersectSphere(zone, loc_astrobee, r):
            return True
    
    #Detect out of bounds
    xbounds = [-6, 2]
    ybounds = [-1, 11]
    zbounds = [0, 3]
    if outOfBounds(loc_astrobee, xbounds, ybounds, zbounds):
        return True
    
    return False

def outOfBounds(loc_astrobee, xbounds, ybounds, zbounds):
    if ((loc_astrobee[0] < xbounds[0] or loc_astrobee[0] > xbounds[1]) or
         loc_astrobee[1] < ybounds[0] or loc_astrobee[1] > ybounds[1] or
         loc_astrobee[2] < zbounds[0] or loc_astrobee[2] > zbounds[1]):
        return True
    else:
        return False
    
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
    #Plot KOZs
    kozs = [[[0,0,0],[1,1,3]], #H
           [[0,1,1],[1,2,2]],
           [[0,2,0],[1,3,3]],
           [[-3,4,0],[-2,5,3]], #A
           [[-3,5,2.5],[-2,6,3]],
           [[-3,5,1],[-2,6,1.5]],
           [[-3,6,0],[-2,7,3]],
           [[-5,8,0],[-4,8.5,3]], #N
           [[-5,8.5,2],[-4,9,3]],
           [[-5,9,1],[-4,9.5,2]],
           [[-5,9.5,0],[-4,10,1]],
           [[-5,10,0],[-4,10.5,3]]]
    
    for zone in kozs:
        plotRectangle(zone[0],zone[1],ax)
        
    #Plot boundary box
    xbounds = [-6, 2]
    ybounds = [-1, 11]
    zbounds = [0, 3]
    
    plotRectangle([xbounds[0],ybounds[0],zbounds[0]], [xbounds[1],ybounds[1],zbounds[1]], ax, 0.0)

#i'm stealing so much code from google that it should be considered robbery
def plotRectangle(c1, c2, ax, a=0.2):
    all_c = calculateOtherCorners(c1, c2)
    np_c = np.array(all_c)
    r = [-1, 1]
    X, Y = np.meshgrid(r, r)
    ax.scatter3D(np_c[:, 0], np_c[:, 1], np_c[:, 2], c="b")
    verts = [[np_c[0],np_c[1],np_c[2],np_c[3]], #dear anyone with eyes
    [np_c[4],np_c[5],np_c[6],np_c[7]], #i apologize
    [np_c[0],np_c[1],np_c[5],np_c[4]],
    [np_c[2],np_c[3],np_c[7],np_c[6]],
    [np_c[1],np_c[2],np_c[6],np_c[5]],
    [np_c[4],np_c[7],np_c[3],np_c[0]]]
    ax.add_collection3d(Poly3DCollection(verts, facecolors='cyan', linewidths=0.75, edgecolors='b', alpha=a))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

#The link below is the poor guy i stole this code from
#https://stackoverflow.com/questions/40460960/how-to-plot-a-sphere-when-we-are-given-a-central-point-and-a-radius-size
def plotAstrobee(ax, loc_astrobee, r, n_meridians = 20, n_circles_latitude = None, camera_angle = 0):
    if n_circles_latitude is None:
        n_circles_latitude = max(n_meridians/2, 4)
    u, v = np.mgrid[0:2*np.pi:n_meridians*1j, 0:np.pi:n_circles_latitude*1j]
    sphere_x = loc_astrobee[0] + r * np.cos(u) * np.sin(v)
    sphere_y = loc_astrobee[1] + r * np.sin(u) * np.sin(v)
    sphere_z = loc_astrobee[2] + r * np.cos(v)
    #ax.plot_wireframe(sphere_x, sphere_y, sphere_z, color="w", edgecolor="r", linewidths=0.75, alpha=0.8)
    #ax.plot_surface(sphere_x, sphere_y, sphere_z, color="w", edgecolor="r", linewidths=0.75, alpha=0.8)
    ax.plot_surface(sphere_x, sphere_y, sphere_z, color="w", alpha=1, zorder=2.5)
    
    y_ranged = np.arange((-1*(0.5 * r)), (0.5 * r), 0.02) #this is the y range, but not adjusted for loc_astrobee
    y_data = np.array([i + loc_astrobee[1] for i in y_ranged]) #this is the y range adjusted for loc_astrobee
    z_data = (5*(y_ranged**2)) + (loc_astrobee[2] - 0.15) #both z range and x range use the non adjusted y range
    x_data = (-1*(y_ranged**2)) + (loc_astrobee[0] + 0.4)
    
    lEyeY = loc_astrobee[1] + 0.08
    rEyeY = loc_astrobee[1] - 0.08
    EyeZ = loc_astrobee[2] + 0.1
    EyeX = loc_astrobee[0] + 0.42
    
    if camera_angle < 180: #TODO: Replace this placeholder with the actual backwards camera angle range
        ax.scatter(EyeX, lEyeY, EyeZ, color="black",zorder=3)    
        ax.scatter(EyeX, rEyeY, EyeZ, color="black",zorder=3)
        ax.plot(x_data,y_data,z_data,linewidth=4,color="black",zorder=3)
    else:
        ax.plot(x_data,y_data,z_data,linewidth=4,color="black")
    
    plt.show()

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
def scatterPlotPoints(ax, color, *args):
    x = []
    y = []
    z = []
    for point in args:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax.scatter3D(x, y, z, c=color)


def scatterPlotList(ax, color, points, s=20):
    x = []
    y = []
    z = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax.scatter3D(x, y, z, c=color, alpha=1, s=s)
    
#TODO: Replace sum keyword with something else
def distanceToPoint(point1, point2):
    sum = 0
    n_dim = 3
    for i in range(n_dim):
        sum += (point1[i] - point2[i])**2 #does this for each dimension so you get 3d euclidean distance
    distance = math.sqrt(sum)
    return distance

#call help
def generatePath(loc_astrobee, point2, jump_dist, iterations, r): #jump_dist is how far the astrobee can move per iteration of A*, this is essentially a measure of resolution
    MARGIN = jump_dist * 0.1
    open_list = [[loc_astrobee,distanceToPoint(loc_astrobee, point2),0,[0,0,0],distanceToPoint(loc_astrobee, point2)]] #[[[coordinate], f_cost, g_cost, parent, h_cost]]
    closed = []
    selected_node = []
    for _ in trange(iterations, desc="Iterations of A* Algorithm"):
        # Finds the index of the best open_list node with the least f_cost
        best_f = open_list[0][1]
        best_h = open_list[0][4]
        best_index = 0
        for index in range(len(open_list)):
            if open_list[index][1] < best_f:
                best_f = open_list[index][1]
                best_h = open_list[index][4]
                best_index = index
            elif open_list[index][1] == best_f:
                if open_list[index][4] < best_h:
                    best_f = open_list[index][1]
                    best_h = open_list[index][4]#best_h isn't actually necessarily the best h_cost, but instead just the h_cost of the best f_cost
                    best_index = index

        #Appends this node to closed and removes it from open_list
        selected_node = open_list[best_index]
        open_list.pop(best_index)
        closed.append(selected_node)
        
        #Tests if selected node is goal
        if pointsAreEqual(selected_node[0], point2, jump_dist):
            break #if it has reached the goal, stop the algorithm
            
        #Generate children of current node (neighbors of current node)
        neighbors = generateNeighbors(selected_node[0], jump_dist)
        for child in neighbors:
            valid_node = True
            
            #Calculates g, h, and f cost
            child_g = selected_node[2] + jump_dist
            #child_g = selected_node[2] + distanceToPoint(selected_node[0], child) #this is a weird function that has weird behavior and might be useful?
            child_h = distanceToPoint(child, point2)
            child_f = child_g + child_h

            #Check if child will collide with KOZ
            if detectCollision(child, r):#TODO: Change this to detectCollision()
                valid_node = False

            #Check if child is on closed
            for point in closed:
                if pointsAreEqual(child, point[0], MARGIN):
                    valid_node = False #Skip the point and move onto the next one

            #Check if the child is on open_list already
            remove_index = 0
            remove = False
            for index in range(len(open_list)):
                if pointsAreEqual(child, open_list[index][0], MARGIN):
                    if child_g <= open_list[index][2]: #If the new g cost is better than the previoius g cost, remove the old one so we can append the new one
                        remove_index = index #THIS HAS TO BE THE LAST STATEMENT BEFFORE THE VARIABLE IS APPENDED
                        remove = True
                    else:
                        valid_node = False
            if remove:
                open_list.pop(remove_index)
            
            #Appends child to open_list
            if valid_node:
                open_list.append([child, child_f, child_g, selected_node[0], child_h]) #both the coordinates and the f_cost
   
    #Find the closest waypoint to point2 and backtrace from there
    lowest_h = closed[0][4]
    selected_node = closed[0]
    i = 0
    for point in closed:
        if point[4] < lowest_h:
            lowest_h = point[4]
            selected_node = closed[i]
        i+=1
    path = backtracing(loc_astrobee, closed, selected_node, MARGIN)
    
    #Create a duplicate-removed version of closed
    closed_points = [i[0] for i in closed]
    plottable = []
    for point1 in closed_points:
        dont_append = False
        for point2 in path:
            if pointsAreEqual(point1, point2, MARGIN) or pointsAreEqual(point1, loc_astrobee, MARGIN):
                dont_append = True
        if not dont_append:
            plottable.append(point1) #plottable is a verison of closed without any of the duplicates of path
            
    return closed, plottable, path

def backtracing(loc_astrobee, closed, selected_node, MARGIN):
    #Performs backtracing and appends list of parents toward final goal
    path = []
    while True: #For all the nodes of the path
        for point in closed: #Find the current node's parent
            if pointsAreEqual(point[0], selected_node[3], MARGIN):
                selected_node = point
                break
        if pointsAreEqual(loc_astrobee, selected_node[0], MARGIN): #check if the parent is the starting node
            return path
        path.append(selected_node[0])

def pointsAreEqual(point1, point2, margin): #this accomodates for the intrinsic inaccuracy of floats
    for i in range(0, 3):
        if (abs(point1[i] - point2[i]) >= margin): #If a single of the x, y, or z coordinates are off then return false
            return False
    return True

def generateNeighbors(current_node, jump_dist):
    neighbors = []
    
    translator = list(itertools.product([0, jump_dist, -1*jump_dist], repeat=3))[1:] #the slice removes the first entry which is just empty
    for translate in translator:
        neighbors.append([current_node[0] + translate[0], #x
                          current_node[1] + translate[1], #y
                          current_node[2] + translate[2]])#z
    return neighbors

def saveAnimation(ax, path, r):
    i = 0
    past_loc = []
    future_loc = path.copy()
    ax.view_init(30,30)
    cwd = os.getcwd()
    if not os.path.exists(cwd + r"\Frames"):
        os.makedirs(cwd + r"\Frames")

    for loc_astrobee in tqdm(path, desc="Path Animation: "):
        plt.cla()
        #Plots Astrobee and KOZs
        plotAstrobee(ax, loc_astrobee, r)
        plotKOZ(ax)
        if not (future_loc is None):
            future_loc.remove(loc_astrobee)
            
        #Plots paths and center of astrobee
        scatterPlotList(ax, "r", past_loc)
        scatterPlotList(ax, "black", [loc_astrobee], 50)
        if not (future_loc is None):
            scatterPlotList(ax, "b", future_loc)
        
        #Saves frame
        plt.savefig(cwd + r"\Frames\Frame " + str(i), dpi=120, bbox_inches='tight')
        past_loc.append(loc_astrobee)
        
        i += 1
    
    images = []
    for counter in range(len(path)):
        images.append(imageio.imread(cwd + r"\Frames\Frame " + str(counter) + ".png"))
    imageio.mimsave('movie.gif', images)
    
point_1 = [1.75, 1, 1.5]
point_2 = [-5.5, 9.75, 2.5]

#astrobee bounding box definition
width = 0.25
length = 0.25
height = 0.25
r = math.sqrt(width**2+length**2+height**2) #The robot also rotates so we should treat it as a sphere

#collide = detectCollision([10.71, -7.5-0.2725783682, 4.48], r)

fig = plt.figure()
axis = fig.add_subplot(111, projection='3d', computed_zorder=False)

#visualizing everything
#scatterPlotPoints(axis, point_1, point_2, loc_astrobee)
scatterPlotPoints(axis, "g", point_1, point_2)
plotKOZ(axis)
#plotAstrobee(axis, loc_astrobee, r)

figure = plt.gcf()  # get current figure
figure.set_size_inches(32, 18)

closed, plottable, path = generatePath(point_1, point_2, 0.1, 100, r) #original 0.03 20000
axis.set_box_aspect([ub - lb for lb, ub in (getattr(axis, f'get_{a}lim')() for a in 'xyz')])
saveAnimation(axis, path, r)
#scatterPlotList(axis, "b", path)
#scatterPlotList(axis, "r", plottable)
#scatterPlotPoints(axis, "g", point_1, point_2)

#Saves the path and closed opints
with open("path", "wb") as fp:
    pickle.dump(path, fp)
with open("closed_points", "wb") as fp:
    pickle.dump(closed, fp)
