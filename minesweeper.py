import random
import numpy as np
from flask import Flask, render_template, request, jsonify
from run import db, app, socketio
from flask_socketio import send, emit
from boulynk_socket import authenticated_only
from flask_login import current_user
import json


class MineSweeper():
    def __init__(self, nb_lines=3, nb_col = 3, nb_bomb=3):
        self.nb_lines = nb_lines
        self.nb_col   = nb_col
        self.status   = "playing"
        self.field    = np.zeros((nb_lines, nb_col), dtype=np.int)
        self.mask     = np.zeros((nb_lines, nb_col), dtype=np.int)

        if (nb_bomb < (nb_col * nb_lines)):
            self.bombPositions = sorted(random.sample(range(0, nb_col * nb_lines), nb_bomb))
        else:
            raise Exception("Too many bombs!")

        for position in self.bombPositions:
            line = int(position / nb_col)
            col  = position % nb_col
            # Adding bombs
            self.field[line][col] = -1
            # Adding bomb count around bombs
            for a in range(line-1, line+2):
                for b in range(col-1, col+2):
                    self.smartBombAdd(a, b)

    def getGrid(self):
        return self.mask * self.field

    def smartBombAdd(self, line, col):
        if ((line < 0) or (col < 0) or (line > self.nb_lines-1) or (col > self.nb_col-1)):
            return
        elif (self.field[line][col] == -1):
            return
        else :
            self.field[line][col] = self.field[line][col] + 1

    def clickOnTile(self, line, col):
        if ((line < 0) or (col < 0) or (line > self.nb_lines-1) or (col > self.nb_col-1)):
            return
        self.mask[line][col] = 1
        if (self.field[line][col] == 0):
            self.field[line][col] = -2
            self.clickOnTile(line+1,col)
            self.clickOnTile(line-1,col)
            self.clickOnTile(line, col+1)
            self.clickOnTile(line, col-1)
        self.updateStatus()
        return (self.status, self.mask * self.field)

    def updateStatus(self):
        countMask = 0
        if -1. in self.mask * self.field:
            self.status = 'lose'
            self.mask = np.ones((self.nb_lines, self.nb_col), dtype=np.int)
            self.field = np.where(self.field == 0, -2, self.field)
            return
        if ((self.mask.sum() + len(self.bombPositions)) == (self.nb_col * self.nb_lines)):
            self.status = 'win'
        else:
            self.status = 'playing'

Global_mines = None
def get_boards():
    global Global_mines
    for user_name in Global_mines:
        if current_user.name == user_name:
            user_board = Global_mines[user_name].getUserBoard()
        else:
            opponent_board = Global_mines[user_name].getOpponentBoard()

@app.route("/minesweeper/test", methods=['POST'])
def test():
    test = request.get_json()
    print(test)
    return jsonify(test)

@app.route("/minesweeper/init", methods=['POST'])
def get_init():
    global Global_mines
    init = request.get_json()
    print(init)
    width = init['width']
    height = init['height']
    nb_bomb = init['nb_bomb']
    mines = MineSweeper(height, width, nb_bomb)
    mines2 = mines
    Global_mines = {"paris": mines, "lyon": mines2}
    lyon_board = {
        "status": Global_mines["lyon"].status,
        "grid": Global_mines["lyon"].getGrid().tolist()
    }
    paris_board = {
        "status": Global_mines["paris"].status,
        "grid": Global_mines["paris"].getGrid().tolist()
    }
    socketio.emit('game_update', json.dumps({"user_board":paris_board}), broadcast=True, room="paris")
    socketio.emit('game_update', json.dumps({"user_board":lyon_board}), broadcast=True, room="lyon")
    socketio.emit('game_update', json.dumps({"opponent_board":paris_board}), broadcast=True, room="lyon")
    socketio.emit('game_update', json.dumps({"opponent_board":lyon_board}), broadcast=True, room="paris")
    return jsonify({"status": "Waiting"})


@app.route("/minesweeper/get", methods=['GET'])
def get_minesweeper():
    global Global_mines
    if Global_mines is None:
        return
    payload = {}
    for user_name in Global_mines:
        if current_user.name == user_name:
            payload["user_board"] = {
                "status": Global_mines[user_name].status,
                "grid": Global_mines[user_name].getGrid().tolist()}
        else:
            payload["opponent_board"] = {
                "status": Global_mines[user_name].status,
                "grid": Global_mines[user_name].getGrid().tolist()}

    if payload["user_board"]["status"] == "playing" and payload["opponent_board"]["status"] == "playing":
        return jsonify(payload)
    return jsonify({"no_grid": True})


@app.route("/minesweeper/pos", methods=['POST'])
def get_pos():
    global Global_mines
    pos = request.get_json()
    X = int(pos['x'])
    Y = int(pos['y'])
    return jsonify({"status":status, "grid":grid.tolist()})

@socketio.on('grid_click')
@authenticated_only
def handle_grid_click(pos):
    pos = json.loads(pos)
    global Global_mines
    print(f"{current_user.name} is ready")
    print(pos)
    X = int(pos['x'])
    Y = int(pos['y'])

    status, grid = Global_mines[current_user.name].clickOnTile(X, Y)
    board = {
        "status": status,
        "grid": grid.tolist()
    }
    print(status)
    for user_name in Global_mines:
        if current_user.name == user_name:
            socketio.emit('game_update', json.dumps({"user_board":board}), broadcast=True, room=user_name)
        else:
            socketio.emit('game_update', json.dumps({"opponent_board":board}), broadcast=True, room=user_name)
    # emit('user_ready', f"{current_user.name} is ready", broadcast=True)


@socketio.on('user_ready')
@authenticated_only
def handle_user_ready(message):
    print(f"{current_user.name} is ready")
    emit('user_ready', f"{current_user.name} is ready", broadcast=True)
