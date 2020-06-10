# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:05:36 2020

@author: Wash
"""
import h5py
import os 

from minesweeper_board import MineSweeperBoard
from rl import experience

def simulate_game(player, row, col, mine):
    board = MineSweeperBoard(row, col, mine)
    board.new_game()
    
    while board.status == 0:
        next_move = player.select_move(board.player_board)
        board.select_move(next_move)
        
        if player.collector is not None:
            if board.status == -1:
                player.collector.record_reward(-1)
            else:
                player.collector.record_reward(1)
                
    return board.status


def create_experience(player, model, rows, cols, mines, num_files, games_per_file=10000):
    collector = experience.ExperienceCollector()
    player.set_collector(collector)
    
    # Determine the latest file_num and start from that number + 1
    latest_file_num = -1
    for file_name in os.listdir("experience"):
        if int(file_name.split("_")[-1]) > latest_file_num:
            latest_file_num = int(file_name.split("_")[-1])
            
    
    latest_file_num += 1
    for i in range(latest_file_num, latest_file_num + num_files):
        for _ in range(games_per_file):
            if _ % (games_per_file // 10) == 0:
                print(f"Simulating game {_}/{games_per_file}")
                
            collector.begin_episode()
            
            game_record = simulate_game(player, rows, cols, mines)
            collector.complete_episode()
            
                
        with h5py.File(f"experience/{rows}r_{cols}c_{mines}m_{i}", 'w') as experience_outf:
            collector.to_buffer().serialize(experience_outf)
        
        collector.reset_collector()