import numpy as np
from Logic.player import HeuristicPlayer

class game:

    def __init__(self, board_size, user_color, game_type):
        """

        :param board_size:
        :param user_color: whether black or white
        :param game_type: 1 -> human vs human, 2 -> human -> computer ??
        """
        self.board_size = board_size
        self.game_type = game_type
        self.user_color = user_color
        self.board = np.zeros((self.board_size, self.board_size))
        self.current_player = 'b'
        self.computer_color = 'b' if user_color != 'b' else 'w'
        self.computer_player = HeuristicPlayer("Beginner", self.board_size, self.computer_color)

    def init_board(self):
        center = (int(self.board_size / 2), int(self.board_size / 2))
        # current_board is a matrix of zeros. 1 is for black and 2 is for white stones
        self.current_board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.move_validity_check = np.zeros((self.board_size, self.board_size), dtype=int)
        self.board[center[0] - 1][center[1]] = 1
        self.board[center[0]][center[1]] = 2
        self.board[center[0]][center[1] - 1] = 1
        self.board[center[0] - 1][center[1] - 1] = 2
        # if self.computer_color == self.current_player:
        #     loc = self.computer_player.move(self.current_board)
        #     self.place_stone(self.computer_color, loc)
        # self.show_valid_moves()

    def run(self):
        while not self.game_over():
            if self.current_player == self.user_color:
                # let user move

            else:




    def game_over(self):
        # true if game is over, false otherwise
        return False

    def flip_opponent_stones(loc, current_board, board_size, player_num, opponent):
        """

        :param loc: location of player move
        :param player_num: player number (aka color)
        :param opponent: opponent number (aka color)
        :param current_board: the board player moved on
        :param board_size: board size
        :return: the board after flips are applied
        """
        # flip stones above current stone
        opponent_stones = 0
        for i in range(loc[0] - 1, -1, -1):
            if current_board[i][loc[1]] == 0:
                break
            elif current_board[i][loc[1]] == opponent:
                opponent_stones += 1
            elif current_board[i][loc[1]] == player_num and opponent_stones != 0:
                for j in range(i, loc[0] + 1):
                    current_board[j][loc[1]] = player_num
                break
        # flip stones bellow current stone
        opponent_stones = 0
        for i in range(loc[0] + 1, board_size):
            if current_board[i][loc[1]] == 0:
                break
            elif current_board[i][loc[1]] == opponent:
                opponent_stones += 1
            elif current_board[i][loc[1]] == player_num and opponent_stones != 0:
                for j in range(loc[0], i + 1):
                    current_board[j][loc[1]] = player_num
                break

        # flip stones at the right of current stone
        opponent_stones = 0
        for i in range(loc[1] + 1, board_size):
            if current_board[loc[0]][i] == 0:
                break
            elif current_board[loc[0]][i] == opponent:
                opponent_stones += 1
            elif current_board[loc[0]][i] == player_num and opponent_stones != 0:
                for j in range(loc[1], i + 1):
                    current_board[loc[0]][j] = player_num
                break
        # flip stones at the left of current stone
        opponent_stones = 0
        for i in range(loc[1] - 1, -1, -1):
            if current_board[loc[0]][i] == 0:
                break
            elif current_board[loc[0]][i] == opponent:
                opponent_stones += 1
            elif current_board[loc[0]][i] == player_num and opponent_stones != 0:
                for j in range(i, loc[1] + 1):
                    current_board[loc[0]][j] = player_num
                break
        # flip stones at the top right of current stone
        opponent_stones = 0
        try:
            for i in range(1, min(loc[0], board_size - loc[1]) + 1):
                if current_board[loc[0] - i][loc[1] + i] == 0:
                    break
                elif current_board[loc[0] - i][loc[1] + i] == opponent:
                    opponent_stones += 1
                elif current_board[loc[0] - i][loc[1] + i] == player_num and opponent_stones != 0:
                    for j in range(0, i):
                        current_board[loc[0] - j][loc[1] + j] = player_num
                    break
        except:
            pass
        # flip stones at the top left of current stone
        opponent_stones = 0
        try:
            for i in range(1, min(loc[0], loc[1]) + 1):
                if current_board[loc[0] - i][loc[1] - i] == 0:
                    break
                elif current_board[loc[0] - i][loc[1] - i] == opponent:
                    opponent_stones += 1
                elif current_board[loc[0] - i][loc[1] - i] == player_num and opponent_stones != 0:
                    for j in range(0, i):
                        current_board[loc[0] - j][loc[1] - j] = player_num
                    break
        except:
            pass
        # flip stones at the bottom left of current stone
        opponent_stones = 0
        try:
            for i in range(1, min(board_size - loc[0], loc[1]) + 1):
                if current_board[loc[0] + i][loc[1] - i] == 0:
                    break
                elif current_board[loc[0] + i][loc[1] - i] == opponent:
                    opponent_stones += 1
                elif current_board[loc[0] + i][loc[1] - i] == player_num and opponent_stones != 0:
                    for j in range(0, i):
                        current_board[loc[0] + j][loc[1] - j] = player_num
                    break
        except:
            pass
        # flip stones at the bottom right of current stone
        opponent_stones = 0
        try:
            for i in range(1, min(board_size - loc[0], board_size - loc[1]) + 1):
                if current_board[loc[0] + i][loc[1] + i] == 0:
                    break
                elif current_board[loc[0] + i][loc[1] + i] == opponent:
                    opponent_stones += 1
                elif current_board[loc[0] + i][loc[1] + i] == player_num and opponent_stones != 0:
                    for j in range(0, i):
                        current_board[loc[0] + j][loc[1] + j] = player_num
                    break
        except:
            pass
        return current_board


    def find_valid_moves(current_player, board, board_size):
        move_validity_check = np.zeros((board_size, board_size), dtype=int)

        if current_player == 'b':
            rows, columns = np.where(board == 1)
            opponent = 2
        elif current_player == 'w':
            rows, columns = np.where(board == 2)
            opponent = 1
        else:
            raise ValueError('invalid location')
        for i in range(len(rows)):
            # check for valid moves above current stone
            opponent_stones = 0
            for j in range(rows[i] - 1, -1, -1):
                if board[j][columns[i]] != opponent:
                    if opponent_stones != 0 and board[j][columns[i]] == 0:
                        move_validity_check[j][columns[i]] = 1
                    break
                else:
                    opponent_stones += 1
            # check for valid moves bellow current stone
            opponent_stones = 0
            for j in range(rows[i] + 1, board_size):
                if board[j][columns[i]] != opponent:
                    if opponent_stones != 0 and board[j][columns[i]] == 0:
                        move_validity_check[j][columns[i]] = 1
                    break
                else:
                    opponent_stones += 1
            # check for valid moves at the right of current stone
            opponent_stones = 0
            for j in range(columns[i] + 1, board_size):
                if board[rows[i]][j] != opponent:
                    if opponent_stones != 0 and board[rows[i]][j] == 0:
                        move_validity_check[rows[i]][j] = 1
                    break
                else:
                    opponent_stones += 1
            # check for valid moves at the left of current stone
            opponent_stones = 0
            for j in range(columns[i] - 1, -1, -1):
                if board[rows[i]][j] != opponent:
                    if opponent_stones != 0 and board[rows[i]][j] == 0:
                        move_validity_check[rows[i]][j] = 1
                    break
                else:
                    opponent_stones += 1
            # check for valid moves at the right and above the current stone
            opponent_stones = 0
            try:
                for j in range(1, min(rows[i], board_size - columns[i]) + 1):
                    if board[rows[i] - j][columns[i] + j] != opponent:
                        if opponent_stones != 0 and board[rows[i] - j][columns[i] + j] == 0:
                            move_validity_check[rows[i] - j][columns[i] + j] = 1
                        break
                    else:
                        opponent_stones += 1
            except:
                pass
            # check for valid moves at the right and below the current stone
            opponent_stones = 0
            try:
                for j in range(1, min(board_size - rows[i], board_size - columns[i]) + 1):
                    if board[rows[i] + j][columns[i] + j] != opponent:
                        if opponent_stones != 0 and board[rows[i] + j][columns[i] + j] == 0:
                            move_validity_check[rows[i] + j][columns[i] + j] = 1
                        break
                    else:
                        opponent_stones += 1
            except:
                pass
            # check for valid moves at the left and above the current stone
            opponent_stones = 0
            try:
                for j in range(1, min(rows[i], columns[i]) + 1):
                    if board[rows[i] - j][columns[i] - j] != opponent:
                        if opponent_stones != 0 and board[rows[i] - j][columns[i] - j] == 0:
                            move_validity_check[rows[i] - j][columns[i] - j] = 1
                        break
                    else:
                        opponent_stones += 1
            except:
                pass
            # check for valid moves at the left and below the current stone
            opponent_stones = 0
            try:
                for j in range(1, min(board_size - rows[i], columns[i]) + 1):
                    if board[rows[i] + j][columns[i] - j] != opponent:
                        if opponent_stones != 0 and board[rows[i] + j][columns[i] - j] == 0:
                            move_validity_check[rows[i] + j][columns[i] - j] = 1
                        break
                    else:
                        opponent_stones += 1
            except:
                pass
        return move_validity_check