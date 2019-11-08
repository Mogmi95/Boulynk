import random
import numpy as np
from flask import Flask, render_template, request, jsonify
from run import db, app
import json

from sqlalchemy import Column, Integer, ForeignKey, orm
from run import db

class MineSweeper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _field  =  db.Column(db.String, default=[])
    _mask   =  db.Column(db.String, default=[])
    _bombPositions   =  db.Column(db.String, default=[])
    status  = db.Column(db.String)

    @property
    def field(self):
        if self.np_field is not None:
            return self.np_field
        self.np_field = np.array(json.loads(self._field))
        return self.np_field

    @field.setter
    def field(self, value):
        self._field = json.dumps(value.tolist())

    @property
    def mask(self):
        if self.np_mask is not None:
            return self.np_mask
        self.np_mask = np.array(json.loads(self._mask))
        return self.np_mask

    @mask.setter
    def mask(self, value):
        self._mask = json.dumps(value.tolist())

    @property
    def bombPositions(self):
        return np.array(json.loads(self._bombPositions))

    @bombPositions.setter
    def bombPositions(self, value):
        self._bombPositions = json.dumps(value)

    def getGrid(self):
        return self.mask * self.field

    def __init__(self, nb_lines=3, nb_col=3, nb_bomb=3):
        self.nb_lines = nb_lines
        self.nb_col = nb_col
        self.status = "playing"
        self.np_field = None
        self.np_mask = None
        self.field = np.zeros((nb_col, nb_lines), dtype=np.int)
        self.mask = np.zeros((nb_col, nb_lines), dtype=np.int)
        print(nb_lines, nb_col, nb_bomb, self.status)
        if (nb_bomb < (nb_col * nb_lines)):
            self.bombPositions = sorted(random.sample(
                range(0, nb_col * nb_lines), nb_bomb))
        else:
            raise Exception("Too many bombs!")

        for position in self.bombPositions:
            line = int(position / nb_col)
            col = position % nb_col
            # Adding bombs
            self.field[line][col] = -1
            # Adding bomb count around bombs
            for a in range(line-1, line+2):
                for b in range(col-1, col+2):
                    self.smartBombAdd(a, b)
        print("field", self.field)

    @orm.reconstructor
    def init_on_load(self):
        self.np_field = None
        self.np_mask = None


    def smartBombAdd(self, line, col):
        field_ = self.field
        if ((line < 0) or (col < 0) or (line > self.nb_lines-1) or (col > self.nb_col-1)):
            return
        elif (field_[line][col] == -1):
            return
        else:
            field_[line][col] = field_[line][col] + 1

    def save(self):
        self.field = self.np_field
        self.mask = self.np_mask

    def clickOnTile(self, line, col):
        if ((line < 0) or (col < 0) or (line > len(self.field)-1) or (col > len(self.field[0])-1)):
            return
        self.mask[line][col] = 1
        if (self.field[line][col] == 0):
            self.field[line][col] = -2
            self.clickOnTile(line+1, col)
            self.clickOnTile(line-1, col)
            self.clickOnTile(line, col+1)
            self.clickOnTile(line, col-1)
        self.updateStatus()
        return (self.status, self.mask * self.field)

    def updateStatus(self):
        nb_col = len(self.field[0])
        nb_lines = len(self.field)
        if -1. in self.mask * self.field:
            self.status = 'lose'
            self.mask = np.ones((nb_lines, nb_col), dtype=np.int)
            return
        if ((self.mask.sum() + len(self.bombPositions)) == (nb_col * nb_lines)):
            self.status = 'win'
        else:
            self.status = 'playing'


@app.route("/minesweeper/test", methods=['POST'])
def test():
    test = request.get_json()
    print(test)
    return jsonify(test)

@app.route("/minesweeper/init", methods=['POST'])
def get_init():
    global mines
    init = request.get_json()
    # print(init)
    size = init['grid_size']
    nb_bomb = init['nb_bomb']
    print(size, nb_bomb)
    mines = MineSweeper.query.first()
    if mines is None:
        mines = MineSweeper(size, size, nb_bomb)
        db.session.add(mines)
    else:
        mines = MineSweeper(size, size, nb_bomb)
    mines.save()
    db.session.commit()
    print(mines.field)
    grid = mines.getGrid()
    # print(grid)
    return jsonify({"status":"Start", "grid":grid.tolist()})

@app.route("/minesweeper/get", methods=['GET'])
def get_minesweeper():
    global mines
    if mines is None:
        return jsonify({"status":"no_grid"})
    return jsonify({"status":mines.status, "grid":mines.getGrid().tolist()})


@app.route("/minesweeper/pos", methods=['POST'])
def get_pos():
    global mines
    pos = request.get_json()
    print(pos)
    X = int(pos['x'])
    Y = int(pos['y'])
    mines = MineSweeper.query.first()
    print(mines.field)
    status, grid = mines.clickOnTile(X, Y)
    mines.save()
    db.session.commit()
    print(status)
    return jsonify({"status":status, "grid":grid.tolist()})
