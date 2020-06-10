# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:19:21 2020

@author: Wash
"""
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

LR = .01
CLIPNORM = 1
BATCH_SIZE = 512
EPOCHS = 1
ITERATIONS = 1
TEMPERATURE = 0             

NUM_GAMES = BATCH_SIZE * 10

ENCODER_NAME = "oneplane"
AGENT_NAME = "policy_agent"
MODEL_NAME = "policy_gradient_model"

AGENT_FILE_NAME = "policy_param_512_batch_1_layers"
LOAD_AGENT = False
SAVE_AGENT = True

CUR_WINS = 0

encoder = encoders.get_encoder_by_name(ENCODER_NAME, ROWS, COLS, MINES)

model = models.get_model_by_name(MODEL_NAME, encoder)

if LOAD_AGENT:
    with h5py.File(AGENT_FILE_NAME, 'r') as prev_agent:
        agent = agents.load_agent_by_name(AGENT_NAME, prev_agent)
else:
    agent = agents.get_agent_by_name(AGENT_NAME, model, encoder)

if TEMPERATURE:
    agent.set_temperature(TEMPERATURE)
    
        
while True:
    print(f"Creating {NUM_GAMES} games")
    create_experience(agent, model, ROWS, COLS, MINES, 1, NUM_GAMES)
    
    for file_name in os.listdir("experience"):
        exp = file_name.split("_")
        
        exp_row = int(exp[0][:-1])
        exp_col = int(exp[1][:-1])
        exp_mine = int(exp[2][:-1])
        
        if exp_row == ROWS and exp_col == COLS and exp_mine == MINES:
            exp_buffer = rl.experience.load_experience(h5py.File( "experience/" + file_name, 'r'))
            agent.train(exp_buffer, lr=LR, clipnorm=CLIPNORM, batch_size=BATCH_SIZE, epochs=EPOCHS)
            
        # os.remove("experience/" + file_name)
    
    win = 0
    for _ in range(NUM_GAMES//10):
        if _ % (NUM_GAMES // 10) == 0:
            print(f"Simulating game {_}/{NUM_GAMES//10} to test updated agent")
        if simulate_game(agent, ROWS, COLS, MINES) == 1:
            win += 1

    print(f'New updated agent win rate: {win/ (NUM_GAMES//10) }%\n')     
    
    # if CUR_WINS < win and SAVE_AGENT:
    #     CUR_WINS = win
    
    if SAVE_AGENT:
        with h5py.File(AGENT_FILE_NAME, 'w') as updated_agent:
            agent.serialize(updated_agent)
            
    # with h5py.File(AGENT_FILE_NAME, 'r') as prev_agent:
    #     agent = agents.load_agent_by_name(AGENT_NAME, prev_agent)