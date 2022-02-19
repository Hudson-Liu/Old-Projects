# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 11:37:08 2022

Custom Loss Function 

Description:

For each element of y_true, compare the y_predict of
the original image and the complemented one, then return
a loss accordingly using the Euclidian distance 
between the predictions for the original images and the complements.

y_predict are labels for the images, these labels can 
come in any form: CIFAR labels, species labels, or labels of which
individual a given image is. 

y_predict will be in the shape (batch_size, number_of_classes), using the 

@author: hudso
"""
import tensorflow as tf
import keras
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, BatchNormalization
import ssl
import numpy as np
import cv2 as cv

class CustomModel(keras.Model):
    def __init__(self, classes):
        super().__init__() #call parent constructor
        self.conv_1 = Conv2D(32,(3,3),activation='relu',padding='same')
        self.batch_1 = BatchNormalization()
        self.conv_2 = Conv2D(32,(3,3),activation='relu',padding='same')
        self.batch_2 = BatchNormalization()
        self.pool_1 = MaxPooling2D((2,2))
        self.conv_3 = Conv2D(64,(3,3),activation='relu',padding='same')
        self.batch_3 = BatchNormalization()
        self.conv_4 = Conv2D(64,(3,3),activation='relu',padding='same')
        
        self.batch_4 = BatchNormalization()
        self.pool_2 = MaxPooling2D((2,2))
        self.conv_5 = Conv2D(128,(3,3),activation='relu',padding='same')
        self.batch_5 = BatchNormalization()
        self.conv_6 = Conv2D(128,(3,3),activation='relu',padding='same')
        
        self.batch_6 = BatchNormalization()
        self.flatten = Flatten()
        self.layer_1 = keras.layers.Dropout(0.2)
        self.layer_2 = Dense(256,activation='relu')
        self.dropout = keras.layers.Dropout(0.2)
        self.outputs = Dense(classes, activation='softmax') #no. of classes
    
    #essentially the Functional API forward-pass call-structure shenanigans
    def call(self, inputs):
        x = self.conv_1(inputs)
        x = self.batch_1(x)
        x = self.conv_2(x)
        x = self.batch_2(x)
        x = self.pool_1(x)
        x = self.conv_3(x)
        x = self.batch_3(x)
        x = self.conv_4(x)
        
        x = self.batch_4(x)
        x = self.pool_2(x)
        x = self.conv_5(x)
        x = self.batch_5(x)
        x = self.conv_6(x)
        
        x = self.batch_6(x)
        x = self.flatten(x)
        x = self.layer_1(x)
        x = self.layer_2(x)
        x = self.dropout(x)
        x = self.outputs(x)
        
        return x #returns the constructed model
    
    def aug_data_import(self, augmented_data):
        self.augmented_data = augmented_data
        
    def comparative_loss(self, y_true, y_pred, y_aug):
        print("Y_TRUE" + str(y_true))
        print("Y_PRED " + str(y_pred))
        loss = keras.backend.square(y_pred - y_true)  # (batch_size, 2)
    
                    
        # summing both loss values along batch dimension 
        loss = keras.backend.sum(loss, axis=1)        # (batch_size,)
        return loss
        
    def train_step(self, data):
        # Unpack the data. Its structure depends on your model and
        # on what you pass to `fit()`.
        x, y = data
        with tf.GradientTape() as tape:
            y_true = y #tensorflow uses y as y_true, but thats confusing
            y_pred = self(x, training=True)  # Forward pass
            y_aug = self(self.augmented_data, training=True) #Prediction for augmented data
            loss = self.comparative_loss(y_true, y_pred, y_aug) # Compute the loss value
        
        #I didnt touch any of this code
        # Compute gradients
        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)
        # Update weights
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))
        # Update metrics (includes the metric that tracks the loss)
        self.compiled_metrics.update_state(y, y_pred)
        # Return a dict mapping metric names to current value
        return {m.name: m.result() for m in self.metrics}
   
#handles all the other stuff that makes it possible to run the model
#AKA: Creates the dataset
class shrek_is_love: 
    def __init__(self): #these will be actual variables in the actual program
        self.complements = []
        self.create_dataset()
    
    #automatically runs
    def create_dataset(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        (images, labels), (_, _) = keras.datasets.cifar10.load_data()
        self.labels = labels
        self.images = images
        self.data_aug()
        
    #NOT MY CODE this is liam's image data generator (thx liam ur cool)
    #automatically runs
    #only does augmentation on "images"/training set, will have to modify this to use a concatenated array of "images" and "testing_img" to be able to train the model with a validation set
    #also have to adjust indexing of finding the corresponding augmented image for the test set
    #wait actually this shouldn't be an issue since we'll do the train/test split together on the final version
    #ok actually the best way to fix it is assume "images" is the full dataset, ignore the testing images, then do a train/test split on only the training set
    #it's just the easiest way, plus we wont run into the same issue on the happywhales thing
    def data_aug(self): 
        imageGen = keras.preprocessing.image.ImageDataGenerator(width_shift_range=.3, height_shift_range=.3, horizontal_flip=True, zoom_range=.3)
        imagees = np.zeros(shape=(1, 32, 32, 3))
        for l in range(np.size(self.images, 0)): 
            # adjust the tuple inside of cv.resize to adjust resolution
            temp = cv.resize(self.images[l], (32, 32))
            imagees[0] = (cv.cvtColor(temp, cv.COLOR_BGR2RGB))
        
            it = imageGen.flow(imagees)
            im = it.next()
            im = im[0].astype('float32')
        
            im = im / 255.0
            self.complements.append(im)
        
        self.images = self.images.astype(np.float)
        self.preprocessor()
        
    def preprocessor(self):
        from sklearn.preprocessing import OneHotEncoder
        onehot_encoder = OneHotEncoder(sparse=False)
        self.labels = onehot_encoder.fit_transform(np.reshape(self.labels, (-1, 1)))
        
        from sklearn.model_selection import train_test_split
        self.images_train, self.images_test, self.labels_train, self.labels_test = train_test_split(self.images, self.labels, test_size=0.25, random_state=42)
        
    
shrek_is_life = shrek_is_love()
model = CustomModel(10)
model.aug_data_import(shrek_is_life.labels) #what this means is that the model will not be training on aug_data, essentially turning it into a secondary test set
model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy']) #you can give it anything for loss; it'll ignore it and use the custom one
model.fit(shrek_is_life.images_train, shrek_is_life.labels_train, epochs = 1, validation_data = (shrek_is_life.images_test, shrek_is_life.labels_test)) 