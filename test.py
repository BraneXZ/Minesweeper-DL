from keras import Sequential 
import h5py
import os 

from create_experience_files import create_experience, simulate_game
import models
import encoders
import agents
import rl
from scipy.stats import binom_test

binom_test(1000, 10000, .1)

# encoder = encoders.get_encoder_by_name("oneplane", 5, 5, 3)
# model = Sequential()

# for layer in models.get_model_by_name("model1", encoder.shape()):
#     model.add(layer)
    
# agent = agents.get_agent_by_name("policy_agent", model, encoder)

# latest_file_name = -1
# for file_name in os.listdir("experience"):
#     f = file_name.split("_")
    
#     if int(f[-1]) > latest_file_name:
#         latest_file_name = int(f[-1])

# print(latest_file_name)
    