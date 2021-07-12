# Using numpy to transpose an array and flatten the array into
# one-dimension

import numpy as np

n, m = map(int, input().split())    # define the NXM array shape

arr = np.reshape(np.array(list(map(int, input().split()))), (n, m))     # reshape the array to NXM

arr_t = np.transpose(arr)
arr_f = arr_t.flatten()

print(arr_t, arr_f)
