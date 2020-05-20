# -*- coding: utf-8 -*-
"""
Created on Tue May 19 10:45:12 2020

@author: Wash
"""

from flask import Flask, request, jsonify, render_template, redirect, abort
import json
import os
import numpy as np

from minesweeper_board import MineSweeperBoard
from move import Move

app = Flask(__name__, template_folder="static")
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

board = None

@app.route('/', methods=['GET', 'POST'])
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
    return jsonify(board.player_board.tolist())


@app.route('/applyMove')
def applyMove():
    row = int(request.args.get('row'))
    col = int(request.args.get('col'))
    
    move = Move(row, col, board.player_board)
    board.select_move(move)
    print(board.explored)
    
    if board.game_over:
        return jsonify(-1)
    elif board.explored == 0:
        return jsonify(1)
    return jsonify(board.player_board.tolist())
    
app.run()