# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:35:32 2020

@author: Wash
"""

from keras.models import Model
from keras.layers import Conv2D, Dense, Flatten, Input
from keras.layers import concatenate


def get_model(encoder):
    board_input = Input(shape=encoder.shape())
    action_input = Input(shape=(encoder.num_points(), ))
    
    # For board input
    conv1a = Conv2D(25, (3, 3), padding="same", data_format="channels_first", activation="relu") (board_input)
    
    flat = Flatten() (conv1a)
    processed_board = Dense(25) (flat)
    
    board_and_action = concatenate([action_input, processed_board])
    hidden_layer = Dense(256, activation='relu') (board_and_action)
    value_output = Dense(1, activation='tanh') (hidden_layer)
    
    return Model(inputs=[board_input, action_input], outputs=value_output)