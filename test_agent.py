# -*- coding: utf-8 -*-
"""
Created on Sat May 23 17:19:12 2020

@author: Wash
"""

import h5py

import agents
from create_experience_files import simulate_game

AGENT_FILE_NAME = "policy_agent_param"
AGENT_NAME = "policy_agent"
NUM_GAMES = 10000

with h5py.File(AGENT_FILE_NAME, 'r') as prev_agent:
    agent = agents.load_agent_by_name(AGENT_NAME, prev_agent)
    
    
win = 0
for i in range(NUM_GAMES):    
    if simulate_game(agent, 5, 5, 3) == 1:
        win += 1

print(win/NUM_GAMES)
