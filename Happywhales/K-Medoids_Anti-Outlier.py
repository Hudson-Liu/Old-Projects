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
def k_medoids(array, clusters, iterations, percentile):
    #k medoids clustering
    removed = []
    for i in range(0, iterations + 1):
        #train on data w/o outliers
        medoids = KMedoids(n_clusters = clusters, max_iter = 300).fit(array)
        centroids = medoids.cluster_centers_
        
        #add back the removed points
        array.append(removed)
        predictions = medoids.predict(array)
        
        #find distance from each datapoint to centroid
        distances = []
        dimensions = len(array[0])
        for l in range(0, len(array)): #for each datapoint
            respective_centroid = centroids[predictions[l]] #find the corresponding centroid for the given datapoint
            distance = 0
            for i in range(0, dimensions): #and calculate the distance to the centroid between the two
                distance = distance + ((array[l][i] - respective_centroid[l][i]) ** 2)
            distances.append(math.sqrt(distance))
        
        #remove the biggest distances from the list
        sort_ind = np.argsort(distances)
        chunk = (1.0 - percentile) * len(sort_ind)
        remove = sort_ind[-chunk:]
        remove = np.sort(remove) #needs to be sorted or else messes up indexing
        remove = np.flip(remove)
        removed = []
        for e in range(0, len(remove)):
            removed.append(array.pop(remove[e]))
            
    return medoids
        #for i in enumerate(centroids):
            #distances = np.append(distances, cdist([center_elem],data[clusters == i], 'euclidean')) 
            #insert cdist stuff and then just replace parts of points and distances w/ it
            #use this: https://medium.datadriveninvestor.com/outlier-detection-with-k-means-clustering-in-python-ee3ac1826fb0



array = [[2,3,5,3],[3,4,5,2],[2,3,4,5]]
centroids, sume = k_medoids(array, 1, 1, 0.9)
