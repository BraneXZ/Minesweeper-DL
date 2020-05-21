# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:13:00 2020

@author: Wash
"""

class Encoder:
    def name(self):
        raise NotImplementedError()
        
    def encode(self, game_state):
        raise NotImplementedError()
        
    def encode_move(self, move):
        raise NotImplementedError()
    
    def decode_move_(self, move):
        raise NotImplementedError()
        
    def shape(self):
        raise NotImplementedError()
        
import importlib

def get_encoer_by_name(name, row, col, mine):
    """
    

    Parameters
    ----------
    name : str
        Name of the encoder
    row : int
        Number of rows 
    col : int
        Number of columns
    mine : int
        Number of mines

    Returns
    -------
    Encoder object
        Returns the specified encoder object using the name parameter

    """
    module = importlib.import_module('encoders.' + name)
    constructor = getattr(module, 'create')
    return constructor(row, col, mine)