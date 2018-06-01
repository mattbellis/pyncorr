import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size

#seed = np.random.seed(5)
#data = np.random.random((1000,3))
#seed = np.random.seed(4)
#rand = np.random.random((1000,3))

data = np.loadtxt("../../test_data/GRID_model_data.dat")
rand = np.loadtxt("../../test_data/GRID_model_random.dat")

#print(data[0],rand[0])


ddiv = np.array_split(data,size)
rdiv = np.array_split(rand,size)

hist_dr = np.zeros(100)
hist_dd = np.zeros(100)
hist_rr = np.zeros(100)

t_i = MPI.Wtime()
for i in range(rank,4,size):
    #DD
    if rank is 0:
        t_dd_i=MPI.Wtime()
        dd = spatial.distance.pdist(data)
        h_dd = np.histogram(dd,bins=100)
        hist_dd += h_dd[0]
        t_dd_f=MPI.Wtime()-t_dd_i
    #RR
    if rank is 1:
        rr = spatial.distance.pdist(rand)
        h_rr = np.histogram(rr,bins=100)
        hist_rr += h_rr[0]
    #DR
    dr = spatial.distance.cdist(ddiv[i],rand)
    h_dr = np.histogram(dr,bins=100)
    hist_dr += h_dr[0]
    comm.Barrier()

hist_dr_f = np.zeros_like(hist_dr)
hist_rr_f = np.zeros_like(hist_rr)
hist_dd_f = np.zeros_like(hist_dd)

comm.Reduce([hist_dr,MPI.DOUBLE],[hist_dr_f,MPI.DOUBLE],root=0)
comm.Reduce([hist_rr,MPI.DOUBLE],[hist_rr_f,MPI.DOUBLE],root=0)
comm.Reduce([hist_dd,MPI.DOUBLE],[hist_dd_f,MPI.DOUBLE],root=0)
t_f = MPI.Wtime()-t_i
comm.Barrier()

if rank is 0:
    print("calculations took %.2f seconds"%(t_f))
    ddnorm = 4950000
    drnorm = 10000**2
    rrnorm = ddnorm
    w = ((hist_dd_f/ddnorm) - (2*hist_dr_f/drnorm) + (hist_rr_f/rrnorm))/(hist_rr_f/rrnorm)
    #w = ((hist_dd_f) - (2*hist_dr_f) + (hist_rr_f))/(hist_rr_f)
    #plt.figure()
    #plt.plot(w,marker='+')
    #plt.show()



    
    
    
