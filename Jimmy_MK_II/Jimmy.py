#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 11:37:01 2022

SPDX-FileCopyrightText: © 2022 Hudson Liu <hudsonliu0@gmail.com>
All rights reserved
Unauthorized copying, distributing, and modifying of this file, via any medium is strictly prohibited
Proprietary and confidential

SELLER MAKES NO WARRANTIES WHETHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY IMPLIED WARRANTY 
OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. THE PURCHASE OF THIS (ITEM) IS SUBJECT TO THE TERMS AND 
CONDITIONS OF AN “AS IS” SALE.

@author: Hudson-Liu
"""

import numpy as np
from tensorflow import keras
import Data_PreProcessor
import os
import glob
from sklearn.preprocessing import StandardScaler
from math import ceil, floor

class MainNet: #holds MainNet, Weight iterator, and Bias iterator
    def __init__(self):
        self.logitsInterpreterInit()
        self.intentionNetInit()
        self.weightIteratorInit()
        self.biasIteratorInit()
        self.hyperParameter_Optimizer_Init()
        #make a new function to import a new subnet function so that the actual training
        #loop just needs to hand off a new SubNet to the mainNetTrainingLoop function each epoch
        
    def logitsInterpreterInit(self):
        #creates stacked lstm, all these values i pulled out of my arse
        inputs = keras.Input(shape = (None, 2)) #the shape is (one single logit per batch, total amount of logits from subnet (variable so we dont give it an input), individual logit + correct logit)
        LSTMlayer1 = keras.layers.LSTM(1000, return_sequences=True)(inputs)
        LSTMlayer2 = keras.layers.LSTM(500, return_sequences=False)(LSTMlayer1)
        outputs = keras.layers.Dense(100, activation='softmax')(LSTMlayer2) #random encoded output
        self.logits_interpreter = keras.Model(inputs=inputs, outputs=outputs, name="interpreter")
        self.logits_interpreter.summary()
    
    #intention net is literally just the intention of the network dont ask
    def intentionNetInit(self):
        #find output size of logits_interpreter
        unprocessed_weights = self.logits_interpreter.layers[len(self.logits_interpreter.layers) - 1].get_weights() #get the weights and biases of the last layer of the subnet
        num_of_biases = len(unprocessed_weights[1]) #get the number of biases, which is equal to the amoutn of output nodes
        
        #the shape is (one single interpreter output per batch, number of epochs the subnet has to run, size of output of interpreter)
        inputs = keras.Input(shape = (None, num_of_biases)) #num of biases stays constant, im just doing this for the sake of encapsulation
        LSTMlayer1 = keras.layers.LSTM(1000, return_sequences=True)(inputs)
        LSTMlayer2 = keras.layers.LSTM(500, return_sequences=True)(LSTMlayer1)
        outputs = keras.layers.Dense(10, activation='softmax')(LSTMlayer2) #random encoded output
        self.intention = keras.Model(inputs=inputs, outputs=outputs, name="intention")
        self.intention.summary()
        
    def weightIteratorInit(self):
        #the shape is (one single intention per batch, number of weights in SubNet (cant be specified since when running this same model across many other SubNets, they wont be identically sized), individual weight + intention)
        #output size of intentionNet
        unprocessed_weights = self.intention.layers[len(self.intention.layers) - 1].get_weights() #get the weights and biases of the last layer of the subnet
        num_of_biases = len(unprocessed_weights[1]) #get the number of biases, which is equal to the amoutn of output nodes
        weightIntent = int(ceil(num_of_biases))
        
        #initializaes model
        inputs = keras.Input(shape = (None, (1 + weightIntent))) #the "1" is the actual weight, and the num of biases/2 is since half of the outputs of the intentionNet are for the weights, and the other half is for the biases
        LSTMlayer1 = keras.layers.LSTM(1000, return_sequences=True)(inputs)
        LSTMlayer2 = keras.layers.LSTM(500, return_sequences=True)(LSTMlayer1)
        outputs = keras.layers.TimeDistributed(keras.layers.Dense(1, activation='softmax'))(LSTMlayer2)
        self.weights = keras.Model(inputs=inputs, outputs=outputs, name="weights")
        self.weights.summary()
    
    def biasIteratorInit(self):
        unprocessed_weights = self.intention.layers[len(self.intention.layers) - 1].get_weights() #get the weights and biases of the last layer of the subnet
        num_of_biases = len(unprocessed_weights[1]) #get the number of biases, which is equal to the amoutn of output nodes
        biasIntent = int(floor(num_of_biases)) #this is the portion of the IntentionNet output intended for the bias iterator
        
        #initializaes model
        inputs = keras.Input(shape = (None, (1 + biasIntent))) #the "1" is the actual weight, and the num of biases/2 is since half of the outputs of the intentionNet are for the weights, and the other half is for the biases
        LSTMlayer1 = keras.layers.LSTM(1000, return_sequences=True)(inputs)
        LSTMlayer2 = keras.layers.LSTM(500, return_sequences=True)(LSTMlayer1)
        outputs = keras.layers.TimeDistributed(keras.layers.Dense(1, activation='softmax'))(LSTMlayer2)
        self.biases = keras.Model(inputs=inputs, outputs=outputs, name="biases")
        self.biases.summary()
        
    def hyperParameter_Optimizer_Init(self):
        inputs = keras.Input(shape=(3,), batch_size=1) #num_features, num_depVar, num_samples
        FFNNlayer1 = keras.layers.Dense(100, activation='relu')(inputs)
        FFNNlayer2 = keras.layers.Dense(100, activation='relu')(FFNNlayer1)
        numericalOutput = keras.layers.Dense(3, activation='sigmoid')(FFNNlayer2) #num of hidden layers, nodes per hidden layer, one hot encoded activation functions, and epochs
        categoricalOutput = keras.layers.Dense(9, activation='softmax')(FFNNlayer2) #Taking advantage of the Functional API, we can give the output layer multiple activations. In this case, since one output (the activaiton function of the subnet) is onehotencoded, while the other outputs are all numerical, the numerical ones caxn be covered under a sigmoid activation, and the categorical onehotencoded activaiton function data can be represented with softmax activation functions
        outputs = keras.layers.concatenate([numericalOutput, categoricalOutput])
        self.hyperparameters = keras.Model(inputs=inputs, outputs=outputs, name="hyperparameters")
        self.hyperparameters.summary()

class SubNet:
    #add required specification of output_size to metadata document
    def __init__(self, num_layers, activation, num_nodes, input_size, output_size): #int, str, int, int, int
            self.subNet = keras.Sequential()
            self.subNet.add(keras.layers.Input(shape = (input_size,)))
            nodes_per_layer = num_nodes/num_layers
            for i in range(num_layers):
                self.subNet.add(keras.layers.Dense(nodes_per_layer, activation=activation))
            self.subNet.add(keras.layers.Dense(output_size, activation='sigmoid'))

class MainClass:
    def __init__(self, existing_preprocessed_data, import_sequentially, epochs_per_mainNet, single_shot, samplewiseImportInfo): #both are boolean
        self.existing_preprocessed_data = existing_preprocessed_data
        self.import_sequentially = import_sequentially
        self.epochs_per_mainNet = epochs_per_mainNet
        #self.single_shot = single_shot
        #self.samplewiseImportInfo = samplewiseImportInfo
        
        #preprocess data if necessary
        if not self.existing_preprocessed_data:
            path = r"\Metadata"
            extension = "txt"
            files = self.findFilepaths(path, extension)
            self.preProcessData(files)
        
        #import data
        path = r"\Preprocessed_Data"
        extension = 'npz'
        datafiles = self.findFilepaths(path, extension)
        
        if not self.import_sequentially:
            self.datasets = self.importAllData(datafiles)
        
        #self.training_loop(single_shot, samplewiseImportInfo)
    
    #create a list of the files that are going to either be opened or preprocessed
    def findFilepaths(self, path, extension):
        cwd = os.getcwd() #cwd = current working directory
        os.chdir(cwd + path)
        files = glob.glob('*.{}'.format(extension))
        
        text = "\n".join(files)
        path = r"\Dataset_Processing_Order"
        os.chdir(cwd + path)
        with open('order_of_datasets.txt', 'w') as f:
            f.write(text)
        
        os.chdir(cwd)
        
        return files
    
    def preProcessData(self, files):
        counter = 0
        cwd = os.getcwd()
        for file in files:
            file = cwd + "\\Metadata\\" + file
            Data_PreProcessor.PreProcessor(cwd, file, counter)
            counter += 1
    
    def importAllData(self, datafiles):
        datasets = []
        cwd = os.getcwd()
        for dataset in datafiles:
            filepath = repr(dataset)[1:-1]
            filepath = cwd + "\\PreProcessed_Data\\" + filepath
            datasets.append(np.load(filepath)) 
        return datasets
            
    def seqImportData(self, datafiles, number):
        cwd = os.getcwd()
        filepath = repr(datafiles[number])[1:-1]
        filepath = cwd + "\\PreProcessed_Data\\" + filepath
        dataset = np.load(filepath)
        
        return dataset
    
    #figuring out the output of the hyperparameter optimizer by decoding it into useful information that can then be used for the creation of the subnet
    def decodeHyperparameterOutput(encoded):
        #find activation
        activations_dict = ["relu", "sigmoid", "softmax", "softplus", "softsign", "tanh", "selu", "elu", "exponential"]
        activations_index = np.argsort(encoded[0][3:])
        best_activation = activations_index[0]
        activation = activations_dict[best_activation]
        
        #find numerical stuff (total amount of nodes, number of hidden layers, number of epochs)
        num_total_nodes = 1000 * encoded[0][0] #1000 nodes at most
        num_hidden_layers = 4 * encoded[0][1] #4 hidden layers at most
        num_epochs = 500 * encoded[0][2] #500 epochs at most
        return activation, num_total_nodes, num_hidden_layers, num_epochs
    
    #only used for multi-shot network, aka. Jimmy MK II w/ multiple dataset
    def samplewiseImportInfo(self): #info refers to "dataset_info.txt"
        #Imports all the Dataset_Info.txt stuff and scales it samplewise one go
        file = open("Dataset_Info.txt", "r", encoding='utf-8-sig')
        lines = file.readlines()
        dataset_info = np.array([[0, 0, 0, 0]])
        for i in range(0, len(lines)):
            modified_line = (lines[i].replace("\n", "")).split(" ")
            #handles this quirk of the data preprocessor when it saves stuff
            if len(modified_line) == 4:
                dataset_info = np.append(dataset_info, [modified_line], axis=0)
            else: 
                print("There was an incorrect line found in the \"Dataset_Info.txt\" file. This is likely because the first line is just \"\\n\"")
        dataset_info = dataset_info[1:]
        
        #scaling
        dataset_info = dataset_info.astype(float)
        scaler = StandardScaler()
        dataset_info = scaler.fit_transform(dataset_info)#samplewise normalization, linked here: https://stats.stackexchange.com/questions/354774/should-i-normalize-featurewise-or-samplewise
        return dataset_info
        
    #kind of useless (since single-shot avoids the hyperparameter optimizer completely and multi-shot uses samplewiseImportInfo) but i'll keep it in since it might work better than samplewise
    def featurewiseImportInfo(self, epoch_number):
        file = open("Dataset_Info.txt", "r", encoding='utf-8-sig')
        lines = file.readlines()
        dataset_info = (lines[epoch_number].replace("\n", "")).split(" ")
        scaler = StandardScaler()
        dataset_info = np.reshape(dataset_info, (len(dataset_info), 1)) #convert to format for standard scalar
        dataset_info = scaler.fit_transform(dataset_info)#featurewise normalization, linked below
        dataset_info = np.reshape(dataset_info, (1, len(dataset_info))) #https://stats.stackexchange.com/questions/354774/should-i-normalize-featurewise-or-samplewise
        dataset_info = dataset_info.astype(float)
        #tensorflow_dataset_info =  tf.data.Dataset.from_tensor_slices(dataset_info)
        return dataset_info
    
    #training loop for single solution
    def training_loop(self, single_shot, samplewiseImportInfo):
        #scale all dataset info in one go only if single_shot is false
        if not single_shot and samplewiseImportInfo:
            bulk_dataset_info = self.samplewiseImportInfo()
            
        for i in range(self.epochs_per_mainNet):
            #initializing the subnet via the hyperparameter optimizer
            mainNet = MainNet()
            if not single_shot:
                #choose which kind of scaling to do on the dataset_info
                if samplewiseImportInfo:
                    dataset_info = bulk_dataset_info[i]
                else:
                    dataset_info = self.featurewiseImportInfo(i)
                
                hyperparameters = mainNet.hyperparameters.predict(np.array([dataset_info])) #forward propagation of hyperparameter optimizer
                num_hidden_layers, activation, num_total_nodes, num_epochs = self.decodeHyperparameterOutput(hyperparameters)
                
                #scale hyperparametsr so that they actualy arents just between 0 and 1 but represent meaningfu values
                #add dependent variable size to dataset_info export modify respective methods
                subNetInstance = SubNet(num_hidden_layers, activation, num_total_nodes)
            
        
#jimmy = MainNet(50) #the only parameter is how many epochs each SubNet is rana
# but did you consider adding a monkE everywhere? 
print('MonkEEEEEEEEEEEEEEEEEEE')
#the following code is purely for testing purposes
mainNet = MainNet()
mainClass = MainClass(False, False, 1, False, True)
bulk_dataset_info = mainClass.samplewiseImportInfo()
dataset_info = bulk_dataset_info[0]
#hyperparameters = mainNet.hyperparameters.predict(np.array([dataset_info]))
