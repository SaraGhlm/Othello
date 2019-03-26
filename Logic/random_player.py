from Logic.game import Game
import random
import numpy as np


class RandomPlayer:
    def __init__(self, board_size, color):
        self.board_size = board_size
        self.color = color
        self.number = 1 if self.color == 'b' else 2
        self.game = Game(self.board_size)

    def move(self, board):
        valid_moves = self.game.find_valid_moves(self.color, board, self.board_size)
        rows, columns = np.where(valid_moves == 1)
        index = random.randint(0, len(rows) - 1)
        return rows[index], columns[index]

    def get_color(self):
        return self.color
