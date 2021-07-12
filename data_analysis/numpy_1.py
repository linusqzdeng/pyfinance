# Using numpy to convert a list of nine integers to
# 3X3 numpy array.

import numpy as np

raw_list = list(map(int, input().strip().split()))

new_list = np.reshape(raw_list, (3, 3))     # reshape the one-dimension array to 3X3
print(new_list)

print(new_list.shape)       # print out the shape of the list
