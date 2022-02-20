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
    #called each forward propagation (calculating loss, training, etc.)
    def call(self, inputs):
        print("INPUTS: " + str(inputs))
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
    
    #pass the augmented data and the full unaugmented labels for indexing
    def data_import(self, augmented_data, y_true_all):
        self.augmented_data = augmented_data
        self.y_true_all = np.asarray(y_true_all, dtype=np.int8) #in theory you could get this from the fit function but thats hard and im lazy + that might mess up some other stuff idfk
        
    def comparative_loss(self, y_true, y_pred, y_aug):
        print("Y_TRUE" + str(y_true))
        print("Y_PRED " + str(y_pred))
        print("Y_AUG" + str(y_aug))
        loss = keras.backend.square(y_pred - y_true)  # (batch_size, 2)
    
                    
        # summing both loss values along batch dimension 
        loss = keras.backend.sum(loss, axis=1)        # (batch_size,)
        return loss
        
    def train_step(self, data):
        # Unpack the data. Its structure depends on your model and
        # on what you pass to `fit()`.
        x, y = data
        y_true = y #tensorflow uses y as y_true, but thats confusing
        
        print("Y TRUE ALL" + str(self.y_true_all))
        print("Y TRUE INSTANCE" + str(y_true))
        print("YEEEYEY" + str(y_true.numpy())) #needs to have eager execution enabled for .numpy()to work, supposedly eager execution is slightly slower but there are literally no better available solutions :(
        #a lower level implementation could potentially make this part significantly more efficient by not having to perform a search each time
        aug_index = 0
        y_true_arr = y_true.numpy()
        for i in range(np.size(self.y_true_all, axis = 0) - 1): 
            if np.array_equal(self.y_true_all[i], y_true_arr): #y_true is of type tf.data.Dataset
                aug_index = i 
        print(aug_index)
        
        with tf.GradientTape() as tape:
            y_pred = self(x, training=True)  # Forward pass
            
            y_aug = self(self.augmented_data[aug_index], training=True) #Prediction for augmented data
            loss = self.comparative_loss(y_true, y_pred, y_aug) #Compute the loss value
        
        #I didnt touch any of this code
        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))
        self.compiled_metrics.update_state(y, y_pred)
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
        self.preprocessor()
        
    def preprocessor(self):
        from sklearn.preprocessing import OneHotEncoder
        onehot_encoder = OneHotEncoder(sparse=False)
        self.labels = onehot_encoder.fit_transform(np.reshape(self.labels, (-1, 1)))
        
        from sklearn.model_selection import train_test_split
        shared_seed = 5 #the indexes of complements_train and image_train have to line up, so that labels_train can apply to both
        self.complements_train, self.complements_test = train_test_split(self.complements, test_size=0.25, random_state=shared_seed)
        self.images_train, self.images_test, self.labels_train, self.labels_test = train_test_split(self.images, self.labels, test_size=0.25, random_state=shared_seed)
        
#in practice, the below will be all that needs to be given to the model
shrek_is_life = shrek_is_love()
model = CustomModel(10) #10 classes
model.data_import(shrek_is_life.complements_train, shrek_is_life.labels_train) #the model will not be training on aug_data, essentially turning it into a secondary test set
model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'], run_eagerly=True) #you can give it anything for loss; it'll ignore it and use the custom one
print(shrek_is_life.images_train.shape)
model.fit(x = shrek_is_life.images_train, y = shrek_is_life.labels_train, epochs = 1)
