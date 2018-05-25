import numpy as np
import scipy
import matplotlib.pylab as plt
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank

divs = 4

if rank is 0:
    seed = np.random.seed(seed=5)
    data = np.random.random((100,3))
    seed = np.random.seed(seed=10)
    random = np.random.random((100,3))
    
    d_divs = np.array_split(data,4)
    A=np.zeros(())
    
    
