# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:05:36 2020

@author: Wash
"""
import h5py

from minesweeper_board import MineSweeperBoard
from rl import experience

def simulate_game(player, row, col, mine):
    board = MineSweeperBoard(row, col, mine)
    board.new_game()
    
    while board.status == 0:
        next_move = player.select_move(board.player_board)
        board.select_move(next_move)

    return board.status


def create_experience(player, model, rows, cols, mines, num_files, games_per_file):
    collector = experience.ExperienceCollector()
    player.set_collector(collector)
    
    for i in range(num_files):
        print(f'Creating file {i}/{num_files}')
        for _ in range(games_per_file):
            collector.begin_episode()
            
            game_record = simulate_game(player, rows, cols, mines)
            collector.complete_episode(reward=game_record)
            
                
        with h5py.File(f"experience/{rows}r_{cols}c_{mines}m_{i}", 'w') as experience_outf:
            collector.to_buffer().serialize(experience_outf)
        
        collector.reset_collector()