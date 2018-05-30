import numpy as np
from scipy import spatial
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
    
    d_divs = np.array_split(data,3)
    A=d_divs[0]
    B=d_divs[1]
    C=d_divs[2]
    #D=np.zeros((len(d_divs[3])))
    
    comm.Send(A,dest=1,tag=0)
    comm.Send(B,dest=2,tag=0)
    comm.Send(C,dest=3,tag=0)
    
    comm.Bcast(random)
    
else:
    data = np.empty((100,3))
    random = np.empty((100,3))
    d_divs = np.array_split(data,3)
    A=d_divs[0]
    B=d_divs[1]
    C=d_divs[2]
    d1 = np.empty(100)
    d2 = np.empty(100)
    d3 = np.empty(100)

if rank is 1:
    comm.Recv(A)
    d1 = spatial.distance.cdist(A,random,metric='euclidean')
    d1 = np.concatenate(d1[:])
    d1 = np.histogram(d1,bins=100,range=(0,1))
    comm.Send([d1[0],MPI.DOUBLE],dest=3)
    
if rank is 2:
    comm.Recv(B)
    d2 = spatial.distance.cdist(A,random,metric='euclidean')
    d2 = np.concatenate(d2[:])
    d2 = np.histogram(d2,bins=100,range=(0,1))
    #print(d2b)
    comm.Send([d2[0],MPI.DOUBLE],dest=3)
    
if rank is 3:
    comm.Recv(C)
    comm.Recv(d1)
    comm.Recv(d2)
    d3 = spatial.distance.cdist(A,random,metric='euclidean')
    d3 = np.concatenate(d3[:])
    d3 = np.histogram(d3,bins=100,range=(0,1))
    plt.figure()
    #plt.plot(d3)
    #plt.plot(d2)
    #plt.plot(d3)

plt.show()
