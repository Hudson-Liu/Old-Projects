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
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

epochsPerSubNet = 50 #The number of epochs each SubNet will run
timesteps = epochsPerSubNet #the LSTM will take exactly as many timesteps as epochs of the SubNet
inputs = keras.Input(shape = (timesteps, 5))
LSTMlayer1 = keras.layers.LSTM(1024, return_sequences=True)(inputs)
LSTMlayer2 = keras.layers.LSTM(1024, return_sequences=True)(LSTMlayer1)
LSTMlayer3 = keras.layers.LSTM(1024, return_sequences=True)(LSTMlayer2)
LSTMlayer4 = keras.layers.LSTM(1024)(LSTMlayer3)
outputs = keras.layers.Dense(5)(LSTMlayer4)
jimmy = keras.Model(inputs=inputs, outputs=outputs, name="Jimmy")
jimmy.summary()