# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:19:21 2020

@author: Wash
"""
from keras import Sequential 
import h5py
import os 

import models
import encoders
import agents
import rl

# Change these variable values to alter the training script
ROWS = 5 
COLS = 5
MINES = 3

LR = 5
CLIPNORM = 1e-5 
BATCH_SIZE = 1024 

ENCODER_NAME = "oneplane"
AGENT_NAME = "policy_agent"
MODEL_NAME = "model1"

SAVE_AGENT = True
AGENT_FILE_NAME = "policy_agent_param"
LOAD_AGENT = False


encoder = encoders.get_encoder_by_name(ENCODER_NAME, ROWS, COLS, MINES)
model = Sequential()

for layer in models.get_model_by_name(MODEL_NAME, encoder.shape()):
    model.add(layer)

if LOAD_AGENT:
    with h5py.File(AGENT_FILE_NAME, 'r') as prev_agent:
        agent = agents.load_agent_by_name(AGENT_NAME, prev_agent)
else:
    agent = agents.get_agent_by_name(AGENT_NAME, model, encoder)


for file_name in os.listdir("experience"):
    exp = file_name.split("_")
    exp_row = int(exp[0][:-1])
    exp_col = int(exp[1][:-1])
    exp_mine = int(exp[2][:-1])
    
    if exp_row == ROWS and exp_col == COLS and exp_mine == MINES:
        exp_buffer = rl.experience.load_experience(h5py.File( "experience/" + file_name, 'r'))
        agent.train(exp_buffer, lr=LR, clipnorm=CLIPNORM, batch_size=BATCH_SIZE)
        
        if SAVE_AGENT:
            with h5py.File(AGENT_FILE_NAME, 'w') as updated_agent:
                agent.serialize(updated_agent)
                

