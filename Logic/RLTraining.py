import numpy as np

class Train:
    def __init__(self, board):
        self.board = board
        self.board_values = np.array([[4, -3, 2, 2, 2, 2, -3, 4],
                                 [-3, -4, -1, -1, -1, -1, -4, -3],
                                 [2, -1, 1, 0, 0, 1, -1, 2],
                                 [2, -1, 0, 1, 1, 0, -1, 2],
                                 [2, -1, 0, 1, 1, 0, -1, 2],
                                 [2, -1, 1, 0, 0, 1, -1, 2],
                                 [-3, -4, -1, -1, -1, -1, -4, -3],
                                 [4, -3, 2, 2, 2, 2, -3, 4]])
        self.board_size = board.shape[0]
        self.value = {}

    def convert_board_to_index(self, board):
        index = 0
        for i in range(board.shape[0]):
            for j in range(board.shape[0]):
                index *= 3
                index += board[i][j]
        return int(index)

    def calc_value(self, board):
        result = self.convert_board_to_index(board)
        print(result)
        if result not in self.value.keys():
            self.value[result] = 10
            print(self.value)
