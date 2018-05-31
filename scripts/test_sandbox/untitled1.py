import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
'''

d_split = np.array_split(data,3)

d1 = spatial.distance.cdist(d_split[0][:],random[:])
d2 = spatial.distance.cdist(d_split[1][:],random[:])
d3 = spatial.distance.cdist(d_split[2][:],random[:])


d = np.concatenate( (np.concatenate(d1[:]),np.concatenate(d2[:]),np.concatenate(d3[:])) )

plt.figure()
plt.hist(d,bins=100)
plt.show()
'''
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size

for i in range(rank,33,size):
    print('[%i]'%(comm.rank),i)
    
