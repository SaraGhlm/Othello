from Logic.player import Player
from Logic.game import Game
import numpy as np
import csv


if __name__ == '__main__':
    players = ['Combination_Easy']
    possible_weights = [20, 60, 80]
    all_possible_weights = []
    first_player_list = []
    second_player_list = []
    result_list = []
    for i in players:
        for j in players:
            # if i != j:
            for k in possible_weights:
                for m in possible_weights:
                    for n in possible_weights:
                        for o in possible_weights:
                            for p in possible_weights:
                                for q in possible_weights:
                                    all_possible_weights.append([k, m, n, o, p, q])

            for k in all_possible_weights:
                for m in all_possible_weights:
                    if m != k:
                        second_player = Player(i, 8, 'w', k)
                        first_player = Player(j, 8, 'b', m)
                        second_player_list.append(second_player.name + str(k))
                        first_player_list.append(first_player.name + str(m))
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
                        print(k, m, message)

    for i in range(len(first_player_list)):
        print(first_player_list[i], second_player_list[i], result_list[i])

    final_results = open('comparison', 'w')
    writer = csv.writer(final_results, delimiter=',')
    for i in range(len(first_player_list)):
        writer.writerow([str(first_player_list[i]), str(second_player_list[i]), str(result_list[i])])
