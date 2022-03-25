#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 4 11:45:06 2020
 
SPDX-FileCopyrightText: © 2021 Hudson Liu <hudsonliu0@gmail.com>
All rights reserved
Unauthorized copying, distributing, and modifying of this file, via any medium is strictly prohibited
Proprietary and confidential
 
@params: .csv path, index of current dataset
@author: https://www.youtube.com/watch?v=dQw4w9WgXcQ
@author: Hudson5
"""

import numpy as np #for arrays
import pandas as pd #data manipulation and processing
import sys
import os
from joblib import dump
from sklearn.impute import SimpleImputer #fill out missing data
from sklearn.compose import ColumnTransformer 
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler


def PreProcessor(cwd, filepath, index_number): #string, int
    #just a litte default checkpoint for debugging
            
    #reading metadata from .txt
    filepath = repr(filepath)[1:-1] #convert the string to raw so backslashes get preserved https://note.nkmk.me/en/python-raw-string-escape/ 
    
    rawMetadata = open(filepath,"r+", encoding='utf-8-sig') #encoding necessary for \ufeff error on linux
    metadata = rawMetadata.readlines()
    filename = metadata[0].replace("\n", "") #\n again for linux compatibility
    featureCol = (metadata[1].replace("\n", "")).split(" ")
    dependantInput = metadata[2].replace("\n", "")
    categoricalIndex = list(map(int, (metadata[3].replace("\n", "")).split(" ")))
    dependantEncodingType = metadata[4].replace("\n", "")
    
    datapath = cwd + "\\Datasets\\" + filename
    rawData = pd.read_csv(datapath, sep=",")
    
    #set features and dependant and converts to numpy array
    features = rawData[featureCol].to_numpy()
    depVar = rawData[dependantInput].to_numpy()
    
    #confirm if dep and indep are correct
    
    #fill missing for categorical/string data only runs if there's categorical columns
    if categoricalIndex != "NONE":
        numericalIndex = [i for i in range(len(featureCol)) if i not in categoricalIndex] #list of noncategorial data
        categorical = features[:, categoricalIndex]
        imputerCategorical = SimpleImputer(missing_values = np.nan, strategy = "most_frequent")
        imputerCategorical.fit(categorical[:, :])
        categorical[:, :] = imputerCategorical.transform(categorical[:, :])
    else:
        numericalIndex = [i for i in range(len(featureCol))]
        
    #fill missing for numerical data https://stackoverflow.com/questions/45704226/what-does-fit-method-in-scikit-learn-do
    numerical = features[:, numericalIndex] #version of features array with only numerical data
    imputerNumerical = SimpleImputer(missing_values = np.nan, strategy = "mean")
    imputerNumerical.fit(numerical[:, :])
    numerical[:, :] = imputerNumerical.transform(numerical[:, :])
    
    #indexs all of the columns in the categorical array then one hot encodes also labelencodes dependant vars
    categoricalLength = np.size(categorical, 1)
    encoderIndex = [*range(categoricalLength)] #finds index of all data to be encoded in featureCal
    encoder = ColumnTransformer(transformers = [('encoder', OneHotEncoder(), encoderIndex)], remainder = 'passthrough') #one hot encoding then convert back into numpy array
    categorical = np.array(encoder.fit_transform(categorical))
    encoder_filename = r"Encoders\OneHotEncoding_" + str(index_number) + ".joblib"
    dump(encoder, encoder_filename)
    if dependantEncodingType == "LabelEncode":
        encoderLabel = LabelEncoder()
        depVar = encoderLabel.fit_transform(depVar)
    elif dependantEncodingType == "OneHot":
        depVar = depVar.reshape(-1, 1)
        encoderLabel = ColumnTransformer(transformers = [('encoder', OneHotEncoder(), [0])], remainder = 'passthrough')
        depVar = encoderLabel.fit_transform(depVar)
        dep_encoder_filename = r"Encoders\DependentEncoding_" + str(index_number) + ".joblib"
        dump(encoderLabel, dep_encoder_filename)
    elif dependantEncodingType == "Numerical": #this is here that way it wont be grouped into the else statement and skip labelencoding
        None
    else:
        print("Invalid syntax in Metadata document. \nThe Encoding type is unknown. \nThe program will now abort")
        sys.exit()
    
    #connect categorical and non categorical
    features = np.concatenate((categorical, numerical), axis = 1,)
    
    #feature scaling also hudson YOUR SO DUMB REMMEBEr LEN() IS ONLY FOR LIST DUMMY
    scaler = StandardScaler()
    featuresLength = np.size(features, 1)
    categoricalLength = np.size(categorical, 1) #how many columns that have been one hot encoded
    scalerIndexRev = [*range(categoricalLength)] #indexes of one hot encoded columns
    scalerIndex = [i for i in range(featuresLength) if i not in scalerIndexRev] #indexes of normal columns
    features[:, scalerIndex] = scaler.fit_transform(features[:, scalerIndex])
    features = np.asarray(features).astype(np.float32)
    
    data_filename = r"PreProcessed_Data\PreProcessed_Data_" + str(index_number)
    np.savez(data_filename, features = features, depVar = depVar)
    
    #if the file doesn't exist already, create it
    if not os.path.exists("Dataset_Info.txt"):
        open('Dataset_Info.txt', 'w')
        
    if (depVar.ndim != 2):
        depVar = depVar.reshape(-1, 1)
        
    #save down some of the variables necessary for the hyperparameter optimizer
    with open('Dataset_Info.txt', 'r+') as f:
        f.write(str(len(featureCol)) + " " + str(np.size(features, axis=1)) + " " + str(np.size(features, axis=0)) + " " + str(np.size(depVar, axis=1)) + "\n")
