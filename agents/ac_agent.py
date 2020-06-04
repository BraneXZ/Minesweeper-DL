# -*- coding: utf-8 -*-
"""
Created on Thu May 29 11:05:05 2020

@author: Wash
"""
import h5py
import numpy as np
from keras.optimizers import SGD

from agents import Agent
import encoders 
import move 
import kerasutil

class ACAgent(Agent):
    def __init__(self, model, encoder):
        self.model = model
        self.encoder = encoder 
        self.collector = None
        
    def select_move(self, player_board):
        board_tensor = self.encoder.encode(player_board)
        X = np.array([board_tensor])
        
        actions, values = self.model.predict(X)
        move_probs = actions[0]
        estimated_value = values[0][0]
        
        move_probs = clip_probs(move_probs)
        
        num_moves = self.encoder.row * self.encoder.col
        candidates = np.arange(num_moves)
        
        # Randomly choose the first move since it can never lose
        if np.sum(player_board) == -num_moves:
            ranked_moves = np.random.choice(candidates, num_moves, replace=False)
        else:
            ranked_moves = np.random.choice(candidates, num_moves, replace=False, p=move_probs)
        
        # Iterate through all moves and select the first possible move to apply
        for point_idx in ranked_moves:
            possible_move = self.encoder.decode_move_index(point_idx)

            if move.validate_move(possible_move, player_board):
                if self.collector is not None:
                    self.collector.record_decision(state=board_tensor, action=point_idx, estimated_value=estimated_value)
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

    def train(self, experience, lr, clipnorm, batch_size, epochs):
        self.model.compile(
            loss = ['categorical_crossentropy', 'mse'],
            optimizer = SGD(lr=lr),
            loss_weights=[1, .5]
        )

        n = experience.states.shape[0]
        num_moves = self.encoder.num_points()
        policy_target = np.zeros((n, num_moves))
        value_target = np.zeros((n, ))
        
        for i in range(n):
            action = experience.actions[i]
            policy_target[i][action] = experience.advantages[i]
            reward = experience.rewards[i]
            value_target[i] = reward
            
        self.model.fit(experience.states, [policy_target, value_target], batch_size=batch_size, epochs=epochs)
        
        
def create(model, encoder):
    return ACAgent(model, encoder)

def clip_probs(original_probs):
    min_p = 1e-5
    max_p = 1 - min_p 
    clipped_probs = np.clip(original_probs, min_p, max_p)
    clipped_probs /= np.sum(clipped_probs)
    return clipped_probs 

def load(h5file):
    model = kerasutil.load_model_from_hdf5_group(h5file['model'])
    encoder_name = h5file['encoder'].attrs['name']
    row = h5file['encoder'].attrs['row']
    col = h5file['encoder'].attrs['col']
    mine = h5file['encoder'].attrs['mine']
    encoder = encoders.base.get_encoder_by_name(encoder_name, row, col, mine)
    return ACAgent(model, encoder)
