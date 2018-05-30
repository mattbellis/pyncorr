import numpy as np
from mpi4py import MPI
import matplotlib.pylab as plt

comm = MPI.COMM_WORLD
rank = comm.rank

def pprint(string="", end="\n", comm=MPI.COMM_WORLD):
    """Print for MPI parallel programs: Only rank 0 prints *str*."""
    if comm.rank == 0:
        print(string) 
#########################################
# Example Code
#########################################
'''
my_N = 4
N = my_N * comm.size

if comm.rank == 0:
    A = np.arange(N, dtype=np.float64)
else:
    A = np.empty(N, dtype=np.float64)

my_A = np.empty(my_N, dtype=np.float64)

# Scatter data into my_A arrays
comm.Scatter( [A, MPI.DOUBLE], [my_A, MPI.DOUBLE] )

for r in range(comm.size):
    if comm.rank == r:
        print("[%d] %s" % (comm.rank, my_A))
    comm.Barrier()

# Everybody is multiplying by 2
my_A *= 2

# Allgather data into A again
comm.Allgather( [my_A, MPI.DOUBLE], [A, MPI.DOUBLE] )

for r in range(comm.size):
    if comm.rank == r:
        print("[%d] %s" % (comm.rank, A))
    comm.Barrier()

'''
#########################################


if rank is 0:
    data = np.arange(20,dtype=np.float64)
    ddiv = np.array_split(data,4)
else:
    data = np.empty(20,dtype=np.float64)
    ddiv = np.array_split(data,4)
    
d_s = np.empty((5),dtype=np.float64)
comm.Scatter([np.array(ddiv),MPI.DOUBLE],[d_s,MPI.DOUBLE])

d_s *=2

comm.Allgather([d_s,MPI.DOUBLE],[data,MPI.DOUBLE])

comm.Barrier()

pprint(data)