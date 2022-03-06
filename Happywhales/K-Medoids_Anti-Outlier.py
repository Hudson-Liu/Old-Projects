# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 22:14:38 2022

Make a k-medoids clustering algorithm given a set of points in n-dimensional space (for some variable n that will be an argument for your function). 
Once the first clustering/centroid finding is done, eliminate the 10-20% of points in each cluster farthest from the centroids and redo clustering 
without them. Then use the new centroids to add those points back in to their clusters. Do this 1 or 2 times. This should allow us to not be so 
influenced by points that are outliers or aren't representative of the overall data

@author: hudso
"""
from sklearn_extra.cluster import KMedoids
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances
import numpy as np
import math
import warnings
import matplotlib.pyplot as plt

#returns trained kmedoids model
#input array cannot be ragged, though idk why it would be
def k_medoids(array, clusters, iterations):
    #k medoids clustering
    for i in range(0, iterations + 1):
        distances = findDistances(array)
        medoids = KMedoids(n_clusters = clusters, max_iter = 300).fit(x)
        clusters = medoids.fit_predict(distances)
        centroids = medoids.cluster_centers_
        return centroids
        
        #find outliers
        points = np.zeros((len(array),len(array[0])), float)
        distances = np.zeros((len(array),len(array[0])), float)
        for i in enumerate(centroids):
            #distances = np.append(distances, cdist([center_elem],data[clusters == i], 'euclidean')) 
            #insert cdist stuff and then just replace parts of points and distances w/ it
            #use this: https://medium.datadriveninvestor.com/outlier-detection-with-k-means-clustering-in-python-ee3ac1826fb0

#given points to classify and the model returned by k_medoids function
def prediction(array, medoids):
    distances = findDistToCentroid(array, medoids.cluster_center_)  
    return medoids.predict(distances)

#i just now realized that the sklearn function "pairwise_distances" does exactly this
def findDistances(array):
    distances = []
    dimensions = len(array[0])
    for element in range(0, len(array)):
        distances.append([])
        for complement in range(0, len(array)): #replace 0 with elements to remove repeats
            distance = 0
            for i in range(0, dimensions):
                distance = distance + ((array[element][i] - array[complement][i]) ** 2)
            distances[element].append(math.sqrt(distance))
    distances = np.array(distances)
    return distances

#private, only ran by class
def findDistToCentroid(array, centroids):
    distances = []
    dimensions = len(array[0])
    for element in range(0, len(array)):
        distances.append([])
        for complement in range(0, len(centroids)): #replace 0 with elements to remove repeats
            distance = 0
            for i in range(0, dimensions):
                distance = distance + ((array[element][i] - centroids[complement][i]) ** 2)
            distances[element].append(math.sqrt(distance))
    distances = np.array(distances)
    return distances

array = [[2,3,5,3],[3,4,5,2],[2,3,4,5]]
array = [[1, 2], [2, 2], [2, 3], [8, 7], [8, 9], [7, 9], [7, 7], [12,10], [25, 24], [24, 24], [24, 25], [25, 25], [25,20], [20,25]]
spaghet = findDistances(array)
centroids = k_medoids(array, 1, 1)
