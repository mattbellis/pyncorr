import numpy as np
import pyncorr
import matplotlib.pylab as plt

import time 

# The range over which we would look for correlations
#hrange = 450
hrange = 200

# Number of bins to use when calculating the 2ptcf
nbins = 50


t0 = time.time()
print("Reading in some data....\n")

################################################################################
# Read in some data
################################################################################
data = pyncorr.read_in_columnar_data('../test_data/GRID_model_data_100gals.dat',cols_to_use=[0,1,2],convert=None)
random = pyncorr.read_in_columnar_data('../test_data/GRID_model_random_100gals.dat',cols_to_use=[0,1,2],convert=None)

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

print(nd,nr)

#plt.figure()
#plt.plot(data[0],data[1],'.',markersize=1)

t1 = time.time()

# Note that the data/random should be transposed before passing it into the pyncorr functions
ddd,edges = pyncorr.three_point_correlation_function(data.transpose(),data.transpose(), data.transpose(),histrange=[(0,500),(1,3),(0,1)],nbins=(nbins,nbins,nbins),triplet_to_calculate="DDD")
pyncorr.write_out_tripletcounts(ddd,edges,nd,nd,nd,filename='ddd.dat',norm=nd*(nd-1)*(nd-2)/6.)
print("Finished with ddd...")

t2 = time.time()
print()

ddr,edges = pyncorr.three_point_correlation_function(data.transpose(),data.transpose(), random.transpose(),histrange=[(0,500),(1,3),(0,1)],nbins=(nbins,nbins,nbins),triplet_to_calculate="DDR")
pyncorr.write_out_tripletcounts(ddr,edges,nd,nd,nr,filename='ddr.dat',norm=nd*(nd-1)*nr/2.)
print("Finished with ddr...")

t3 = time.time()
print()

drr,edges = pyncorr.three_point_correlation_function(data.transpose(),random.transpose(), random.transpose(),histrange=[(0,500),(1,3),(0,1)],nbins=(nbins,nbins,nbins),triplet_to_calculate="DRR")
pyncorr.write_out_tripletcounts(drr,edges,nd,nd,nr,filename='drr.dat',norm=nd*nr*(nr-1)/2.)
print("Finished with drr...")

t4 = time.time()
print()

rrr,edges = pyncorr.three_point_correlation_function(random.transpose(),random.transpose(), random.transpose(),histrange=[(0,500),(1,3),(0,1)],nbins=(nbins,nbins,nbins),triplet_to_calculate="RRR")
pyncorr.write_out_tripletcounts(rrr,edges,nd,nd,nr,filename='rrr.dat',norm=nr*(nr-1)*(nr-2)/6.)
print("Finished with rrr...")

t5 = time.time()
print()


'''
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
'''

print("Time to read in and plot the data: %f sec" % (t1-t0))
print("Time to calc DDD: %f sec" % (t2-t1))
print("Time to calc DDR: %f sec" % (t3-t2))
print("Time to calc DRR: %f sec" % (t4-t3))
print("Time to calc RRR: %f sec" % (t5-t4))

#plt.show()
