# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 22:14:38 2022

A standard K-Medoid Algorithm, except it runs K-Medoids for multiple iterations,
removing outliers between each iteration. The function returns a trained
k_medoids object, that can then be used for predictions.

@author: hudso
"""
from sklearn_extra.cluster import KMedoids
import numpy as np
import math
import matplotlib.pyplot as plt

#returns trained kmedoids model
def k_medoids(array, clusters, iterations, percentile):
    #k medoids clustering
    removed = []
    removed = np.empty((0,0), float)
    for i in range(0, iterations + 1):
        #train on data w/o outliers
        medoids = KMedoids(n_clusters = clusters, max_iter = 300).fit(array)
        centroids = medoids.cluster_centers_
        
        #add back the removed points
        if (i != 0): #janky fix but it works
            array = np.append(array, removed, axis = 0)
        predictions = medoids.predict(array)
        
        #find distance from each datapoint to centroid
        distances = []
        dimensions = len(array[0])
        for l in range(0, len(array)): #for each datapoint
            respective_centroid = centroids[predictions[l]] #find the corresponding centroid for the given datapoint
            distance = 0
            for j in range(0, dimensions): #and calculate the distance to the centroid between the two
                distance = distance + ((array[l][j] - respective_centroid[j]) ** 2)
            distances.append(math.sqrt(distance))
        
        #remove the biggest distances from the list
        sort_ind = np.argsort(distances)
        chunk = int((1.0 - percentile) * len(sort_ind)) + 1
        remove = sort_ind[-chunk:]
        remove = np.sort(remove) #needs to be sorted or else messes up indexing
        remove = np.flip(remove)
        removed = []
        for e in range(0, len(remove)):
            removed.append(array[remove[e]])
            array = np.delete(array, remove[e], axis=0)
        removed = np.array(removed)

    if dimensions == 2:
        plt.title("K-Medoids Algorithm Results")
        
        x_data = array[:,0]
        y_data = array[:,1]
        
        x_centroids = centroids[:,0]
        y_centroids = centroids[:,1]
        
        x_outliers = removed[:,0]
        y_outliers = removed[:,1]
        
        plt.scatter(x_outliers, y_outliers, marker="*", c = "red")
        plt.scatter(x_data, y_data, c = medoids.labels_.astype(float), marker = ".") #converts labels into colors
        plt.scatter(x_centroids, y_centroids, marker="o", c = "blue")
        
        plt.legend(["Outliers", "Datapoints", "Centroids"], loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
        plt.show()
        
    return medoids

#stuff below can be removed, it's just to demonstrate proper inputs
array = np.random.rand(200,2)
clusters = 5
iterations = 5
percentile = 0.9

trained_model = k_medoids(array, clusters, iterations, percentile)
