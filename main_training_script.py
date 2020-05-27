# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:19:21 2020

@author: Wash
"""
from keras import Sequential 
import h5py
import os 

from create_experience_files import create_experience, simulate_game
import models
import encoders
import agents
import rl

# Change these variable values to alter the training script
ROWS = 5
COLS = 5
MINES = 3

LR = 0.001
CLIPNORM = 1
BATCH_SIZE = 512
EPOCHS = 10
ITERATIONS = 1

ENCODER_NAME = "oneplane"
AGENT_NAME = "policy_agent"
MODEL_NAME = "model1"

SAVE_AGENT = True
AGENT_FILE_NAME = "policy_agent_param2"
LOAD_AGENT = True


encoder = encoders.get_encoder_by_name(ENCODER_NAME, ROWS, COLS, MINES)
model = Sequential()

for layer in models.get_model_by_name(MODEL_NAME, encoder.shape()):
    model.add(layer)

if LOAD_AGENT:
    with h5py.File(AGENT_FILE_NAME, 'r') as prev_agent:
        agent = agents.load_agent_by_name(AGENT_NAME, prev_agent)
else:
    agent = agents.get_agent_by_name(AGENT_NAME, model, encoder)

# print("Creating 100,000 games with updated agent")
# create_experience(agent, model, ROWS, COLS, MINES, 10)
        
for i in range(ITERATIONS):
    
    print(f"Performing iteration: {i+1}")
    num = -1
    for file_name in os.listdir("experience"):
        exp = file_name.split("_")
        
        exp_row = int(exp[0][:-1])
        exp_col = int(exp[1][:-1])
        exp_mine = int(exp[2][:-1])
        
        if exp_row == ROWS and exp_col == COLS and exp_mine == MINES:
            exp_buffer = rl.experience.load_experience(h5py.File( "experience/" + file_name, 'r'))
            agent.train(exp_buffer, lr=LR, clipnorm=CLIPNORM, batch_size=BATCH_SIZE, epochs=EPOCHS)
            
            if SAVE_AGENT:
                with h5py.File(AGENT_FILE_NAME, 'w') as updated_agent:
                    agent.serialize(updated_agent)
            num += 1
            if num == 1:
                break
        
win = 0
for i in range(10000):
    if simulate_game(agent, ROWS, COLS, MINES) == 1:
        win += 1

print(f'New updated agent win rate: {win}/10000')
    