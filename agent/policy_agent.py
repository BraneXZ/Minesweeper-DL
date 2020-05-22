# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:05:05 2020

@author: Wash
"""
import h5py
import numpy as np
from keras.optimizers import SGD

from agent.base import Agent
import encoders 
import move 
import kerasutil

class PolicyAgent(Agent):
    def __init__(self, model, encoder):
        self.model = model
        self.encoder = encoder 
        self.collector = None
        
    def select_move(self, player_board):
        board_tensor = self.encoder.encode(player_board)
        X = np.array([[board_tensor]])
        
        move_probs = self.model.predict(X)[0]

        move_probs = clip_probs(move_probs)
        
        num_moves = self.encoder.row * self.encoder.col
        candidates = np.arange(num_moves)
        ranked_moves = np.random.choice(candidates, num_moves, replace=False, p=move_probs)
        
        # Iterate through all moves and select the first possible move to apply
        for point_idx in ranked_moves:
            possible_move = self.encoder.decode_move_index(point_idx)

            if move.validate_move(possible_move, player_board):
                if self.collector is not None:
                    self.collector.record_decision(state=board_tensor, action=point_idx)
                return possible_move        
        
    def serialize(self, h5file):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = self.encoder.name()
        h5file['encoder'].attrs['row'] = self.encoder.row
        h5file['encoder'].attrs['col'] = self.encoder.col
        h5file['encoder'].attrs['mine'] = self.encoder.mine
        h5file.create_group('model')
        kerasutil.save_model_to_hdf5_group(self.model, h5file['model'])
        
    def set_collector(self, collector):
        self.collector = collector

    def train(self, experience, lr, clipnorm, batch_size):
        self.model.compile(
            loss = 'categorical_crossentropy',
            optimizer = SGD(lr=lr, clipnorm=clipnorm)
        )
        
        target_vectors = preprare_experience_data(experience, self.encoder.row, self.encoder.col)
        X = np.expand_dims(experience.states, axis=1)
        
        self.model.fit(X, target_vectors, batch_size=batch_size, epochs=10)
        
def clip_probs(original_probs):
    min_p = 1e-5
    max_p = 1 - min_p 
    clipped_probs = np.clip(original_probs, min_p, max_p)
    clipped_probs /= np.sum(clipped_probs)
    return clipped_probs 

def load_policy_agent(h5file):
    model = kerasutil.load_model_from_hdf5_group(h5file['model'])
    encoder_name = h5file['encoder'].attrs['name']
    row = h5file['encoder'].attrs['row']
    col = h5file['encoder'].attrs['col']
    mine = h5file['encoder'].attrs['mine']
    encoder = encoders.base.get_encoder_by_name(encoder_name, row, col, mine)
    return PolicyAgent(model, encoder)

def preprare_experience_data(experience, row, col):
    experience_size = experience.actions.shape[0]
    target_vectors = np.zeros((experience_size, row * col))
    for i in range(experience_size):
        action = experience.actions[i]
        reward = experience.rewards[i]
        target_vectors[i][action] = reward
    return target_vectors