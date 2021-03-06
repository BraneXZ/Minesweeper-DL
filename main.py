# -*- coding: utf-8 -*-
"""
Created on Tue May 19 10:45:12 2020

@author: Wash
"""

from flask import Flask, request, jsonify, render_template
import os
import h5py 

from minesweeper_board import MineSweeperBoard
from move import Move
import agents


app = Flask(__name__, template_folder="static")
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

board = None
POLICY_AGENT_FILE_NAME = "policy_agent_param2"
Q_LEARNING_AGENT_FILE_NAME = "q_learning_less_games_1"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/newBoard')
def newBoard():
    row = int(request.args.get('row'))
    col = int(request.args.get('col'))
    mine = int(request.args.get('mine'))
    global board
    board = MineSweeperBoard(row, col, mine)
    board.new_game()
    
    response = {
        "board": board.player_board.tolist(),
        "status": board.status
    }
    return jsonify(response)


@app.route('/applyMove')
def applyMove():
    row = int(request.args.get('row'))
    col = int(request.args.get('col'))
    
    move = Move(row, col)
    board.select_move(move)
    
    response = {
        "board": board.player_board.tolist(),
        "status": board.status
    }
    
    return jsonify(response)


@app.route('/playAgent')
def playAgent():
    request_agent = request.args.get('agent')
    if request_agent == "random":
        playing_agent = agents.random_agent.RandomBot()
    elif request_agent == "policy":
        with h5py.File(POLICY_AGENT_FILE_NAME, 'r') as prev_agent:
            playing_agent = agents.load_agent_by_name("policy_agent", prev_agent)
    elif request_agent == "qlearning":
        with h5py.File(Q_LEARNING_AGENT_FILE_NAME, 'r') as prev_agent:
            playing_agent = agents.load_agent_by_name("q_learning_agent", prev_agent)
            
    move = playing_agent.select_move(board.player_board)
    board.select_move(move)
    
    response = {
        "board": board.player_board.tolist(),
        "status": board.status,
        "select_row": str(move.select_row),
        "select_col": str(move.select_col)
    }
    
    return jsonify(response)
    
app.run()

