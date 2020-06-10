# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 11:28:52 2020

@author: Wash
"""

from encoders.base import Encoder
from move import Move
import numpy as np

class TwoPlaneEncoder(Encoder):
    def __init__(self, row, col, mine):
        self.row = row
        self.col = col
        self.mine = mine
        self.num_planes = 2
        
    def name(self):
        return 'twoplane'
    
    def encode(self, game_state):
        """
        Encode the game_state to two planes
        First plane marks 1 for unclicked points
        Second plane marks 1-8 for number of mines surround that point (ignoring 0)

        Parameters
        ----------
        game_state : TYPE
            Current game state

        Returns
        -------
        list
            Encoded board state

        """
        first_plane = np.zeros( (game_state.shape) ) 
        second_plane = np.zeros( (game_state.shape) )
        
        for r in range(game_state.shape[0]):
            for c in range(game_state.shape[1]):
                val = game_state[r, c]
                if val == -1:
                    first_plane[r, c] = 1
                elif val > 0:
                    second_plane[r, c] = val
        
        return [first_plane, second_plane]
        
    def encode_move(self, move):
        """
        Turns board point into an integer index

        Parameters
        ----------
        move : Move object
            Move with select row and select col

        Returns
        -------
        INT
           Encoded move as an integer 

        """
        return self.col * (move.select_row) + (move.select_col)

    def decode_move_index(self, index):
        row = index // self.col
        col = index % self.col
        return Move(row, col)
    
    def num_points(self):
        return self.row * self.col
    
    def shape(self):
        return self.num_planes, self.row, self.col
    
def create(row, col, mine):
    return TwoPlaneEncoder(row, col, mine)
        