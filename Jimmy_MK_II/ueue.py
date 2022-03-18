# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 11:37:01 2022

@author: hudso
"""
import numpy as np
from tensorflow import keras
import Data_PreProcessor
import os
import glob

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
            print(Data_PreProcessor.PreProcessor(cwd, file, counter))
            counter += 1
    
    def importAllData(self, datafiles):
        datasets = []
        cwd = os.getcwd()
        for dataset in datafiles:
            filepath = repr(dataset)[1:-1]
            filepath = cwd + "\\PreProcessed_Data\\" + filepath
            datasets.append(np.load(filepath)) 
        return datasets
    
halloa = MainClass(False, False)
aaaaaaaa = halloa.datasets[0]['featuresTrain']
print(halloa.datasets[0]['featuresTest'])
print(halloa.datasets[0]['dependantTrain'])
print(halloa.datasets[0]['dependantTest'])