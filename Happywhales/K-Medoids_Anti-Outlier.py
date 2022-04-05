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
    @staticmethod
    def k_medoids(array, num_clusters, iterations, percentile):
        #k medoids clustering
        removed = []
        history = []
        removed = np.empty((0,0), float)
        dimensions = len(array[0])
        
        for i in range(0, iterations + 1):
            #train on data w/o outliers
            if (np.size(array, axis=0) != 0 and num_clusters < np.size(array, axis=0)):
                medoids = KMedoids(n_clusters = clusters, max_iter = 300).fit(array)
                centroids = medoids.cluster_centers_
            elif np.size(array, axis=0 == 0):
                error_message = "All datapoints have been identified as outliers in iteration {iteration}. The percentile is likely set too low."
                print(error_message.format(iteration = i))
                break
            else:
                error_message = "The number of datapoints is less than the number of clusters in iteration {iteration}"
                print(error_message.format(iteration = i))
                break
            
            #add back the removed points
            if (i != 0): #janky fix but it works
                if (np.size(removed, axis=0) != 0):
                    history.append([array, centroids, removed, medoids])
                    array = np.append(array, removed, axis = 0)
                else:
                    error_message = "No outliers have been detected in iteration {iteration}. The percentile is likely set too high."
                    print(error_message.format(iteration = i))
                    break
            predictions = medoids.predict(array)
            
            #find distance from each datapoint to centroid
            distances = []
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
    
        if dimensions in (2, 3): #if it's 2 or 3 dimensional
            images = []
            customFont = ImageFont.truetype("arial.ttf", 24)
            for i in range(iterations):
                if dimensions == 2 and np.size(history, axis=0) > 0:
                    fig = Modified_KMedoids.two_dim_vis(history[i][0], history[i][1], history[i][2], history[i][3], num_clusters)
                elif dimensions == 3 and np.size(history, axis=0) > 0:
                    fig = Modified_KMedoids.three_dim_vis(history[i][0], history[i][1], history[i][2], history[i][3], num_clusters)
                else:
                    print("The program failed on it's first iteration, so there is no data to display.")
                    break
                fig.canvas.draw() #Depending on the backend, the canvas is not automatically drawn, and hence needs to first be manually drawn
                image = PIL.Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
                manipulable_image = ImageDraw.Draw(image)
                manipulable_image.text((10, 10), "Iteration Number: " + str(i + 1), font = customFont, fill=(0, 0, 0))
                images.append(image)
            if (len(images) > 0):   
                first_img = images[0]
                first_img.save(fp='clustering.gif', format='GIF', append_images=images, save_all=True, duration=300, loop=0)
            else:
                print("No images were able to be created.")
        return medoids
    
    #The name is short for "Two Dimensional Visualization"; visualizes 2d clusters using MatPlotLib
    @staticmethod
    def two_dim_vis(array, centroids, removed, medoids, num_clusters):
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
    
    @staticmethod #NOTE TO SELF: Any function that doesn't use self can be a staticmethod, since it's independent of the instance of the class
    def three_dim_vis(array, centroids, removed, medoids, num_clusters):
        fig = plt.figure(figsize=(7, 7))
        ax = plt.axes(projection='3d')
        ax.set_title("K-Medoids Algorithm Results")
            
        x_data = array[:,0]
        y_data = array[:,1]
        z_data = array[:,2]
        
        x_centroids = centroids[:,0]
        y_centroids = centroids[:,1]
        z_centroids = centroids[:,2]
        
        x_outliers = removed[:,0]
        y_outliers = removed[:,1]
        z_outliers = removed[:,2]
        
        predictions = medoids.labels_.astype(float)
        colors = [(pred/num_clusters) for pred in predictions]
        colors = pl.cm.viridis(colors)
        
        index = 0
        for point in array:
            corresponding_centroid = int(predictions[index])
            x = [point[0], x_centroids[corresponding_centroid]]
            y = [point[1], y_centroids[corresponding_centroid]]
            z = [point[2], z_centroids[corresponding_centroid]]
            plt.plot(x, y, z, c=colors[index], alpha=0.2)
            index += 1
        
        ax.scatter(x_outliers, y_outliers, z_outliers, marker="*", c = "red", label='Outliers')
        ax.scatter(x_data, y_data, z_data, c = colors, cmap='brg', marker = ".", label="Datapoints") #converts labels into colors
        ax.scatter(x_centroids, y_centroids, z_centroids, marker="o", c = "black", label="Centroids")
        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
        plt.show()
        return fig
    
#executes the kmedoids class on a 2d randomly generated array for demo purposes
dimensions = int(input("How many dimensions would you like? (Visualization works only with 2 or 3 dimensions) "))
num_datapoints = int(input("How many datapoints would you like to cluster? ")) #2000
array = np.random.rand(num_datapoints, dimensions)
clusters = int(input("How many clusters would you like to create? ")) #8
iterations = int(input("How many iterations would you like to run the outlier algorithm for? ")) #30
percentile = float(input("What percentile (Out of 100) should the outliers be in? "))/100.0 #90

trained_model = Modified_KMedoids.k_medoids(array, clusters, iterations, percentile)
