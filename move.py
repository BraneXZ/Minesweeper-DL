# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:44:43 2020

@author: Wash
"""

class Move:
    """
    Player selects a move by row and column
    """
    def __init__(self, select_row, select_col):
        self.select_row = select_row
        self.select_col = select_col

def validate_move(move, player_board):
    """
    Validate the move
    Move is valid as long as it is within the size of the board
    and the selected move has -1 on the board

    Parameters
    ----------
    move : move object
        Move selected
    player_board : ndarray
        Current board state

    Returns
    -------
    bool
        True if move is valid false otherwise

    """
    select_row = move.select_row
    select_col = move.select_col
    
    player_board_rows = player_board.shape[0]
    player_board_cols = player_board.shape[1]
    
    if select_row >= player_board_rows or select_row < 0 or \
        select_col >= player_board_cols or select_col < 0 or \
        player_board[select_row][select_col] != -1:
        return False
    return True
    
    