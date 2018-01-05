import numpy as np
import timeit
import time

from numba import double
from numba.decorators import jit, autojit
from scipy.spatial.distance import cdist

X = np.random.random((10000, 3))

def pairwise_python(X):
    M = X.shape[0]
    N = X.shape[1]
    D = np.empty((M, M), dtype=np.float)
    for i in range(M):
        for j in range(M):
            d = 0.0
            for k in range(N):
                tmp = X[i, k] - X[j, k]
                d += tmp * tmp
            D[i, j] = np.sqrt(d)
    return D

pairwise_numba = autojit(pairwise_python)

#t = time.time()
#D = pairwise_python(X)
#print("time: %f" % (time.time() - t))
#print(D)
t = time.time()
D = pairwise_numba(X)
print("time: %f" % (time.time() - t))
print(D)
t = time.time()
D = cdist(X,X)
print(D)
print("time: %f" % (time.time() - t))

'''
if __name__ == '__main__':
    import timeit
    X = np.random.random((1000, 3))
    print(timeit.timeit("pairwise_python(X)", setup="import numpy as np;from __main__ import pairwise_python; X = np.random.random((1000, 3))",number=1))
    print(timeit.timeit("pairwise_numba(X)", setup="import numpy as np;from __main__ import pairwise_numba; X = np.random.random((1000, 3))"),number=1)

'''


#timeit(pairwise_numba(X))
