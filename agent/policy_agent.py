# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:05:05 2020

@author: Wash
"""
import h5py
from keras import kerasutil

from agent.base import Agent

class PolicyAgent(Agent):
    def __init__(self, model, encoder):
        self.model = model
        self.encoder = encoder 
        
    def select_move(self, player_board):
        board_tensor = self.encoder.encode(player_board)
        X = np.array([board_tensor])
        move_probs = self.model.predict(X)[0]
        
        
        
    def serialize(self, h5file):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = self.encoder.name()
        h5file['encoder'].attrs['row'] = self.encoder.row
        h5file['encoder'].attrs['col'] = self.encoder.col
        h5file['encoder'].attrs['mine'] = self.encoder.mine
        h5file.create_group('model')
        kerasutil.save_model_to_hdf5_group(self.model, h5file['model'])
        
        
def load_policy_agent(h5file):
    model = kerasutil.load_model_from_hdf5_group(h5file['model'])
    encoder_name = h5file['encoder'].attrs['name']
    row = h5file['encoder'].attrs['row']
    col = h5file['encoder'].attrs['col']
    mine = h5file['encoder'].attrs['mine']
    encoder = encoders.get_encoder_by_name(encoder_name, row, col, mine)
    return PolicyAgent(model, encoder)