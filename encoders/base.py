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
        