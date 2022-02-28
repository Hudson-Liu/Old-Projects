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
import numpy as np

#input array cannot be ragged, though idk why it would be
def k_medoids(array, clusters, dimensions, iterations):
    #dimensionality reduction
    pca = PCA(n_components=2)
    array = pca.fit_transform(array)
    
    #k medoids clustering
    for i in range(0, iterations):
        medoids = KMedoids(n_clusters = clusters, metric = 'euclidean', max_iter = 300).fit(array)
        centroids = medoids.cluster_centers_
        #find outliers
        points = np.zeros((len(data),len(data[0])), float)
        distances = np.zeros((len(data),len(data[0])), float)
        for i in enumerate(centroids):
            #insert cdist stuff and then just replace parts of points and distances w/ it
            #use this: https://medium.datadriveninvestor.com/outlier-detection-with-k-means-clustering-in-python-ee3ac1826fb0
