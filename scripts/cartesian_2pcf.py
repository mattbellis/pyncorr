import numpy as np
import pyncorr
import matplotlib.pylab as plt

import time 

# The range over which we would look for correlations
#hrange = 450
hrange = 200

# Number of bins to use when calculating the 2ptcf
nbins = 200


t0 = time.time()
print("Reading in some data....\n")

################################################################################
# Read in some data
################################################################################
data = pyncorr.read_in_columnar_data('../test_data/GRID_model_data.dat',cols_to_use=[0,1,2],convert=None)
random = pyncorr.read_in_columnar_data('../test_data/GRID_model_random.dat',cols_to_use=[0,1,2],convert=None)

################################################################################
# You probably don't want to read in any of the larger datasets (>10k) when 
# testing the code, just because it can take a while to run
################################################################################

#data = pyncorr.read_in_columnar_data('../test_data/GRID_model_data_LARGE_SAMPLE.dat',cols_to_use=[0,1,2],convert=None)
#random = pyncorr.read_in_columnar_data('../test_data/GRID_model_random_LARGE_SAMPLE.dat',cols_to_use=[0,1,2],convert=None)

# REAL DATA
#data = pyncorr.read_in_columnar_data('../test_data/sdss_data/10k_weighted_north_cmass.dat',cols_to_use=[0,1,2],convert='radecredz2xyz')
#random = pyncorr.read_in_columnar_data('../test_data/sdss_data/10k_weighted_random.dat',cols_to_use=[0,1,2],convert='radecredz2xyz')
#data = pyncorr.read_in_columnar_data('../test_data/sdss_data/100k_weighted_north_cmass.dat',cols_to_use=[0,1,2],convert='radecredz2xyz')
#random = pyncorr.read_in_columnar_data('../test_data/sdss_data/100k_weighted_random.dat',cols_to_use=[0,1,2],convert='radecredz2xyz')

print("Data is read in...")

nd = len(data[0])
nr = len(random[0])


plt.figure()
plt.plot(data[0],data[1],'.',markersize=1)

t1 = time.time()

# Note that the data/random should be transposed before passing it into the pyncorr functions
dr,edges = pyncorr.cartesian_distance(data.transpose(),random.transpose(),histrange=(0,hrange),nbins=nbins)
pyncorr.write_out_paircounts(dr,edges,nd,nr,filename='dr.dat',norm=nd*nr)
print("Finished with dr...")

t2 = time.time()

print()

dd,edges = pyncorr.cartesian_distance(data.transpose(),data.transpose(),histrange=(0,hrange),same_coords=True,nbins=nbins)
pyncorr.write_out_paircounts(dd,edges,nd,nd,filename='dd.dat',norm=(nd*nd-nd)/2.0)
print("Finished with dd...")

t3 = time.time()

rr,edges = pyncorr.cartesian_distance(random.transpose(),random.transpose(),histrange=(0,hrange),same_coords=True,nbins=nbins)
pyncorr.write_out_paircounts(rr,edges,nr,nr,filename='rr.dat',norm=(nr*nr-nr)/2.0)
print("Finished with rr...")

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
