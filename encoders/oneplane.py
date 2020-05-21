# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:25:29 2020

@author: Wash
"""

from encoders.base import Encoder

class OnePlaneEncoder(Encoder):
    def __init__(self, row, col, mine):
        self.row = row
        self.col = col
        self.mine = mine
        self.num_planes = 1
        
    def name(self):
        return 'oneplane'
    
    def encode(self, game_state):
        """
        This function returns itself since the game state is already encoded correctly for one plane
        
        Parameters
        ----------
        game_state : ndarray
            Player board state

        Returns
        -------
        game_state : ndarray
            Encoded player board state
        """
        return game_state

    def encode_move(self, move):
        """
        Turns boar point into an integer index

        Parameters
        ----------
        move : Move object
            Move with select row and select col

        Returns
        -------
        INT
           Encoded move as an integer 

        """
        return self.col * (move.select_row - 1) + (move.select_col - 1)

    def decode_move_index(self, index):
        row = index // self.col
        col = index % self.col
        return Move(row, col)
    
    def shape(self):
        return self.num_planes, self.row, self.col