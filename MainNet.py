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


class MainNet: #holds MainNet, Weight iterator, and Bias iterator
    def __init__(self):
        self.logitsInterpreterInit()
        self.intentionNetInit()
        self.weightIteratorInit()
        self.hyperParameter_Optimizer_Init()
        #make a new function to import a new subnet function so that the actual training
        #loop just needs to hand off a new SubNet to the mainNetTrainingLoop function each epoch
        
    #updates every training step/epoch for the SubNet
    def setSubNet(self, SubNet):
        self.SubNet = SubNet
        
    def logitsIntepreterInit(self):
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
        inputs = keras.Input(shape = (None, num_of_biases)) 
        LSTMlayer1 = keras.layers.LSTM(1000, return_sequences=True)(inputs)
        LSTMlayer2 = keras.layers.LSTM(500, return_sequences=True)(LSTMlayer1)
        outputs = keras.layers.Dense(10, activation='softmax')(LSTMlayer2) #random encoded output
        self.intention = keras.Model(inputs=inputs, outputs=outputs, name="intention")
        self.intention.summary()
        
    def weightIteratorInit(self):
        #the shape is (one single intention per batch, number of weights in SubNet (cant be specified since when running this same model across many other SubNets, they wont be identically sized), individual weight + intention)
        #output size of intentionNet
        unprocessed_weights = self.logits_interpreter.layers[len(self.logits_interpreter.layers) - 1].get_weights() #get the weights and biases of the last layer of the subnet
        num_of_biases = len(unprocessed_weights[1]) #get the number of biases, which is equal to the amoutn of output nodes
        
        #initializaes model
        inputs = keras.Input(shape = (None, (1 + num_of_biases)))
        LSTMlayer1 = keras.layers.LSTM(1000, return_sequences=True)(inputs)
        LSTMlayer2 = keras.layers.LSTM(500, return_sequences=True)(LSTMlayer1)
        outputs = keras.layers.TimeDistributed(keras.layers.Dense(1, activation='softmax'))(LSTMlayer2)
        self.weights = keras.Model(inputs=inputs, outputs=outputs, name="weights")
        self.weights.summary()
        #finish weight iterator, make bias iterator, finish training step
    
    def hyperParameter_Optimizer_Init(self):
        inputs = keras.Input(shape=(3,)) #num_features, num_depVar, num_samples
        FFNNlayer1 = keras.layers.Dense(100, activation='relu')(inputs)
        FFNNlayer2 = keras.layers.Dense(100, activation='relu')(FFNNlayer1)
        outputs = keras.layers.Dense(4, activation='sigmoid')(FFNNlayer2)
        self.hyperparameters = keras.Model(inputs=inputs, outputs=outputs, name="hyperparameters")
        self.hyperparameters.summary()
    """
    def setWeights(self):
        for(how many layers there are):
            layer.setWeights()
    
    #a single step of training, logits are raw logits from SubNet
    def mainNetTrainingStep(SubNet_logits, correct_logits):
        
        logits_interpreter(logits, correct)
            
    
        
    def genAlg(): #generational algorithm
        """
class SubNet:
    #add required specification of output_size to metadata document
    def __init__(self, num_layers, activation, num_nodes, dataset, num_features, output_size): #int,
            self.subNet = keras.Sequential()
            self.subNet.add(keras.layers.Input(shape = (num_features,)))
            nodes_per_layer = num_nodes/num_layers
            for i in range(num_layers):
                self.subNet.add(keras.layers.Dense(nodes_per_layer))

class MainClass:
    def __init__(self, existing_preprocessed_data, import_sequentially): #both are boolean
        self.existing_preprocessed_data = existing_preprocessed_data
        self.import_sequentially = import_sequentially
        
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
        
        #open info necessary for hyperparameter optimizer
        open()UJ08usda098f
    
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
            
    def seqImportData(datafiles, number):
        cwd = os.getcwd()
        filepath = repr(datafiles[number])[1:-1]
        filepath = cwd + "\\PreProcessed_Data\\" + filepath
        dataset = np.load(filepath)
        
        return dataset
    
    #training loop for single solution
    def training_loop():
        mainNet = MainNet()
        
        mainNet.hyperparameters()
        
            
#jimmy = MainNet(50) #the only parameter is how many epochs each SubNet is ran
