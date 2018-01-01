import numpy as np
import pyncorr
import matplotlib.pylab as plt

import time 

nbins = 200

#nd = 1000
#nr = 1000
#x = np.random.random((nd,3))
#y = np.random.random((nr,3))

t0 = time.time()
print("Reading in some data....\n")

# Read in some data
data = np.loadtxt('../test_data/GRID_model_data.dat',unpack=True)
random = np.loadtxt('../test_data/GRID_model_random.dat',unpack=True)
#data = np.loadtxt('../test_data/GRID_model_data_LARGE_SAMPLE.dat',unpack=True)
#random = np.loadtxt('../test_data/GRID_model_random_LARGE_SAMPLE.dat',unpack=True)

nd = len(data[0])
nr = len(random[0])

#data = pyncorr.radeccmd2xyz(data[0],data[1],data[2])
#data = np.array(data)
data = data.transpose()

#random = pyncorr.radeccmd2xyz(random[0],random[1],random[2])
#random = np.array(random)
random = random.transpose()

#x = data
#y = random
#hrange = 450
hrange = 200

plt.figure()
plt.plot(data.transpose()[0],data.transpose()[1],',')

t1 = time.time()

d,edges = pyncorr.cartesian_distance(data,random,histrange=(0,hrange),nbins=nbins)
dr = d
pyncorr.write_out_paircounts(d,edges,nd,nr,filename='dr.dat',norm=nd*nr)

t2 = time.time()

print()

d,edges = pyncorr.cartesian_distance(data,data,histrange=(0,hrange),same_coords=True,nbins=nbins)
dd = d
pyncorr.write_out_paircounts(d,edges,nd,nd,filename='dd.dat',norm=(nd*nd-nd)/2.0)

t3 = time.time()

d,edges = pyncorr.cartesian_distance(random,random,histrange=(0,hrange),same_coords=True,nbins=nbins)
rr = d
pyncorr.write_out_paircounts(d,edges,nr,nr,filename='rr.dat',norm=(nr*nr-nr)/2.0)

t4 = time.time()

# Read in the data
dd_data = np.loadtxt('dd.dat',unpack=True)
dr_data = np.loadtxt('dr.dat',unpack=True)
rr_data = np.loadtxt('rr.dat',unpack=True)

# Pull out the bin centers from the first one.
x = dd_data[1][3:]
# Get the pair counts and normalizations
dd,ddnorm = dd_data[3][3:],dd_data[0][2]
dr,drnorm = dr_data[3][3:],dr_data[0][2]
rr,rrnorm = rr_data[3][3:],rr_data[0][2]

plt.figure()
plt.plot(x,dr,'o',label='dr')
plt.plot(x,dd,'o',label='dd')
plt.plot(x,rr,'o',label='rr')
plt.legend()

w = ((dd/ddnorm) - (2*dr/drnorm) + (rr/rrnorm))/(rr/rrnorm)

plt.figure()
plt.plot(x,w,'o',label='w')
plt.legend()

print("Time to read in and plot the data: %f sec" % (t1-t0))
print("Time to calc DR: %f sec" % (t2-t1))
print("Time to calc DD: %f sec" % (t3-t2))
print("Time to calc RR: %f sec" % (t4-t3))

plt.show()
