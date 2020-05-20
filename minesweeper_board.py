# -*- coding: utf-8 -*-
"""
Created on Wed May 13 18:30:11 2020

@author: Wash
"""
import numpy as np
import copy

class MineSweeperBoard():
    """
    This class will handle the game state and logic in the game
    """
    def __init__(self, num_rows, num_cols, num_mines):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_mines = num_mines
        
    
    def new_game(self):
        """
        Initialize a new game with num_rows, num_cols
        This method does not initialize the mines yet since mines are not set until first point is selected
        
        -1 represents a point that has not been selected
        0 represents no mines in its neighbor
        1-8 represents number of mines in its neighbor
        9 represents a mine
        
        board will represent the board the system sees, which contains all the bomb location
        player_board will not contain the bomb location
        """
        board = np.full((self.num_rows, self.num_cols), -1)
        self.board = board
        self.player_board = copy.deepcopy(self.board)
        self.first_move = False
        self.game_over = False
        self.explored = self.num_rows * self.num_cols - self.num_mines 
        
    def select_move(self, move):
        """
        Player selects a move and update the board
        
        Initialize the bombs if that's the case
        """
        if not move.validate_move():
            return
        if not self.first_move:
            self._initialize_mines(move)
        
        self._select_move(move)
        
    def _select_move(self, move):
        """
        Utility function that selects the move and checks with the main board to see if the move is placed on a mine
        """
        select_row = move.select_row
        select_col = move.select_col
        board_val = self.board[select_row][select_col]
        
        # Game over if the value is a mine
        if board_val == 9:
            self.game_over = True
        
        # Reveal its val if it has mines around it
        elif board_val > 0:
            self.player_board[select_row][select_col] = board_val
            self.explored -= 1
        
        # Expand the board if val is 0
        else:
            reveal_locations = set([(select_row, select_col)])
            neighbors = set(self.neighbors(select_row, select_col))
            
            while neighbors:
                neighbor = neighbors.pop()
                neighbor_row, neighbor_col = neighbor[0], neighbor[1]
                neighbor_val = self.board[neighbor_row][neighbor_col]
                
                reveal_locations.add(neighbor)
                
                if neighbor_val == 0:
                    neighbor_neighbors = self.neighbors(neighbor_row, neighbor_col)
                    
                    for nn in neighbor_neighbors:
                        p = (nn[0], nn[1])
                        if p not in neighbors and p not in reveal_locations and self.player_board[nn[0]][nn[1]] == -1:
                            neighbors.add( p )

            for loc in reveal_locations:
                loc_row, loc_col = loc[0], loc[1]
                self.player_board[loc_row][loc_col] = self.board[loc_row][loc_col]
            
            self.explored -= len(reveal_locations)
            
    def _initialize_mines(self, move):
        """
        Initialize mines after first move
        Makes the first move valid and never have mines around it and then randomly place mines on the board
        """
        self.board[move.select_row][move.select_col] = 0
        
        possible_mine_locations = []
        move_neighbors = self.neighbors(move.select_row, move.select_col)
        
        # All availble mine locations on the board
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                # Don't place mine around the neighbor of the move
                if (r, c) in move_neighbors or (r, c) == (move.select_row, move.select_col):
                    continue
                possible_mine_locations.append( (r, c) )
        
        mine_locations_index = np.random.choice(np.arange(len(possible_mine_locations)), self.num_mines, replace=False)
        
        # Place mines
        for index in mine_locations_index:
            mine = possible_mine_locations[index]
            r, c = mine[0], mine[1]
            self.board[r][c] = 9
        
        # Update board to reflect how many bombs in its neighbor
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.board[r][c] != -1:
                    continue
                
                point_neighbors = self.neighbors(r, c)
                mine_count = 0
                for neighbor in point_neighbors:
                    if self.board[neighbor[0]][neighbor[1]] == 9:
                        mine_count += 1
                self.board[r][c] = mine_count
        
        self.first_move = True
        
    
    def neighbors(self, row, col):
        """
        Utility function that will return a list of tuples (row, col) that are neighbors to the input row col
        """
        neighbors = []
        for r in range(row-1, row+2):
            if r >= self.num_rows or r < 0:
                continue
            for c in range(col-1,  col+2):
                if c >= self.num_cols or c < 0 or (r == row and c == col):
                    continue
                neighbors.append( (r, c) )
        return neighbors

    def print_board(self, player=True):
        """
        Print the player board if it's true, else print board with mines 
        """
        board = self.player_board if player else self.board
        for r in range(board.shape[0]):
            row_string = ""
            for c in range(board.shape[1]):
                if board[r][c] == -1:
                    row_string += 'o'
                else: 
                    row_string += str(board[r][c])
            print(row_string)
            
            