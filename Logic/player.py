import numpy as np
from Logic.game import *


# need to get move_validity_check rows and columns from second-page so only checks places where it has a valid move
# evaluation function needs to evaluate the value of different move and gives each possible board a value
# player will choose the one with highest score
def evaluation(board, player_num, board_size):
    opponent = 1
    if player_num == 1:
        opponent = 2

    valid_moves = find_valid_moves(player_num, board, board_size)
    rows, columns = np.where(valid_moves == 1)

    max_value = -100
    best_move = (0, 0)
    for i in range(len(rows)):
        temp_board = np.copy(board)
        temp_board = flip_opponent_stones((rows[i], columns[i]), temp_board, board_size, player_num, opponent)
        player_score = sum(sum(temp_board == player_num))
        opponent_score = sum(sum(temp_board == opponent))
        total_value = player_score - opponent_score
        if total_value > max_value:
            max_value = total_value
            best_move = (rows[i], columns[i])

    return best_move
