# -*- coding: utf-8 -*-
"""
Created on Wed May 27 13:40:16 2020

@author: Wash
"""
import numpy as np
from keras.optimizers import SGD

from agents import Agent
import encoders 
import move 
import kerasutil

class QAgent(Agent):
    def __init__(self, model, encoder):
        self.model = model
        self.encoder = encoder
        self.collector = None
        self.temperature = 0.0
    
    def set_temperature(self, temperature):
        """
        Temperature is the epsilon value that controls how randomized the policy is
        """
        self.temperature = temperature
        
    def set_collector(self, collector):
        self.collector = collector 
        
    def select_move(self, player_board):
        board_tensor = self.encoder.encode(player_board)
        
        valid_moves = []
        board_tensors = []
        for r in range(player_board.shape[0]):
            for c in range(player_board.shape[1]):
                possible_move = move.Move(r, c)
                if move.validate_move(possible_move, player_board):
                    valid_moves.append(self.encoder.encode_move(possible_move))
                    board_tensors.append(board_tensor)
                    
        # One-hot encoding all the valid moves                    
        num_moves = len(valid_moves)
        board_tensors = np.array(board_tensors)
        move_vectors = np.zeros( (num_moves, self.encoder.num_points()) )        
        
        for i, m in enumerate(valid_moves):
            move_vectors[i][m] = 1
        
        values = self.model.predict([board_tensors, move_vectors])
        values = values.reshape(num_moves)
        
        ranked_moves = self.rank_moves_eps_greedy(values)
        
        for move_idx in ranked_moves:
            decoded_move = self.encoder.decode_move_index(valid_moves[move_idx])
            
            if move.validate_move(decoded_move, player_board):
                if self.collector is not None:
                    self.collector.record_decision(state=board_tensor, action=valid_moves[move_idx])
                return decoded_move
        
    def rank_moves_eps_greedy(self, values):
        if np.random.random() < self.temperature:
            values = np.random.random(values.shape)
        ranked_moves = np.argsort(values)
        
        return ranked_moves[::-1]
    
    def train(self, experience, lr, clipnorm, batch_size, epochs):
        opt = SGD(lr=lr)
        self.model.compile(loss='mse', optimizer=opt) # mse because we're learning a continous value
        
        n = experience.states.shape[0]
        num_moves = self.encoder.num_points()
        
        y = np.zeros((n,))
        actions = np.zeros((n,num_moves))
        
        for i in range(n):
            action = experience.actions[i]
            reward = experience.rewards[i]
            actions[i][action] = 1
            y[i] = reward
        
        self.model.fit([experience.states, actions], y, batch_size=batch_size, epochs=epochs)
        
    def serialize(self, h5file):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = self.encoder.name()
        h5file['encoder'].attrs['row'] = self.encoder.row
        h5file['encoder'].attrs['col'] = self.encoder.col
        h5file['encoder'].attrs['mine'] = self.encoder.mine
        h5file.create_group('model')
        kerasutil.save_model_to_hdf5_group(self.model, h5file['model'])
        
        
def create(model, encoder):
    return QAgent(model, encoder)

def load(h5file):
    model = kerasutil.load_model_from_hdf5_group(h5file['model'])
    encoder_name = h5file['encoder'].attrs['name']
    row = h5file['encoder'].attrs['row']
    col = h5file['encoder'].attrs['col']
    mine = h5file['encoder'].attrs['mine']
    encoder = encoders.base.get_encoder_by_name(encoder_name, row, col, mine)
    return QAgent(model, encoder)

def preprare_experience_data(experience, row, col):
    experience_size = experience.actions.shape[0]
    target_vectors = np.zeros((experience_size, row * col))
    for i in range(experience_size):
        action = experience.actions[i]
        reward = experience.rewards[i]
        target_vectors[i][action] = reward
    return target_vectors    