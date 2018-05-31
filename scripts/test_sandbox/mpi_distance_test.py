import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size

seed = np.random.seed(5)
data = np.random.random((1000,3))
seed = np.random.seed(4)
rand = np.random.random((1000,3))
ddiv = np.array_split(data,size)

hist = np.zeros((100))
#print(len(hist))

for i in range(rank,4,size):
   d = spatial.distance.cdist(ddiv[i],rand)
   h = np.histogram(d,bins=100)
   hist += h[0]

hist_f = np.zeros_like(hist)

comm.Reduce([hist,MPI.DOUBLE],[hist_f,MPI.DOUBLE],root=0)

comm.Barrier()

if rank is 0:
    plt.figure()
    plt.plot(hist_f)
    plt.show()





    
    
    
