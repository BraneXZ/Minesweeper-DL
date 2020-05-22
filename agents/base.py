# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:02:21 2020

@author: Wash
"""

class Agent:
    def __init__(self):
        pass

    def select_move(self, player_board):
        raise NotImplementedError()
        
        
import importlib

def get_agent_by_name(name, model, encoder):
    module = importlib.import_module('agents.' + name)
    constructor = getattr(module, "create")
    return constructor(model, encoder)

def load_agent_by_name(name, h5file):
    module = importlib.import_module('agents.' + name)
    constructor = getattr(module, "load")
    return constructor(h5file)