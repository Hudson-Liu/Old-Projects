# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 08:49:17 2022

@author: hudso
"""

import numpy as np #for arrays
import cv2 as cv
from tensorflow import keras
import glob
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.cluster import MiniBatchKMeans
from tensorflow.keras import datasets, layers, models
import tensorflow as tf
#imports images
image_input = [cv.imread(file, 1) for file in glob.glob("ea/*.png")]
#resizes images and removes photos that failed to load
hudsonisanidiot = 0
buffer = 0 #needs to accomodate for updated indexes after removing elements
width = 256
height = 256
for i in range(0, np.size(image_input, 0)):
    iso_var = image_input[i - buffer]
    try:
        image_input[i - buffer] = cv.resize(iso_var, (width, height), interpolation = cv.INTER_AREA)
        image_input[i - buffer] = cv.cvtColor(image_input[i - buffer], cv.COLOR_BGR2GRAY)
        _, image_input[i - buffer] = cv.threshold(image_input[i - buffer], 127, 255, cv.THRESH_BINARY) #from grayscale to black/white
        imgplot = plt.imshow(image_input[i], cmap = 'gray')
        plt.show()
    except:
        hudsonisanidiot += 1
        print(str(hudsonisanidiot) + " images failed to load get good lol")
        buffer += 1
        del image_input[i]
image_input = np.asarray(image_input)

#saves data
#np.save("preprocessed_data", image_input)

#image contouring for image-foreground extraction
contours = []
for i in range(0, np.size(image_input, 0)):
    contour, hierarchy = cv.findContours(image_input[i], cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours.append(contour)

#visualizing the contours
if (np.size(contours, 0) > 25):
    graphs = 25
else:
    graphs = np.size(contours, 0)
    
for i in range(graphs):
    blank_img = np.zeros((width, height), dtype=np.uint8)
    image_input[i] = cv.drawContours(blank_img, contours[i], -1, color=(255,255,255), thickness=2, lineType=cv.LINE_AA)
    imgplot = plt.imshow(image_input[i], cmap = 'gray')
    plt.show()

"""
#train/test split
x_train, x_test = train_test_split(image_input, test_size = 0.25)
x_train = x_train.astype('float32') 
x_test = x_test.astype('float32')
x_train = x_train/255.0
x_test = x_test/255.0

kmeans = MiniBatchKMeans(n_clusters = 10) #10 is arbitrarily chosen
kmeans.fit(x_train)

print(kmeans.labels_)"""
