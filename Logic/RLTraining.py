import numpy as np



def convert_board_to_index(board):
    index = 0
    for i in range(board.shape[0]):
        for j in range(board.shape[0]):
            index *= 3
            index += board[i][j]
    return int(index)



board_size = 3
value = {}
test = np.zeros((board_size, board_size))
test[0][0] = 2
print(test)
print(convert_board_to_index(test))

print(value[convert_board_to_index(test)])

