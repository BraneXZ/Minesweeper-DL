# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:11:46 2020

@author: Wash
"""

from keras.layers.core import Dense, Flatten, Dropout
from keras.layers import MaxPooling2D, AveragePooling2D, GlobalMaxPooling2D, BatchNormalization
from keras.layers.convolutional import Conv2D
from keras import Sequential 
from keras.utils.vis_utils import plot_model
from keras.regularizers import l2

def get_model(encoder):
    input_shape = encoder.shape()
    
    model = Sequential()
    
    model.add(Conv2D(512, (3, 3), padding="same", input_shape=input_shape, activation="relu", name="Conv1a", data_format="channels_first"))
    model.add(Dropout(.5, name="Dropout1a"))
    # model.add(GlobalMaxPooling2D(data_format="channels_first"))
    # model.add(AveragePooling2D(data_format="channels_first"))
    # model.add(MaxPooling2D(data_format="channels_first", padding="same"))
    
    # model.add(Conv2D(267, (3, 3), padding="same", input_shape=input_shape, activation="relu", name="Conv2a", data_format="channels_first"))
    # model.add(Dropout(.5, name="Dropout2a"))

    # model.add(Conv2D(50, (3, 3), padding="same", activation="relu", name="Conv3a", data_format="channels_first"))
    # model.add(Dropout(.5, name="Dropout3a"))
    
    # model.add(Conv2D(512, (3, 3), padding="same", activation="relu", name="Conv4a"))
    # model.add(Dropout(.5, name="Dropout4a"))
    
    model.add(Flatten())
    model.add(Dense(input_shape[-1] * input_shape[-2], activation="softmax", name="Dense"))
    
    plot_model(model, to_file="policy_gradient_model.png", show_shapes=True)
    return model
        
    