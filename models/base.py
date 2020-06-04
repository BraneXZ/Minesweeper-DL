# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:53:38 2020

@author: Wash
"""

import importlib

def get_model_by_name(name, encoder):
    module = importlib.import_module('models.' + name)
    get_model = getattr(module, 'get_model')
    return get_model(encoder)

