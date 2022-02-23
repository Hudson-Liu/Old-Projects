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
        
        self.classes = classes #Initializes the number of classes variable
    
    #essentially the Functional API forward-pass call-structure shenanigans
    #called each forward propagation (calculating loss, training, etc.)
    def call(self, inputs):
        #print("INPUTS: " + str(inputs))
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
    
    #Imports necessary data (It's hard to gain access of the values handed to .fit())
    def data_import(self, augmented_data, x_all, batch_size):
        self.augmented_data = augmented_data
        self.x_all = np.asarray(x_all, dtype=np.float32)
        self.batch_size = batch_size
        
    #Very useful advice: https://stackoverflow.com/questions/65889381/going-from-a-tensorarray-to-a-tensor
    def comparative_loss(self, y_true, y_pred, y_aug):
        output_loss = tf.TensorArray(tf.float32, size=self.classes)
        batch_loss = tf.TensorArray(tf.float32, size=self.batch_size)
        for n in range(self.batch_size):
            for i in range(self.classes):
                output_loss = output_loss.write(i, tf.square(tf.abs(tf.subtract(y_pred[n][i], y_aug[n][i])))) #finds Euclidean Distance for each prediction, then averages the loss across all iterations in the batch
            indexes = tf.keras.backend.arange(0, self.classes, step=1, dtype='int32')
            output_loss_tensor = output_loss.gather(indexes)
            batch_loss = batch_loss.write(n, tf.math.reduce_sum(output_loss_tensor))
        indexes = tf.keras.backend.arange(0, self.batch_size, step=1, dtype='int32')
        batch_loss_tensor = batch_loss.gather(indexes)
        total_loss = tf.math.reduce_sum(batch_loss_tensor)
        total_loss = tf.math.divide(total_loss, self.batch_size)
        print("TOTAL LOSS: " + str(total_loss))
        
        return total_loss
        
    def train_step(self, data):
        x, y = data #Current batch
        
        #Finds the range of indexes for the complements of the current batch of images
        #A lower level implementation could make this significantly more efficient by avoiding searching each time
        aug_index = 0
        x_arr = x.numpy() #Turns the input data iterable Tensor into a numpy array, Eager Execution must be enabled for this to work
        for i in range(np.size(self.x_all, axis = 0)):
            difference = cv.subtract(self.x_all[i], x_arr[0])
            if np.count_nonzero(difference) == 0: #In the .fit() line for this CustomModel, shuffle = False for this to work
                aug_index = i #Lower bound of the batch of images
                found = True
        if found == False:
            print("Yikes mate the x_arr wasn't found in x_all... probably a rounding error")
        print("\nCurrent Index: " + str(aug_index))
        
        #Forward pass/predictions + loss calculation
        with tf.GradientTape() as tape:
            y_pred = self(x, training=True)
            y_aug = self(self.augmented_data[aug_index:aug_index+self.batch_size], training=True)
            
            loss = self.comparative_loss(y, y_pred, y_aug) #Computes the actual loss value
        
        #I didn't touch any of this code
        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))
        self.compiled_metrics.update_state(y, y_pred)
        return {m.name: m.result() for m in self.metrics}
   
#Essentially emulates the environment that the model would normally be running in
#E.g. Creates the dataset, does Image Augmentation, etc.
#In the actual implementation, only the "CustomModel" class will be used, this is purely for testing purposes
class shrek_is_love: 
    def __init__(self):
        self.complements = []
        self.create_dataset()
    
    #automatically runs
    def create_dataset(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        (images, labels), (_, _) = keras.datasets.cifar10.load_data() #only uses the training sets and then splits it again later since that'll be what we'll be dealing with in the happywhale dataset anyways
        self.labels = labels
        self.images = images
        self.data_aug()
        
    #NOT MY CODE this is liam's image data generator (thx liam ur cool)
    #automatically runs
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
        self.complements = np.asarray(self.complements, dtype=np.float)
        self.images = self.images.astype(np.float)
        self.images = self.images / 255.0
        self.preprocessor()
        
    def preprocessor(self):
        from sklearn.preprocessing import OneHotEncoder
        onehot_encoder = OneHotEncoder(sparse=False)
        self.labels = onehot_encoder.fit_transform(np.reshape(self.labels, (-1, 1)))
        
        from sklearn.model_selection import train_test_split
        shared_seed = 5 #the indexes of complements_train and image_train have to line up, so that labels_train can apply to both
        self.complements_train, self.complements_test = train_test_split(self.complements, test_size=0.25, random_state=shared_seed)
        self.images_train, self.images_test, self.labels_train, self.labels_test = train_test_split(self.images, self.labels, test_size=0.25, random_state=shared_seed)
        
#The following code will be all that is necessary to run the CustomModel classs
batch_size = 32
shrek_is_life = shrek_is_love()
model = CustomModel(10) #10 classes
model.data_import(shrek_is_life.complements_train, shrek_is_life.images_train, batch_size) #the model will not be training on aug_data, essentially turning it into a secondary test set
model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'], run_eagerly=True) #you can give it anything for loss; it'll ignore it and use the custom one
model.fit(x = shrek_is_life.images_train, y = shrek_is_life.labels_train, shuffle = False, batch_size = batch_size, epochs = 1)
