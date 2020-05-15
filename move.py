# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:44:43 2020

@author: Wash
"""

class Move:
    """
    Player selects a move by row and column and the board
    This class will also provide validation for the move
    """
    def __init__(self, select_row, select_col, player_board):
        self.select_row = select_row
        self.select_col = select_col
        self.player_board = player_board
        
    def validate_move(self):
        """
        Validate the move
        Move is valid as long as it is within the size of the board
        and the selected move has -1 on the board
        """
        player_board_rows = self.player_board.shape[0]
        player_board_cols = self.player_board.shape[1]
        
        if self.select_row >= player_board_rows or self.select_row < 0 or \
            self.select_col >= player_board_cols or self.select_col < 0 or \
            self.player_board[self.select_row][self.select_col] != -1:
            return False
        return True
    
    