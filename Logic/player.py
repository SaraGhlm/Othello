import numpy as np
from Logic.game import Game
import time


# need to get move_validity_check rows and columns from second-page so only checks places where it has a valid move
# evaluation function needs to evaluate the value of different move and gives each possible board a value
# player will choose the one with highest score

class HeuristicPlayer:
    def __init__(self, level, board_size, computer_color):
        self.level = level
        self.board_size = board_size
        self.computer_color = computer_color
        self.opponent_color = 'w' if self.computer_color == 'b' else 'b'
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
        self.game = Game(self.board_size)

    def move(self, board):
        valid_moves = self.game.find_valid_moves(self.computer_color, board, self.board_size)
        rows, columns = np.where(valid_moves == 1)
        max_value = -10000000
        location = (-1, -1)
        for i in range(len(rows)):
            move_value = 0
            temp_board = np.copy(board)
            temp_board = self.game.flip_opponent_stones((rows[i], columns[i]), temp_board, self.board_size,
                                                        self.computer_num, self.opponent_num)
            stone_rows, stone_columns = np.where(temp_board == self.computer_num)
            for j in range(len(stone_rows)):
                move_value += self.static_weight[stone_rows[j]][stone_columns[j]]
            if move_value > max_value:
                max_value = move_value
                location = (rows[i], columns[i])
        return location

    def coin_parity(self, board):
        computer_score = sum(sum(board == self.computer_num))
        opponent_score = sum(sum(board == self.opponent_num))
        return 100 * (computer_score - opponent_score) / (computer_score + opponent_score)

    def mobility(self, board):
        valid_moves_computer = sum(sum(self.game.find_valid_moves(self.computer_color, board, self.board_size)))
        valid_moves_opponent = sum(sum(self.game.find_valid_moves(self.opponent_color, board, self.board_size)))

        if valid_moves_computer == 0 and valid_moves_opponent == 0:
            return 0
        else:
            return 100 * (valid_moves_computer - valid_moves_opponent) / (valid_moves_computer + valid_moves_opponent)

    def potential_mobility(self, board):
        valid_moves_computer = self.game.find_valid_moves(self.computer_color, board, self.board_size)
        computer_counter = 0

        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == 0 and valid_moves_computer[i][j] == 0:
                    list_of_i = [i, i + 1, i - 1]
                    list_of_j = [j, j + 1, j - 1]
                    for k in list_of_i:
                        for l in list_of_j:
                            if (k, l) != (i, j):
                                try:
                                    if board[k][l] == self.opponent_num:
                                        computer_counter += 1
                                        break
                                except:
                                    pass

        valid_moves_opponent = self.game.find_valid_moves(self.opponent_color, board, self.board_size)
        opponent_counter = 0

        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == 0 and valid_moves_opponent[i][j] == 0:
                    list_of_i = [i, i + 1, i - 1]
                    list_of_j = [j, j + 1, j - 1]
                    for k in list_of_i:
                        for l in list_of_j:
                            if (k, l) != (i, j):
                                try:
                                    if board[k][l] == self.computer_num:
                                        opponent_counter += 1
                                        break
                                except:
                                    pass
        return 100 * (computer_counter - opponent_counter) / (computer_counter + opponent_counter)

    def corners(self, board):
        # Calculating already captured corners
        computer_corners = 0
        computer_corners = computer_corners + 1 if board[0][0] == self.computer_num else computer_corners
        computer_corners = computer_corners + 1 if board[0][self.board_size - 1] == self.computer_num else computer_corners
        computer_corners = computer_corners + 1 if board[self.board_size - 1][0] == self.computer_num else computer_corners
        computer_corners = computer_corners + 1 if board[self.board_size - 1][self.board_size - 1] == self.computer_num else computer_corners

        opponent_corners = 0
        opponent_corners = opponent_corners + 1 if board[0][0] == self.opponent_num else opponent_corners
        opponent_corners = opponent_corners + 1 if board[0][self.board_size - 1] == self.opponent_num else opponent_corners
        opponent_corners = opponent_corners + 1 if board[self.board_size - 1][0] == self.opponent_num else opponent_corners
        opponent_corners = opponent_corners + 1 if board[self.board_size - 1][
                                                 self.board_size - 1] == self.opponent_num else opponent_corners

        # Calculating potential corners
        valid_moves_computer = self.game.find_valid_moves(self.computer_color, board, self.board_size)
        computer_potential_corner = 0
        computer_potential_corner = computer_potential_corner + 1 if valid_moves_computer[0][0] == 1 else computer_potential_corner
        computer_potential_corner = computer_potential_corner + 1 if valid_moves_computer[0][self.board_size - 1] == 1 else computer_potential_corner
        computer_potential_corner = computer_potential_corner + 1 if valid_moves_computer[self.board_size - 1][0] == 1 else computer_potential_corner
        computer_potential_corner = computer_potential_corner + 1 if valid_moves_computer[self.board_size - 1][self.board_size - 1] == 1 else computer_potential_corner

        valid_moves_opponent = self.game.find_valid_moves(self.opponent_color, board, self.board_size)
        opponent_potential_corner = 0
        opponent_potential_corner = opponent_potential_corner + 1 if valid_moves_opponent[0][
                                                                         0] == 1 else opponent_potential_corner
        opponent_potential_corner = opponent_potential_corner + 1 if valid_moves_opponent[0][
                                                                         self.board_size - 1] == 1 else opponent_potential_corner
        opponent_potential_corner = opponent_potential_corner + 1 if valid_moves_opponent[self.board_size - 1][
                                                                         0] == 1 else opponent_potential_corner
        opponent_potential_corner = opponent_potential_corner + 1 if valid_moves_opponent[self.board_size - 1][
                                                                         self.board_size - 1] == 1 else opponent_potential_corner

        valid_moves = valid_moves_opponent + valid_moves_computer
        common_potential_corner = 0
        common_potential_corner = common_potential_corner + 1 if valid_moves[0][
                                                                         0] == 2 else common_potential_corner
        common_potential_corner = common_potential_corner + 1 if valid_moves[0][
                                                                         self.board_size - 1] == 1 else common_potential_corner
        common_potential_corner = common_potential_corner + 1 if valid_moves[self.board_size - 1][
                                                                         0] == 2 else common_potential_corner
        common_potential_corner = common_potential_corner + 1 if valid_moves[self.board_size - 1][
                                                                         self.board_size - 1] == 2 else common_potential_corner

        numerator = computer_corners + computer_potential_corner - 2 * common_potential_corner - opponent_corners - computer_potential_corner
        denominator = computer_corners + computer_potential_corner + 2 * common_potential_corner + opponent_corners + computer_potential_corner
        print(computer_corners, opponent_corners, computer_potential_corner, opponent_potential_corner, common_potential_corner)
        return 100 * numerator / denominator


if __name__ == '__main__':
    player = HeuristicPlayer("", 8, 'b')
    board = np.zeros((8, 8))
    # board[0][0] = 1
    board[0][1] = 1
    board[0][2] = 2
    board[0][7] = 2
    board[1][1] = 2
    board[1][2] = 1
    board[2][2] = 1
    board[3][3] = 1
    board[3][4] = 2
    board[4][3] = 2
    board[4][4] = 1
    board[7][7] = 1
    board[7][0] = 2
    print(board)
    print(player.corners(board))
