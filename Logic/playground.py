from Logic.player import Player
from Logic.game import Game
import numpy as np


if __name__ == '__main__':
    players = ['static', 'parity', 'mobility', 'pmobility', 'corners', 'stability']
    for i in players:
        for j in players:
            if i != j:
                second_player = Player('beginner', 8, 'w', i)
                first_player = Player('beginner', 8, 'b', j)
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
                        board = game.flip_opponent_stones(second_player.move(board), board, 8, 2, 1)
                        current_player = 'b'
                    else:
                        board = game.flip_opponent_stones(first_player.move(board), board, 8, 1, 2)
                        current_player = 'w'
                    result, message = game.game_over(board=board)
                black_score = sum(sum(board == 1))
                white_score = sum(sum(board == 2))
                print(i, j, message, white_score, black_score)
