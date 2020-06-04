# -*- coding: utf-8 -*-
"""
Created on Fri May 22 10:11:56 2020

@author: Wash
"""
import numpy as np

class ExperienceBuffer:
    def __init__(self, states, actions, rewards, advantages):
        self.states = states
        self.actions = actions
        self.rewards = rewards
        self.advantages = advantages 
        
    def serialize(self, h5file):
        h5file.create_group('experience')
        h5file['experience'].create_dataset('states', data=self.states)
        h5file['experience'].create_dataset('actions', data=self.actions)
        h5file['experience'].create_dataset('rewards', data=self.rewards)
        h5file['experience'].create_dataset('advantages', data=self.advantages)

class ExperienceCollector:
    def __init__(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.advantages = []
        
        self.current_episode_states = []
        self.current_episode_actions = []
        self.current_episode_rewards = []
        self.current_episode_estimated_value = []
        
    def begin_episode(self):
        self.current_episode_states = []
        self.current_episode_actions = []
        self.current_episode_rewards = []
        self.current_episode_estimated_value = []
        
    def record_decision(self, state, action, estimated_value=0):
        self.current_episode_states.append(state)
        self.current_episode_actions.append(action)
        self.current_episode_estimated_value.append(estimated_value)
        
    def record_reward(self, reward):
        self.current_episode_rewards.append(reward)
        
    def complete_episode(self):
        num_states = len(self.current_episode_states)
        self.states += self.current_episode_states
        self.actions += self.current_episode_actions
        self.rewards += self.current_episode_rewards
        
        for i in range(num_states):
            advantage = self.current_episode_rewards[i] - self.current_episode_estimated_value[i]
            self.advantages.append(advantage)
            
        self.current_episode_states = []
        self.current_episode_actions = []
        self.current_episode_rewards = []
        self.current_episode_estimated_value = []
        
    def to_buffer(self):
        return ExperienceBuffer(
            states = np.array(self.states),
            actions = np.array(self.actions),
            rewards = np.array(self.rewards),
            advantages = np.array(self.advantages)
        )
    
    def reset_collector(self):
        self.states = []
        self.actions = []
        self.rewards = []
        
def load_experience(h5file):
    return ExperienceBuffer(
        states = np.array(h5file['experience']['states']),
        actions = np.array(h5file['experience']['actions']),
        rewards = np.array(h5file['experience']['rewards']),
        advantages = np.array(h5file['experience']['advantages']))
