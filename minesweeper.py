import random
import numpy as np
from flask import Flask, render_template, request, jsonify
from run import db, app

class MineSweeper():
    def __init__(self, nb_lines=3, nb_col = 3, nb_bomb=3):
        self.nb_lines = nb_lines
        self.nb_col   = nb_col
        self.status   = "playing"
        self.field    = np.zeros((nb_col, nb_lines), dtype=np.int)
        self.mask     = np.zeros((nb_col, nb_lines), dtype=np.int)

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
            return
        if ((self.mask.sum() + len(self.bombPositions)) == (self.nb_col * self.nb_lines)):
            self.status = 'win'
        else:
            self.status = 'playing'

@app.route("/minesweeper/test", methods=['POST'])
def test():
    test = request.get_json()
    print(test)
    return jsonify(test)

mines = "prout"
@app.route("/minesweeper/init", methods=['POST'])
def get_init():
    global mines
    init = request.get_json()
    print(init)
    size = init['grid_size']
    nb_bomb = init['nb_bomb']
    print(size, nb_bomb)
    mines = MineSweeper(size, size, nb_bomb)
    grid = mines.getGrid()
    print(grid)
    return jsonify({"status":"Start", "grid":grid.tolist()})


@app.route("/minesweeper/pos", methods=['POST'])
def get_pos():
    global mines
    pos = request.get_json()
    print(pos)
    X = int(pos['x'])
    Y = int(pos['y'])
    status, grid = mines.clickOnTile(X, Y)
    print(status)
    return jsonify({"status":status, "grid":grid.tolist()})
