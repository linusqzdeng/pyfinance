# Concate two numpy arrays of N x P and M xP

import numpy as np

n, m, p = map(int, input().strip().split())

arr_np = np.array([input().split() for _ in range(n)], int)
arr_mp = np.array([input().split() for _ in range(m)], int)

arr_concat = np.concatenate((arr_np, arr_mp))

print(arr_concat)
