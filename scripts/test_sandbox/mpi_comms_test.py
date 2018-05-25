import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
cores= comm.Get_size()

comm.Barrier()

N = 10
divs=3
if comm.rank == 0:
    A = np.arange(N, dtype=np.float64)
    print(A)
    Adiv=np.array_split(A,divs)
    B = np.zeros(N)
    C = np.zeros(N)
    D = np.zeros(N)
    #print(B,Adiv[0])
    B[0:len(Adiv[0])] += Adiv[0]
    C[0:len(Adiv[1])] += Adiv[1]
    D[0:len(Adiv[2])] += Adiv[2]
    
    comm.Send([B,MPI.DOUBLE],dest=1)
    comm.Send([C,MPI.DOUBLE],dest=2)
    comm.Send([D,MPI.DOUBLE],dest=3)
    
else:
    B = np.empty(N, dtype=np.float64)     
    C = np.empty(N, dtype=np.float64)
    D = np.empty(N, dtype=np.float64)
    s1 = np.empty(1)
    s2 = np.empty(1)
    s3 = np.empty(1)

if rank is 1:
    comm.Recv(B)
    s1 = np.sum(B)
    print(s1)
    comm.Send([s1,MPI.FLOAT],dest=3)
    
if rank is 2:
    comm.Recv(C)
    s2 = np.sum(C)
    print(s2)
    comm.Send([s2,MPI.FLOAT],dest=3)

if rank is 3:
    comm.Recv(D)
    comm.Recv(s1)
    comm.Recv(s2)
    s3 = np.sum(D)
    print(s3)
    s_f = np.sum((s1,s2,s3))
    print(s_f)

