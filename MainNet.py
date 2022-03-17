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
    def __init__(epochsPerMainNet, epochsPerSubNet, SubNet):
        self.epochsPerMainNet = epochsPerMainNet
        self.epochsPerSubNet = epochsPerSubNet #the LSTM will take exactly as many timesteps as epochs of the SubNet
        self.SubNet = SubNet
        mainNetInit()
        weightIteratorInit()
        #make a new function to import a new subnet function so that the actual training
        #loop just needs to hand off a new SubNet to the mainNetTrainingLoop function each epoch
        
    #updates every training step/epoch for the SubNet
    def setSubNet(SubNet):
        self.SubNet = SubNet
        
    def mainNetInit(self):
        #finds the output shape of the subnet
        unprocessed_weights = self.SubNet.layers[len(self.SubNet.layers) - 1].get_weights() #get the weights and biases of the last layer of the subnet
        num_of_biases = len(unprocessed_weights[1]) #get the number of biases
        
        inputs = keras.Input(batch_input_shape = (1, num_of_biases, 2)) #the shape is (one single logit per batch, total amount of logits from subnet, individual logit + correct logit)
        LSTMlayer1 = keras.layers.LSTM(1000, return_sequences=True)(inputs)
        LSTMlayer2 = keras.layers.LSTM(1000, return_sequences=True)(LSTMlayer1)
        LSTMlayer3 = keras.layers.LSTM(1000, return_sequences=True)(LSTMlayer2)
        outputs = keras.layers.LSTM(1, return_sequences=True)(LSTMlayer3) #modified logit
        jimmy = keras.Model(inputs=inputs, outputs=outputs, name="Jimmy")
        jimmy.summary()
        
    def weightIteratorInit(self):
        
        #find how many weights there are for the Weight Iterator
        numberOfWeights = 0
        for layer in self.SubNet.layers:
            numberOfWeights += len(layer.get_weights())
        inputs = keras.Input(shape = (numberOfWeights, 5))
        
        #initializaes model
        LSTMlayer1 = keras.layers.LSTM(1000, return_sequences=True)(inputs)
        LSTMlayer2 = keras.layers.LSTM(1000, return_sequences=True)(LSTMlayer1)
        LSTMlayer3 = keras.layers.LSTM(1000, return_sequences=True)(LSTMlayer2)
        outputs = keras.layers.LSTM(1000, return_sequences=True)(LSTMlayer3)
        weights = keras.Model(inputs=inputs, outputs=outputs, name="weights")
        weights.summary()
        
    def setWeights(self):
        for(how many layers there are):
        layer.setWeights()v
    
    #a single step of training
    def mainNetTrainingStep():
        
            
            
    def genAlg(): #generational algorithm
        
class SubNet:
    #add required specification of output_size to metadata document
    def __init__(layer_number, node_number, activation, dataset, output_size): #int, int, str, np array
            subNet = keras.Input(shape = (node_number))
            

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
            
    def seqImportData(number):
        cwd = os.getcwd()
        filepath = repr(datafiles[number])[1:-1]
        filepath = cwd + "\\PreProcessed_Data\\" + filepath
        dataset = np.load(filepath)
        
        return dataset
    
    def training_loop():
        
            
jimmy = MainNet(50) #the only parameter is how many epochs each SubNet is ran
