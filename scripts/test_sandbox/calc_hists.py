# this is what I am using to generate the mpi datasets
# i have debugged to the best of my ability but i simply do not have enough time left here today to finish

import numpy as np
#import matplotlib.pyplot as plt
#from scipy.spatial import distance
import pyncorr
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size

fstr = "10k" # this string is for what size dataset you're using, to make things a little easier when scaling up

data = pyncorr.read_in_columnar_data('../../../cmass/%s_weighted_random.dat'%(fstr),convert='radecredz2xyz')
rand = pyncorr.read_in_columnar_data('../../../cmass/%s_weighted_random.dat'%(fstr),convert='radecredz2xyz')

data = data.transpose() # my loop doesn't play nice with the raw output from read_in_columnar_data, so we transpose
rand = rand.transpose()

def dd_or_rr(dataset,histrange,bins=100):

    #calculate distances between points within an individual dataset, used for dd or rr
    
    ddiv = np.array_split(dataset,size)
    
    for i in range(rank,size,size):
        idx0 = ddiv[i]
        #self counts
        hist,edges = pyncorr.cartesian_distance(idx0,idx0,histrange=histrange,same_coords=True)
        if i is not size-1:    
            idx1 = np.concatenate(ddiv[i+1:])
            hist,edges = pyncorr.cartesian_distance(idx0,idx1,histrange=histrange)

    comm.Barrier()
    # it turns out that when you use comm.reduce it requires an operation and by default that is a sum.
    # so, i've switched to using gather which seems to work similarly.
    hist_f = comm.gather(hist,root=0) # this outputs a list of the histogrammed values from each process [array(ouput1),array(output2), ... ,etc.]
    edges_f = comm.gather(edges,root=0) # all the edges are the same
    
    if rank is 0:
        print(hist_f,np.sum(hist_f),len(hist_f))
        hist_f = np.sum(hist_f,axis=0) # sum the arrays along axis zero to preserve binning
        return hist_f,edges_f[0] # only return the zeroth value of edges bc they're all the same so who cares

def dr(dset_d,dset_r,histrange,bins=100):
    
    # calculate distances between points in two separate datasets, used for rr

    ddiv = np.array_split(dset_d,size)

    for i in range(rank,size,size):
        hist,edges = pyncorr.cartesian_distance(ddiv[i],dset_r,histrange=histrange,nbins=bins)

    comm.Barrier()
    hist_f = comm.gather(hist,root=0)
    edges_f = comm.gather(edges,root=0)
    
    if rank is 0:
        hist_f = np.sum(hist_f,axis=0)
        return hist_f,edges_f[0]

#t1 = MPI.Wtime()
dd = dd_or_rr(data,(0,1500))
#t2 = MPI.Wtime()
dr = dr(data,rand,(0,1500))
#t3 = MPI.Wtime()
rr = dd_or_rr(rand,(0,1500))
#t4 = MPI.Wtime()

if rank is 0:
    print(dr[0])
    print(dr[1])
    #print('Done! Took %.2f seconds for all calculations.'%(t4-t1))
    #print('DD: %.2f seconds'%(t2-t1))
    #print('DR: %.2f seconds'%(t3-t2))
    #print('RR: %.2f seconds'%(t4-t3))
    nd = len(data)
    nr = len(rand)
    pyncorr.write_out_paircounts(dd[0],dd[1],nd,nd,filename='dd_%s.dat'%(fstr),norm=((nd*nd-nd)/2))
    pyncorr.write_out_paircounts(dr[0],dr[1],nd,nr,filename='dr_%s.dat'%(fstr),norm=(nd*nr))
    pyncorr.write_out_paircounts(rr[0],rr[1],nr,nr,filename='rr_%s.dat'%(fstr),norm=((nr*nr-nr)/2))
    print('written')




