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

#input array cannot be ragged, though idk why it would be
def k_medoids(array, clusters, iterations):
    
    
    #k medoids clustering
    for i in range(0, iterations):
        distances = findDistances(array)
        medoids = KMedoids(n_clusters = clusters, metric = 'precomputed', max_iter = 300).fit(distances)
        centroids = medoids.cluster_centers_
        #figure out how to correlate distances to the points that they're between
        #the kmedoid algorithm relies upon clustering points, not distances, so we have to be able to 
        #correspond those points to the distances that are representing them
        
        #find outliers
        points = np.zeros((len(array),len(array[0])), float)
        distances = np.zeros((len(array),len(array[0])), float)
        #for i in enumerate(centroids):
            
            #insert cdist stuff and then just replace parts of points and distances w/ it
            #use this: https://medium.datadriveninvestor.com/outlier-detection-with-k-means-clustering-in-python-ee3ac1826fb0

def findDistances(array):
    distances = []
    dimensions = len(array[0])
    for element in range(0, len(array)):
        for complement in range(element, len(array)):
            distance = 0
            for i in range(0, dimensions):
                distance = distance + (array[element][i] - array[complement][i]) ** 2
            distances.append(math.sqrt(distance))
    return distances
