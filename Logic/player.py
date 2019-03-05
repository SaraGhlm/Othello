import numpy as np
from Logic.game import Game
import time


# need to get move_validity_check rows and columns from second-page so only checks places where it has a valid move
# evaluation function needs to evaluate the value of different move and gives each possible board a value
# player will choose the one with highest score

class Player:
    def __init__(self, level, board_size, computer_color, type="static"):
        self.level = level
        self.board_size = board_size
        self.computer_color = computer_color
        self.opponent_color = 'w' if self.computer_color == 'b' else 'b'
        self.computer_num = 1 if self.computer_color == 'b' else 2
        self.opponent_num = 1 if self.computer_color == 'w' else 2
        self.game = Game(self.board_size)
        self.type = type

    def move(self, board):
        if self.type == "static":
            return self.static_player(board)
        elif self.type == "stability":
            return self.stability(board)

    def static_player(self, board):
        static_weight = np.array([[4, -3, 2, 2, 2, 2, -3, 4],
                                  [-3, -4, -1, -1, -1, -1, -4, -3],
                                  [2, -1, 1, 0, 0, 1, -1, 2],
                                  [2, -1, 0, 1, 1, 0, -1, 2],
                                  [2, -1, 0, 1, 1, 0, -1, 2],
                                  [2, -1, 1, 0, 0, 1, -1, 2],
                                  [-3, -4, -1, -1, -1, -1, -4, -3],
                                  [4, -3, 2, 2, 2, 2, -3, 4]])
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
                move_value += static_weight[stone_rows[j]][stone_columns[j]]
            if move_value > max_value:
                max_value = move_value
                location = (rows[i], columns[i])
        return location

    def stability_player(self, board):
        valid_moves = self.game.find_valid_moves(self.computer_color, board, self.board_size)
        rows, columns = np.where(valid_moves == 1)
        max_stability = -200
        location = (-2, -2)
        for i in range(len(rows)):
            temp_board = np.copy(board)
            temp_board = self.game.flip_opponent_stones((rows[i], columns[i]), temp_board, self.board_size,
                                                        self.computer_num, self.opponent_num)
            stability_value = self.stability(temp_board)
            print(stability_value)
            print(rows[i], columns[i])
            if stability_value > max_stability:
                max_stability = stability_value
                location = (rows[i], columns[i])
                print(location)

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

        temp = np.zeros(board.shape)
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == 0 and valid_moves_computer[i][j] == 0:
                    list_of_i = [i, i + 1, i - 1]
                    list_of_j = [j, j + 1, j - 1]
                    for k in list_of_i:
                        for l in list_of_j:
                            if (k, l) != (i, j):
                                if -1 < k < 8 and -1 < l < 8:
                                    if board[k][l] == self.opponent_num and temp[i][j] == 0:
                                        computer_counter += 1
                                        temp[i][j] = 1
                                        break

        valid_moves_opponent = self.game.find_valid_moves(self.opponent_color, board, self.board_size)
        opponent_counter = 0

        temp = np.zeros(board.shape)
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == 0 and valid_moves_opponent[i][j] == 0:
                    list_of_i = [i, i + 1, i - 1]
                    list_of_j = [j, j + 1, j - 1]
                    for k in list_of_i:
                        for l in list_of_j:
                            if (k, l) != (i, j):
                                if -1 < k < 8 and -1 < l < 8:
                                    if board[k][l] == self.computer_num and temp[i][j] == 0:
                                        opponent_counter += 1
                                        temp[i][j] = 1
                                        break
        print(computer_counter, opponent_counter)
        return 100 * (computer_counter - opponent_counter) / (computer_counter + opponent_counter)

    def corners(self, board):
        # Calculating already captured corners
        computer_corners = 0
        computer_corners = computer_corners + 1 if board[0][0] == self.computer_num else computer_corners
        computer_corners = computer_corners + 1 if board[0][
                                                       self.board_size - 1] == self.computer_num else computer_corners
        computer_corners = computer_corners + 1 if board[self.board_size - 1][
                                                       0] == self.computer_num else computer_corners
        computer_corners = computer_corners + 1 if board[self.board_size - 1][
                                                       self.board_size - 1] == self.computer_num else computer_corners

        opponent_corners = 0
        opponent_corners = opponent_corners + 1 if board[0][0] == self.opponent_num else opponent_corners
        opponent_corners = opponent_corners + 1 if board[0][
                                                       self.board_size - 1] == self.opponent_num else opponent_corners
        opponent_corners = opponent_corners + 1 if board[self.board_size - 1][
                                                       0] == self.opponent_num else opponent_corners
        opponent_corners = opponent_corners + 1 if board[self.board_size - 1][
                                                       self.board_size - 1] == self.opponent_num else opponent_corners

        # Calculating potential corners
        valid_moves_computer = self.game.find_valid_moves(self.computer_color, board, self.board_size)
        computer_potential_corner = 0
        computer_potential_corner = computer_potential_corner + 1 if valid_moves_computer[0][
                                                                         0] == 1 else computer_potential_corner
        computer_potential_corner = computer_potential_corner + 1 if valid_moves_computer[0][
                                                                         self.board_size - 1] == 1 else computer_potential_corner
        computer_potential_corner = computer_potential_corner + 1 if valid_moves_computer[self.board_size - 1][
                                                                         0] == 1 else computer_potential_corner
        computer_potential_corner = computer_potential_corner + 1 if valid_moves_computer[self.board_size - 1][
                                                                         self.board_size - 1] == 1 else computer_potential_corner

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

        # Calculating potential corners for both players
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
        print(computer_corners, opponent_corners, computer_potential_corner, opponent_potential_corner,
              common_potential_corner)
        return 100 * numerator / denominator

    def stability(self, board):
        # Stable stones
        computer_board = self.get_stable_stones(board, self.computer_num)
        computer_stable = sum(sum(computer_board == 100))
        opponent_board = self.get_stable_stones(board, self.opponent_num)
        opponent_stable = sum(sum(opponent_board == 100))
        # print("computer stable ", computer_stable)
        # print(computer_board)
        # print("opponent stable ", opponent_stable)
        # print(opponent_board)

        # Unstable stones are the ones which can be flanked in the next move
        computer_board = self.get_unstable_stones(board, self.opponent_color, self.computer_num,
                                                  self.opponent_num, computer_board)
        computer_unstable = sum(sum(computer_board == 200))
        opponent_board = self.get_unstable_stones(board, self.computer_color, self.opponent_num,
                                                  self.computer_num, opponent_board)
        opponent_unstable = sum(sum(opponent_board == 200))
        # print("computer unstable ", computer_unstable)
        # print(computer_board)
        # print("opponent unstable ", opponent_unstable)
        # print(opponent_board)
        # # the reset is semi stable with weight 0, so it is not important
        #
        computer_stability = computer_stable - computer_unstable
        opponent_stability = opponent_stable - opponent_unstable
        # print(computer_stability, opponent_stability)

        if computer_stability + opponent_stability != 0:
            return 100 * (computer_stability - opponent_stability) / (
                        computer_stable + computer_unstable + opponent_stable + opponent_unstable)
        else:
            return 0

    def get_stable_stones(self, board, number):
        horizontal = True
        vertical = True
        left_to_right = True
        right_to_left = True
        temp_board = np.copy(board)
        for i in range(len(board[0])):
            for j in range(len(board[0])):
                if board[i][j] == number:
                    # check horizontal direction
                    if 0 < i < 7:
                        if board[i - 1][j] != number and board[i + 1][j] != number:
                            horizontal = False
                    # check vertical direction
                    if 0 < j < 7:
                        if board[i][j - 1] != number and board[i][j + 1] != number:
                            vertical = False
                    # check left to right and right to left directions
                    if 0 < i < 7 and 0 < j < 7:
                        if board[i - 1][j - 1] != number and board[i + 1][j + 1] != number:
                            left_to_right = False
                        if board[i - 1][j + 1] != number and board[i + 1][j - 1] != number:
                            right_to_left = False

                    # if all are true, then stone is stable
                    if horizontal and vertical and left_to_right and right_to_left:
                        temp_board[i][j] = 100
                    else:
                        horizontal = True
                        vertical = True
                        left_to_right = True
                        right_to_left = True
        return temp_board

    def get_unstable_stones(self, board, opponent_color, player_number, opponent_number, temp_board):
        opponent_valid_moves = self.game.find_valid_moves(opponent_color, board, len(board[0]))
        rows, columns = np.where(opponent_valid_moves == 1)
        for i in range(len(rows)):
            moved_board = np.copy(board)
            moved_board = self.game.flip_opponent_stones((rows[i], columns[i]), moved_board, self.board_size,
                                                         opponent_number, player_number)
            diff = np.isclose(board, moved_board)
            diff_rows, diff_columns = np.where(diff == False)
            for j in range(len(diff_rows)):
                if temp_board[diff_rows[j]][diff_columns[j]] != 200:
                    temp_board[diff_rows[j]][diff_columns[j]] = 200
            temp_board[rows[i]][columns[i]] = 0
        return temp_board


if __name__ == '__main__':
    player = Player("", 8, 'b')
    board = np.zeros((8, 8))
    board[0][0] = 1
    board[0][1] = 1
    board[0][2] = 1
    board[1][1] = 1
    board[2][1] = 2
    board[1][2] = 2
    # board[2][2] = 1
    # board[0][7] = 1
    board[3][3] = 1
    board[3][4] = 2
    board[4][3] = 2
    board[4][4] = 1
    # board[7][7] = 2
    # board[7][0] = 2
    print(board)
    print(player.stability(board))
