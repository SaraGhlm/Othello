import numpy as np
from Logic.game import *
import time

# need to get move_validity_check rows and columns from second-page so only checks places where it has a valid move
# evaluation function needs to evaluate the value of different move and gives each possible board a value
# player will choose the one with highest score

class HeuristicPlayer:
    def __init__(self, level, board_size, computer_color):
        self.level = level
        self.board_size = board_size
        self.computer_color = computer_color
        self.computer_num = 1 if self.computer_color == 'b' else 2
        self.opponent_num = 1 if self.computer_color == 'w' else 2
        self.static_weight = np.array([[4, -3, 2, 2, 2, 2, -3, 4],
                              [-3, -4, -1, -1, -1, -1, -4, -3],
                              [2, -1, 1, 0, 0, 1, -1, 2],
                              [2, -1, 0, 1, 1, 0, -1, 2],
                              [2, -1, 0, 1, 1, 0, -1, 2],
                              [2, -1, 1, 0, 0, 1, -1, 2],
                              [-3, -4, -1, -1, -1, -1, -4, -3],
                              [4, -3, 2, 2, 2, 2, -3, 4]])

    # def evaluation(self, board, player_num):
    #     opponent = 1
    #     if player_num == 1:
    #         opponent = 2
    #
    #     valid_moves = find_valid_moves(player_num, board, self.board_size)
    #     rows, columns = np.where(valid_moves == 1)
    #
    #     max_value = -100
    #     best_move = (0, 0)
    #     for i in range(len(rows)):
    #         temp_board = np.copy(board)
    #         temp_board = flip_opponent_stones((rows[i], columns[i]), temp_board, self.board_size, player_num, opponent)
    #         player_score = sum(sum(temp_board == player_num))
    #         opponent_score = sum(sum(temp_board == opponent))
    #         total_value = player_score - opponent_score
    #         if total_value > max_value:
    #             max_value = total_value
    #             best_move = (rows[i], columns[i])
    #
    #     return best_move

    def move(self, board):
        valid_moves = find_valid_moves(self.computer_color, board, self.board_size)
        rows, columns = np.where(valid_moves == 1)
        max_value = -10000000
        location = (-1, -1)
        for i in range(len(rows)):
            move_value = 0
            temp_board = np.copy(board)
            temp_board = flip_opponent_stones((rows[i], columns[i]), temp_board, self.board_size,
                                              self.computer_num, self.opponent_num)
            stone_rows, stone_columns = np.where(temp_board == self.computer_num)
            for j in range(len(stone_rows)):
                move_value += self.static_weight[stone_rows[j]][stone_columns[j]]
            if move_value > max_value:
                max_value = move_value
                location = (rows[i], columns[i])
        return location
