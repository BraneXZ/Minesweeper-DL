# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:03:41 2020

@author: Wash
"""

import numpy as np

from agents import Agent
from move import Move

class RandomBot(Agent):
    def select_move(self, player_board):
        moves = []
        
        for r in range(player_board.shape[0]):
            for c in range(player_board.shape[1]):
                if player_board[r][c] == -1:
                    move = Move(r, c, player_board)
                    moves.append(move)
        
        return np.random.choice(moves)
    