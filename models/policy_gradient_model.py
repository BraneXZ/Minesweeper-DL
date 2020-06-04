# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:11:46 2020

@author: Wash
"""

from keras.layers.core import Dense, Flatten
from keras.layers.convolutional import Conv2D
from keras import Sequential 

def get_model(encoder):
    input_shape = encoder.shape()
    
    model = Sequential()
    
    model.add(Conv2D(3, (3, 3), padding="same", input_shape=input_shape, activation="relu"))
    model.add(Flatten())
    model.add(Dense(input_shape[-1] * input_shape[-2], activation="softmax"))
    
    return model
        
    