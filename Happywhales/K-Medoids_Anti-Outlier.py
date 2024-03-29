# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 22:14:38 2022

A standard K-Medoid Algorithm, except it runs K-Medoids for multiple iterations,
removing outliers between each iteration. The function returns a trained
k_medoids object, that can then be used for predictions.

@author: [REMOVED]
"""

from sklearn_extra.cluster import KMedoids #This library was written by scikit-learn, this is their website: https://scikit-learn.org/stable/
from PIL import ImageDraw, ImageFont #This library was written by Pillow, this is their website: https://pillow.readthedocs.io/en/stable/
import numpy as np #This library was written by NumPy, this is their website: https://numpy.org/
import math #This library is built into Python
import matplotlib.pyplot as plt #This library was written by Matplotlib, this is their website: https://matplotlib.org/
import matplotlib.pylab as pl #This library was also written by Matplotlib
import PIL #This library was also written by Pillow
import time #This library is built into Python

class ModifiedKMedoids:
    """A standard K-Medoid Algorithm, except it runs K-Medoids for multiple iterations,
    removing outliers between each iteration. The function returns a trained
    k_medoids object, that can then be used for predictions."""

    @staticmethod
    def k_medoids(array, num_clusters, iterations, percentile, num_times):
        """Returns trained kmedoids model"""

        removed = []
        history = []
        removed = np.empty((0,0), float)
        dimensions = len(array[0])

        #Runs KMedoids Algorithm
        for i in range(0, iterations + 1):

            #Train on data w/o outliers
            if (np.size(array, axis=0) != 0 and num_clusters < np.size(array, axis=0)):
                medoids = KMedoids(n_clusters = num_clusters, max_iter = 300).fit(array)
                centroids = medoids.cluster_centers_
            elif np.size(array, axis=0) == 0:
                error_message = ("All datapoints have been identified as outliers in iteration {iteration}. " +
                                 "There were {num_outliers} outliers and {num_datapoints} ordinary datapoints. " +
                                 "The percentile is likely set too low.")
                print(error_message.format(iteration = i, num_outliers = np.size(removed, axis=0), num_datapoints = np.size(array, axis=0)))
                break
            else:
                error_message = ("The number of datapoints ({num_datapoints}) is less than the number of clusters " +
                                 "({clusters}) in iteration {iteration}")
                print(error_message.format(num_datapoints = np.size(array, axis=0), clusters = num_clusters, iteration = i))
                break

            #Add back the removed outliers
            if i != 0:
                if np.size(removed, axis=0) != 0:
                    history.append([array, centroids, removed, medoids])
                    array = np.append(array, removed, axis = 0)
                else:
                    error_message = ("No outliers have been detected in iteration {iteration}. " +
                                     "There were {num_outliers} outliers and {num_datapoints} ordinary datapoints. " +
                                     "The percentile is likely set too high.")
                    print(error_message.format(iteration = i, num_outliers = np.size(removed, axis=0), num_datapoints = np.size(array, axis=0)))
                    break
            predictions = medoids.predict(array)

            #Find N-Dimensional distance from each datapoint to centroid
            distances = []
            for l in range(0, len(array)): #For each datapoint
                respective_centroid = centroids[predictions[l]] #Find the corresponding centroid
                distance = 0
                for j in range(0, dimensions): #Calculate the distance to the centroid
                    distance = distance + ((array[l][j] - respective_centroid[j]) ** 2)
                distances.append(math.sqrt(distance))

            #Removes the biggest distances from the list
            sort_ind = np.argsort(distances)
            chunk = int((1.0 - percentile) * len(sort_ind)) + 1
            remove = sort_ind[-chunk:]
            remove = np.sort(remove)
            remove = np.flip(remove)
            removed = []
            for e in range(0, len(remove)):
                removed.append(array[remove[e]])
                array = np.delete(array, remove[e], axis=0)
            removed = np.array(removed)

        #Perform visualizations
        if dimensions in (2, 3): #If it's 2 or 3 dimensional
            images = []
            custom_font = ImageFont.truetype("arial.ttf", 24)
            for i in range(iterations):
                if dimensions == 2 and np.size(history, axis=0) > 0:
                    fig = ModifiedKMedoids.two_dim_vis(history[i][0], history[i][1], history[i][2], history[i][3], num_clusters)
                elif dimensions == 3 and np.size(history, axis=0) > 0:
                    fig = ModifiedKMedoids.three_dim_vis(history[i][0], history[i][1], history[i][2], history[i][3], num_clusters)
                else:
                    print("The program failed on it\'s first iteration, so there is no data to display.")
                    break
                fig.canvas.draw() #Depending on the backend, the canvas is not automatically drawn, and hence needs to first be manually drawn
                image = PIL.Image.frombytes("RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
                manipulable_image = ImageDraw.Draw(image)
                manipulable_image.text((10, 10), "Iteration Number: " + str(i + 1), font = custom_font, fill=(0, 0, 0))
                images.append(image)
            if len(images) > 0:
                first_img = images[0]
                file_name = "clustering_" + str(num_times) + ".gif"
                first_img.save(fp=file_name, format="GIF", append_images=images, save_all=True, duration=300, loop=0)
            else:
                print("No images were able to be created, try running the program again with new inputs.")
        
        #Try returning trained KMedoids
        try:
            return medoids
        except UnboundLocalError:
            print("The medoids variable was never declared")
            return None

    @staticmethod
    def two_dim_vis(array, centroids, removed, medoids, num_clusters):
        """The name is short for "Two Dimensional Visualization"; visualizes 2D clusters using MatPlotLib"""
        
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

        ax.scatter(x_outliers, y_outliers, marker="*", c = "red", label="Outliers")
        ax.scatter(x_data, y_data, c = colors, cmap="brg", marker = ".", label="Datapoints") #converts labels into colors
        ax.scatter(x_centroids, y_centroids, marker="o", c = "black", label="Centroids")

        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=3)
        plt.show()
        return fig

    @staticmethod
    def three_dim_vis(array, centroids, removed, medoids, num_clusters):
        """The name is short for "Three Dimensional Visualization"; visualizes 3D clusters using MatPlotLib"""
        
        fig = plt.figure(figsize=(7, 7))
        ax = plt.axes(projection="3d")
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

        ax.scatter(x_outliers, y_outliers, z_outliers, marker="*", c = "red", label="Outliers")
        ax.scatter(x_data, y_data, z_data, c = colors, cmap="brg", marker = ".", label="Datapoints") #converts labels into colors
        ax.scatter(x_centroids, y_centroids, z_centroids, marker="o", c = "black", label="Centroids")

        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=3)
        plt.show()
        return fig
    
    @staticmethod
    def demo(n_dimensions):
        """Demos the KMedoids Algorithm in 3D to showcase proper input parameters"""
        
        #Sets variables and explains them
        print("-The datapoints will be " + str(n_dimensions) + "-dimensional")
        time.sleep(0.2)
        print("-There will be 500 datapoints")
        n_datapoints = 500
        time.sleep(0.2)
        print("-4 Clusters will be created")
        n_clusters = 4
        time.sleep(0.2)
        print("-The algorithm will run for 5 iterations")
        n_iterations = 5
        time.sleep(0.2)
        print("-The 90th percentile will be outliers\n")
        n_percentile = 0.9
        time.sleep(0.2)
        
        #Runs KMedoids Model
        array_1 = np.random.rand(n_datapoints, n_dimensions)
        ModifiedKMedoids.k_medoids(array_1, n_clusters, n_iterations, n_percentile, "example")

#Stops deprecation warnings from appearing in console
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)                 

#Runs KMedoids Demo
print("The following will demonstrate 3 and 4 Dimensional clustering using the KMedoids Algorithm\n")
time.sleep(1)

ModifiedKMedoids.demo(3)
ModifiedKMedoids.demo(4)

#Runs the KMedoids program according to user-set parameters
run_again = True
counter = 0
while True:
    #Gives User the option to quit the program
    while True:
        run_again_input = input("Would you like to run the KMedoids algorithm? (y/n)")
        if run_again_input == "yes" or run_again_input == "Yes" or run_again_input == "y" or run_again_input == "Y":
            run_again = True
            break
        elif run_again_input == "no" or run_again_input == "No" or run_again_input == "n" or run_again_input == "N":
            run_again = False
            break
        else:
            print("That was an invalid entry, please try again")

    #Leaves the loop if user chooses to
    if not run_again:
        break
    
    #Asks for inputs until they're valid
    while True:
        try:
            n_dimensions = int(input("How many dimensions would you like? (Visualization works only with 2 or 3 dimensions) "))
            n_datapoints = int(input("How many datapoints would you like to cluster? ")) #2000
            n_clusters = int(input("How many clusters would you like to create? ")) #8
            n_iterations = int(input("How many iterations would you like to run the outlier algorithm for? ")) #30
            n_percentile = float(input("What percentile (Out of 100) should the outliers be in? "))/100.0 #90
            break
        except ValueError:
            print("The value inputted was invalid, all inputs must be integers.")
    
    #Runs KMedoids Model
    array_1 = np.random.rand(n_datapoints, n_dimensions)
    trained_model = ModifiedKMedoids.k_medoids(array_1, n_clusters, n_iterations, n_percentile, counter)
    
    #Keep tracks of how many times the algorithm has been run
    counter += 1
