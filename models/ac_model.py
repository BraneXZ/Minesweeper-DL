# -*- coding: utf-8 -*-
"""
Created on Fri May 29 13:37:23 2020

@author: Wash
"""

from keras.models import Model
from keras.layers import Conv2D, Dense, Flatten, Input, BatchNormalization, Activation, Dropout
from keras.layers import concatenate

def get_model(encoder):
    board_input = Input(shape=encoder.shape(), name='board_input')
    
    conv1 = Conv2D(64, (3,3), padding='same', activation='relu', data_format="channel_first") (board_input)
    drop_out =  Dropout(rate=0.25) (conv1)
    
    flat = Flatten() (drop_out)
    processed_board = Dense(512) (flat)
    
    policy_hidden_layer = Dense(512, activation='relu', data_format="channel_first") (processed_board)
    policy_output = Dense(encoder.num_points(), activation='softmax') (policy_hidden_layer)
    
    value_hidden_layer = Dense(512, activation='relu', data_format="channel_first") (processed_board)
    value_output = Dense(1, activation='tanh', data_format="channel_first") (value_hidden_layer)
    
    return Model(inputs=board_input, outputs=[plicy_output, value_output])
    
    