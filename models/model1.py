# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:11:46 2020

@author: Wash
"""

from keras.layers.core import Dense, Flatten
from keras.layers.convolutional import Conv2D

def layers(input_shape):
    return [
        Conv2D(3, (5, 5), padding="same", input_shape=input_shape, data_format="channels_first", activation="relu"),
        Conv2D(3, (3, 3), padding="same", data_format="channels_first", activation="relu"),
        Conv2D(3, (3, 3), padding="same", data_format="channels_first", activation="relu"),
        Conv2D(3, (3, 3), padding="same", data_format="channels_first", activation="relu"),
        Flatten(),
        Dense(input_shape[-1]*input_shape[-2], activation="softmax")
    ]