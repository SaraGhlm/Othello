import numpy as np
static_weight = np.array([[4, -3, 2, 2, 2, 2, -3, 4],
                              [-3, -4, -1, -1, -1, -1, -4, -3],
                              [2, -1, 1, 0, 0, 1, -1, 2],
                              [2, -1, 0, 1, 1, 0, -1, 2],
                              [2, -1, 0, 1, 1, 0, -1, 2],
                              [2, -1, 1, 0, 0, 1, -1, 2],
                              [-3, -4, -1, -1, -1, -1, -4, -3],
                              [4, -3, 2, 2, 2, 2, -3, 4]])

available = np.zeros((8, 8), dtype=int)
available[1][1] = 1
available[5][1] = 1
available[7][2] = 1
available[1][7] = 1
print(available)

a = np.zeros((5, 5))
print(np.where(available == 1))
