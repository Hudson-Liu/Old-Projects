#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 13:17:24 2021

SPDX-FileCopyrightText: © 2021 Hudson Liu <hudsonliu0@gmail.com>
All rights reserved
Unauthorized copying, distributing, and modifying of this file, via any medium is strictly prohibited
Proprietary and confidential
    
@author: Hudson-Liu
"""

import numpy as np
from tensorflow import keras
import pygad

class MainNet:
    def __init__(epochsPerSubNet):
        self.timesteps = epochsPerSubNet #the LSTM will take exactly as many timesteps as epochs of the SubNet
        modelInit()
    def modelInit():
        inputs = keras.Input(shape = (timesteps, 5))
        LSTMlayer1 = keras.layers.LSTM(1024, return_sequences=True)(inputs)
        LSTMlayer2 = keras.layers.LSTM(1024, return_sequences=True)(LSTMlayer1)
        LSTMlayer3 = keras.layers.LSTM(1024, return_sequences=True)(LSTMlayer2)
        outputs = keras.layers.LSTM(1024, return_sequences=True)(LSTMlayer3)
        jimmy = keras.Model(inputs=inputs, outputs=outputs, name="Jimmy")
        jimmy.summary()
    def genAlg(): #generational algorithm
        
class SubNet:
    
class Fitness:
    def __init__():
        
    def fitness_func():
    def calculateFitness():
        
jimmy = MainNet(50) #the only parameter is how many epochs each SubNet is ran
