# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:53:38 2020

@author: Wash
"""

import importlib

def get_model_by_name(name, input_shape):
    module = importlib.import_module('models.' + name)
    layer = getattr(module, 'layers')
    return layer(input_shape)

