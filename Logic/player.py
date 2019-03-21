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
        """
            Based on the current board and player type, we return the computer player's best move.

            Each player calculates a specific value for all of the possible moves, and returns the
            location with the maximum value.
        :param board: the current state of the board
        :return: A tuple representing the location of computer player's move
        """
        if self.type == "static":
            return self.static_player(board)
        elif self.type == "parity":
            return self.parity_player(board)
        elif self.type == "mobility":
            return self.mobility_player(board)
        elif self.type == "pmobility":
            return self.potential_mobility_player(board)
        elif self.type == "corners":
            return self.corners_player(board)
        elif self.type == "stability":
            return self.stability_player(board)
        elif self.type == "combination":
            return self.combination_player(board)

    def static_player(self, board):
        """
            Static player uses a static matrix which gives specific weight to each location of the board.
            The value of each move is the sum of the weights of all of the locations containing the
            computer player's stones
        :param board: the current state of the board
        :return: A tuple representing the location of static player's move
        """
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

    def combination_player(self, board):
        valid_moves = self.game.find_valid_moves(self.computer_color, board, self.board_size)
        print("valid moves")
        print(valid_moves)
        print("board")
        print(board)
        rows, columns = np.where(valid_moves == 1)

        temp_board = np.copy(board)
        temp_board = self.game.flip_opponent_stones((rows[0], columns[0]), temp_board, self.board_size,
                                                    self.computer_num, self.opponent_num)
        value = 600 * self.stability(temp_board) + 801.724 * self.corners(temp_board) + 78.922 * self.mobility(
            temp_board) + 77 * self.potential_mobility(temp_board) + 74.396 * self.stone_parity(temp_board)

        max_score = value
        location = (rows[0], columns[0])
        for i in range(1, len(rows)):
            temp_board = np.copy(board)
            temp_board = self.game.flip_opponent_stones((rows[i], columns[i]), temp_board, self.board_size,
                                                        self.computer_num, self.opponent_num)
            value = 600 * self.stability(temp_board) + 801.724 * self.corners(temp_board) + 78.922 * self.mobility(
                temp_board) + 77 * self.potential_mobility(temp_board) + 74.396 * self.stone_parity(temp_board)
            if value > max_score:
                max_score = value
                location = (rows[i], columns[i])

        return location

    def stability_player(self, board):
        """
            Stability player uses the stability characteristic of the stones
        :param board: the current state of the board
        :return: A tuple representing the location of stability player's move
        """
        valid_moves = self.game.find_valid_moves(self.computer_color, board, self.board_size)
        rows, columns = np.where(valid_moves == 1)
        max_stability = -200
        location = (-2, -2)
        for i in range(len(rows)):
            temp_board = np.copy(board)
            temp_board = self.game.flip_opponent_stones((rows[i], columns[i]), temp_board, self.board_size,
                                                        self.computer_num, self.opponent_num)
            stability_value = self.stability(temp_board)
            if stability_value > max_stability:
                max_stability = stability_value
                location = (rows[i], columns[i])

        return location

    def parity_player(self, board):
        """
            Parity player uses the parity characteristic of the stones
        :param board: the current state of the board
        :return: A tuple representing the location of parity player's move
        """
        valid_moves = self.game.find_valid_moves(self.computer_color, board, self.board_size)
        rows, columns = np.where(valid_moves == 1)
        max_parity = -200
        location = (-2, -2)
        for i in range(len(rows)):
            temp_board = np.copy(board)
            temp_board = self.game.flip_opponent_stones((rows[i], columns[i]), temp_board, self.board_size,
                                                        self.computer_num, self.opponent_num)
            parity_value = self.stone_parity(temp_board)
            if parity_value > max_parity:
                max_parity = parity_value
                location = (rows[i], columns[i])

        return location

    def mobility_player(self, board):
        """
            Mobility player uses the mobility characteristic of the stones
        :param board: the current state of the board
        :return: A tuple representing the location of mobility player's move
        """
        valid_moves = self.game.find_valid_moves(self.computer_color, board, self.board_size)
        rows, columns = np.where(valid_moves == 1)
        max_mobility = -200
        location = (-2, -2)
        for i in range(len(rows)):
            temp_board = np.copy(board)
            temp_board = self.game.flip_opponent_stones((rows[i], columns[i]), temp_board, self.board_size,
                                                        self.computer_num, self.opponent_num)
            mobility_value = self.stone_parity(temp_board)
            if mobility_value > max_mobility:
                max_mobility = mobility_value
                location = (rows[i], columns[i])
        return location

    def potential_mobility_player(self, board):
        """
            Potential mobility player uses the potential mobility characteristic of the stones
        :param board: the current state of the board
        :return: A tuple representing the location of potential mobility player's move
        """
        valid_moves = self.game.find_valid_moves(self.computer_color, board, self.board_size)
        rows, columns = np.where(valid_moves == 1)
        max_potential_mobility = -200
        location = (-2, -2)
        for i in range(len(rows)):
            temp_board = np.copy(board)
            temp_board = self.game.flip_opponent_stones((rows[i], columns[i]), temp_board, self.board_size,
                                                        self.computer_num, self.opponent_num)
            potential_mobility_value = self.stone_parity(temp_board)
            if potential_mobility_value > max_potential_mobility:
                max_potential_mobility = potential_mobility_value
                location = (rows[i], columns[i])
        return location

    def corners_player(self, board):
        """
            Corners player uses the corners characteristic of the stones
        :param board: the current state of the board
        :return: A tuple representing the location of corners player's move
        """
        valid_moves = self.game.find_valid_moves(self.computer_color, board, self.board_size)
        rows, columns = np.where(valid_moves == 1)
        max_corners = -200
        location = (-2, -2)
        for i in range(len(rows)):
            temp_board = np.copy(board)
            temp_board = self.game.flip_opponent_stones((rows[i], columns[i]), temp_board, self.board_size,
                                                        self.computer_num, self.opponent_num)
            corners_value = self.stone_parity(temp_board)
            if corners_value > max_corners:
                max_corners = corners_value
                location = (rows[i], columns[i])
        return location

    def stone_parity(self, board):
        """
            The stone parity value is based on the players' immediate score after a specific move.
        :param board: the current state of the board
        :return: parity value
        """
        computer_score = sum(sum(board == self.computer_num))
        opponent_score = sum(sum(board == self.opponent_num))
        return 100 * (computer_score - opponent_score) / (computer_score + opponent_score)

    def mobility(self, board):
        """
            The mobility value is based on the players' immediate possible moves after a specific move.
        :param board: the current state of the board
        :return: mobility value
        """
        valid_moves_computer = sum(sum(self.game.find_valid_moves(self.computer_color, board, self.board_size)))
        valid_moves_opponent = sum(sum(self.game.find_valid_moves(self.opponent_color, board, self.board_size)))

        if valid_moves_computer + valid_moves_opponent == 0:
            return 0
        else:
            return 100 * (valid_moves_computer - valid_moves_opponent) / (valid_moves_computer + valid_moves_opponent)

    def potential_mobility(self, board):
        """
            The potential mobility value is based on the players' potential possible moves after a specific
             move in the near future.
        :param board: the current state of the board
        :return: potential mobility value
        """
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
        if computer_counter + opponent_counter == 0:
            return 0
        return 100 * (computer_counter - opponent_counter) / (computer_counter + opponent_counter)

    def corners(self, board):
        """
            The corners value is based on the players' current and potential captured corners after a specific move.
        :param board: the current state of the board
        :return: corners value
        """
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
        denominator = computer_corners + computer_potential_corner + 2 * common_potential_corner + opponent_corners \
                      + computer_potential_corner
        if denominator == 0:
            return 0
        return 100 * numerator / denominator

    def stability(self, board):
        """
            The stability value is based on the players' stable and unstable stones after a specific move.
            A stable stone is a stone that cannot be replaced by the opponent's stone.
            An unstable stone is a stone that can be replaced by the opponent's stone in its next move.
        :param board: the current state of the board
        :return: stability value
        """
        # Stable stones
        computer_board = self.get_stable_stones(board, self.computer_num)
        computer_stable = sum(sum(computer_board == 100))
        opponent_board = self.get_stable_stones(board, self.opponent_num)
        opponent_stable = sum(sum(opponent_board == 100))

        # Unstable stones are the ones which can be flanked in the next move
        computer_board = self.get_unstable_stones(board, self.opponent_color, self.computer_num,
                                                  self.opponent_num, computer_board)
        computer_unstable = sum(sum(computer_board == 200))
        opponent_board = self.get_unstable_stones(board, self.computer_color, self.opponent_num,
                                                  self.computer_num, opponent_board)
        opponent_unstable = sum(sum(opponent_board == 200))
        # the reset is semi stable with weight 0, so it is not important
        computer_stability = computer_stable - computer_unstable
        opponent_stability = opponent_stable - opponent_unstable

        if computer_stable + opponent_stable != 0:
            return 100 * (computer_stable - opponent_stable) / (computer_stable + opponent_stable)
        else:
            return 0

    def get_stable_stones(self, board, player_number):
        """
            Finds all the stable stones of the given player in the current board
        :param board: the current state of the board
        :param player_number: the player's number
        :return: A board which shows the stable stones of the given player
        """
        horizontal = True
        vertical = True
        left_to_right = True
        right_to_left = True
        temp_board = np.copy(board)
        board_border = self.board_size - 1
        change = False

        #  Check corners for stones as they are always stable
        if temp_board[0][0] == player_number:
            temp_board[0][0] = 100
            change = True
        if temp_board[0][board_border] == player_number:
            temp_board[0][board_border] = 100
            change = True
        if temp_board[board_border][0] == player_number:
            temp_board[board_border][0] = 100
            change = True
        if temp_board[board_border][board_border] == player_number:
            temp_board[board_border][board_border] = 100
            change = True

        while change:
            change = False
            for i in range(len(board[0])):
                for j in range(len(board[0])):
                    if board[i][j] == player_number and temp_board[i][j] != 100 and self.is_stable(temp_board, (i, j)):
                        temp_board[i][j] = 100
                        change = True
        # while change:
        #     change = False
        #     for i in range(len(board[0])):
        #         for j in range(len(board[0])):
        #             if temp_board[i][j] == 100:
        #                 continue
        #             if board[i][j] == player_number:
        #                 # check horizontal direction
        #                 if 0 < i < board_border:
        #                     if board[i - 1][j] != player_number and board[i + 1][j] != player_number:
        #                         horizontal = False
        #                 # check vertical direction
        #                 if 0 < j < board_border:
        #                     if board[i][j - 1] != player_number and board[i][j + 1] != player_number:
        #                         vertical = False
        #                 # check left to right and right to left directions
        #                 if 0 < i < board_border and 0 < j < board_border:
        #                     if board[i - 1][j - 1] != player_number and board[i + 1][j + 1] != player_number:
        #                         left_to_right = False
        #                     if board[i - 1][j + 1] != player_number and board[i + 1][j - 1] != player_number:
        #                         right_to_left = False
        #
        #                 # if all are true, it still need to be beside an edge or another stable stone
        #                 if horizontal and vertical and left_to_right and right_to_left:
        #                     if i == 0 or i == board_border or j == 0 or j == board_border:
        #                         temp_board[i][j] = 100
        #                         change = True
        #                     elif temp_board[i - 1][j] == 100 or temp_board[i + 1][j] == 100 or \
        #                             temp_board[i][j - 1] == 100 or temp_board[i][j + 1] == 100:
        #                         temp_board[i][j] = 100
        #                         change = True
        #                 else:
        #                     horizontal = True
        #                     vertical = True
        #                     left_to_right = True
        #                     right_to_left = True
        return temp_board

    def is_stable(self, stability_board, loc):
        board_border = self.board_size - 1
        horizontal = False
        vertical = False
        left_to_right = False
        right_to_left = False
        if 0 < loc[0] < board_border:
            if stability_board[loc[0] - 1][loc[1]] == 100 or stability_board[loc[0] + 1][loc[1]] == 100:
                horizontal = True
        else:
            horizontal = True

        if 0 < loc[1] < board_border:
            if stability_board[loc[0]][loc[1] - 1] == 100 or stability_board[loc[0]][loc[1] + 1] == 100:
                vertical = True
        else:
            vertical = True

        if 0 < loc[0] < board_border and 0 < loc[1] < board_border:
            if stability_board[loc[0] - 1][loc[1] - 1] == 100 or stability_board[loc[0] + 1][loc[1] + 1] == 100:
                left_to_right = True
            if stability_board[loc[0] + 1][loc[1] - 1] == 100 or stability_board[loc[0] - 1][loc[1] + 1] == 100:
                right_to_left = True
        else:
            left_to_right = True
            right_to_left = True

        return horizontal and vertical and right_to_left and left_to_right

    def get_unstable_stones(self, board, opponent_color, player_number, opponent_number, temp_board):
        """
            Finds all the unstable stones of the given player in the current board.
        :param board: The current state of the board
        :param opponent_color: the opponent's number
        :param player_number: the player's number
        :param opponent_number: the opponent's number
        :param temp_board: A board which shows the stable stones of the given player
        :return: temp_board which shows the stable and unstable stones of the given player
        """
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
    board[3][3] = 1
    board[3][4] = 2
    board[4][3] = 2
    board[4][4] = 1

    board[0][0] = 1
    board[0][1] = 1
    board[1][0] = 1
    board[1][1] = 1
    board[2][0] = 1
    board[2][2] = 1
    board[3][2] = 1
    board[2][3] = 1
    board[1][3] = 1
    board[0][3] = 1
    board[2][4] = 1
    board[2][5] = 1
    board[2][6] = 1
    board[2][7] = 1
    board[1][7] = 1
    board[0][7] = 1
    board[0][6] = 1
    board[0][5] = 1
    board[0][4] = 1
    board[1][6] = 1
    board[1][5] = 1
    board[1][4] = 1

    # board[2][2] = 1
    # board[0][7] = 1
    # board[7][7] = 2
    # board[7][0] = 2
    print(board)
    # print(player.stability(board))
    print(player.get_stable_stones(board, 1))
