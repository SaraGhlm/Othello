from Logic.player import Player
from Logic.game import Game
import numpy as np
from prettytable import PrettyTable


if __name__ == '__main__':
    players = ['Combination_Beginner', 'Combination_Intermediate', 'Combination_Hard']
    first_player_list = []
    second_player_list = []
    result_list = []
    for i in players:
        for j in players:
            # if i != j:
            second_player = Player(i, 8, 'w')
            first_player = Player(j, 8, 'b')
            second_player_list.append(second_player.name)
            first_player_list.append(first_player.name)
            current_player = 'b'
            board = np.zeros((8, 8))
            board[3][3] = 1
            board[3][4] = 2
            board[4][3] = 2
            board[4][4] = 1
            game = Game(8)
            result, _ = game.game_over(board=board)
            while result is False:
                if current_player == 'w':
                    loc = second_player.move(board)
                    if loc is not None:
                        board = game.flip_opponent_stones(loc, board, 8, 2, 1)
                    current_player = 'b'
                else:
                    loc = first_player.move(board)
                    if loc is not None:
                        board = game.flip_opponent_stones(loc, board, 8, 1, 2)
                    current_player = 'w'
                result, message = game.game_over(board=board)
            result_list.append(message)
            black_score = sum(sum(board == 1))
            white_score = sum(sum(board == 2))

    for i in range(len(first_player_list)):
        print(first_player_list[i], second_player_list[i], result_list[i])
