# -*- coding: utf-8 -*-
"""
Created on Fri May 22 10:11:56 2020

@author: Wash
"""
import numpy as np

class ExperienceBuffer:
    def __init__(self, states, actions, rewards):
        self.states = states
        self.actions = actions
        self.rewards = rewards
        
    def serialize(self, h5file):
        h5file.create_group('experience')
        h5file['experience'].create_dataset('states', data=self.states)
        h5file['experience'].create_dataset('actions', data=self.actions)
        h5file['experience'].create_dataset('rewards', data=self.rewards)
        
def load_experience(h5file):
    return ExperienceBuffer(
        states = np.array(h5file['experience']['states']),
        actions = np.array(h5file['experience']['actions']),
        rewards = np.array(h5file['experience']['rewards']))
