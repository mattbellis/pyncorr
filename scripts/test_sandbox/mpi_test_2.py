import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
cores= comm.Get_size()
data=np.linspace(0,10,10)
dsplit = np.array_split(data,cores-1)

s1=np.zeros(1)
s2=np.zeros(1)
s3=np.zeros(1)

if rank is 0:
    s1 = np.sum(dsplit[rank])
    comm.send(s1,dest=3)
if rank is 1:
    s2 = np.sum(dsplit[rank])
    comm.send(s2,dest=3)
if rank is 2:
    s3 = np.sum(dsplit[rank])
    comm.send(s3,dest=3)
if rank is 3:
    s1=comm.recv(None,source=0)
    s2=comm.recv(None,source=1)
    s3=comm.recv(None,source=2)
    f=np.sum((s1,s2,s3))
    print(f)