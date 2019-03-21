import numpy as np


class Game:

    def __init__(self, board_size):
        self.board_size = board_size

    def game_over(self, board):
        """
            Based on the current state of the board, determines whether the game is over or not.
            If it is over, returns true and winner message, otherwise false.

        :param board: the current state of the board game

        :return: True, winner message if the game is over, otherwise False.
        """
        black_valid = self.find_valid_moves('b', board, self.board_size)
        white_valid = self.find_valid_moves('w', board, self.board_size)
        if sum(sum(black_valid)) == 0 and sum(sum(white_valid)) == 0:
            black_score = sum(sum(board == 1))
            white_score = sum(sum(board == 2))
            if black_score > white_score:
                message = 'Black won!'
            elif black_score < white_score:
                message = 'white won!'
            else:
                message = 'Tie!'
            return True, message
        else:
            return False, ''

    def flip_opponent_stones(self, loc, current_board, board_size, player_num, opponent):
        """
            Flips all of the opponent's stones that are influenced by the current move.

        :param loc: The location of the current move in the game board
        :param current_board: State of the game board before the current move
        :param board_size: Size of the board
        :param player_num: The number representing the player ( 1 for black player, 2 for white player)
        :param opponent: The number representing the opponent ( 1 for black opponent, 2 for white opponent)

        :return: The state of the board after the current move
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
            else:
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
            else:
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
            else:
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
            else:
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
                else:
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
                else:
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
                else:
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
                else:
                    break
        except:
            pass
        return current_board

    def find_valid_moves(self, current_player, board, board_size):
        """
            Finds all valid moves for the current player in the current state of the board.

            To find all of the valid moves, we first find all the player's stones in the current board.
            For each stone, we find all the possible locations which can be connected to this stone.

        :param current_player: The current player
        :param board: The current state of the board
        :param board_size: Size of the board

        :return: A 0-1 matrix of size board_size where 1s represent the possible valid moves for the player
        """
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

    def get_score(self, board, player_num):
        black_score = sum(sum(board == 1))
        white_score = sum(sum(board == 2))
        if player_num == 1:
            return black_score - white_score
        return white_score - black_score

if __name__ == '__main__':
    game = Game(8)
    board = np.ones((8, 8))
    # board[0][0] = 1
    # board[0][1] = 1
    # board[0][2] = 1
    # board[1][1] = 1
    board[2][1] = 2
    board[1][2] = 2
    # board[2][2] = 1
    # board[0][7] = 1
    # board[3][3] = 1
    board[3][4] = 2
    board[4][3] = 2
    # board[4][4] = 1
    print(board)
    print(game.game_over(board))
