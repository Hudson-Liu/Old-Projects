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
from PIL import ImageDraw, ImageFont
import PIL
import matplotlib.pylab as pl

class Modified_KMedoids:
    #returns trained kmedoids model
    def k_medoids(self, array, num_clusters, iterations, percentile):
        #k medoids clustering
        removed = []
        history = []
        removed = np.empty((0,0), float)
        for i in range(0, iterations + 1):
            #train on data w/o outliers
            medoids = KMedoids(n_clusters = clusters, max_iter = 300).fit(array)
            centroids = medoids.cluster_centers_
            
            #add back the removed points
            if (i != 0): #janky fix but it works
                history.append([array, centroids, removed, medoids])
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
            images = []
            customFont = ImageFont.truetype("arial.ttf", 24)
            for i in range(iterations):
                fig = self.two_dim_vis(history[i][0], history[i][1], history[i][2], history[i][3], num_clusters)
                fig.canvas.draw() #Depending on the backend, the canvas is not automatically drawn, and hence needs to first be manually drawn
                image = PIL.Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
                manipulable_image = ImageDraw.Draw(image)
                manipulable_image.text((10, 10), "Iteration Number: " + str(i + 1), font = customFont, fill=(0, 0, 0))
                images.append(image)
                
            first_img = images[0]
            first_img.save(fp='clustering.gif', format='GIF', append_images=images, save_all=True, duration=300, loop=0)
            #ani.save('animation.gif', writer='pillow')
            
        return medoids
    
    #The name is short for "Two Dimensional Visualization"; visualizes 2d clusters using MatPlotLib
    def two_dim_vis(self, array, centroids, removed, medoids, num_clusters):
        fig = plt.figure(figsize=(7, 7))
        ax = plt.axes(xlim=(0,1),ylim=(0,1))
        ax.set_title("K-Medoids Algorithm Results")
            
        x_data = array[:,0]
        y_data = array[:,1]
        
        x_centroids = centroids[:,0]
        y_centroids = centroids[:,1]
        
        x_outliers = removed[:,0]
        y_outliers = removed[:,1]
        
        predictions = medoids.labels_.astype(float)
        colors = [(pred/num_clusters) for pred in predictions]
        colors = pl.cm.viridis(colors)
        
        index = 0
        for point in array:
            corresponding_centroid = int(predictions[index])
            x = [point[0], x_centroids[corresponding_centroid]]
            y = [point[1], y_centroids[corresponding_centroid]]
            plt.plot(x, y, c=colors[index], alpha=0.2)
            index += 1
        
        ax.scatter(x_outliers, y_outliers, marker="*", c = "red", label='Outliers')
        ax.scatter(x_data, y_data, c = colors, cmap='brg', marker = ".", label="Datapoints") #converts labels into colors
        ax.scatter(x_centroids, y_centroids, marker="o", c = "black", label="Centroids")
        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
        plt.show()
        return fig
    
#executes the kmedoids class on a 2d randomly generated array for demo purposes
num_datapoints = int(input("How many Datapoints would you like to cluster? ")) #2000
array = np.random.rand(num_datapoints, 2)
clusters = int(input("How many clusters would you like to create? ")) #8
iterations = int(input("How many iterations would you like to run the outlier algorithm for? ")) #30
percentile = float(input("What percentile (Out of 100) should the outliers be in? "))/100.0 #90

kmedoids = Modified_KMedoids()
trained_model = kmedoids.k_medoids(array, clusters, iterations, percentile)
