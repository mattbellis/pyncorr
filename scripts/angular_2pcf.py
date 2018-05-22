import numpy as np
import pyncorr
import matplotlib.pylab as plt

import time 

nbins = 50

t0 = time.time()
print("Reading in some data....\n")

# Read in some data
data = np.loadtxt('../test_data/GRID_model_data.dat',unpack=True)
random = np.loadtxt('../test_data/GRID_model_random.dat',unpack=True)

#data = np.loadtxt('../test_data/GRID_model_data_LARGE_SAMPLE.dat',unpack=True)
#random = np.loadtxt('../test_data/GRID_model_random_LARGE_SAMPLE.dat',unpack=True)

# REAL DATA
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=70, Om0=0.3)

ra,dec,cmd = data[0], data[1], data[2]
radata = ra.copy()
decdata = dec.copy()
data = np.array([radata,decdata])

ra,dec,cmd = random[0], random[1], random[2]
random = np.array([ra,dec])

#from mpl_toolkits.mplot3d import Axes3D
#fig = plt.figure()
##ax = fig.add_subplot(111, projection='3d')
###plt.plot(ra,dec,cmd,'.',markersize=0.5,alpha=0.2)
#plt.plot(radata,decdata,'.',markersize=0.5,alpha=0.2)
##plt.plot(data[0],data[1],data[2],'.',markersize=0.5,alpha=0.2)
#plt.show()
#exit()

#############

nd = len(data[0])
nr = len(random[0])

################ DR ##################################################
t1 = time.time()

d = np.zeros(nbins,dtype=int)

hist_temp,edges = pyncorr.angular_distance(data_temp,random_temp,histrange=(0,hrange),nbins=nbins)
d += hist_temp
dr = d

pyncorr.write_out_paircounts(d,edges,nd,nr,filename='dr.dat',norm=nd*nr)
print("tot: ",tot)

exit()

################################################################################
t4 = time.time()

print("Time to read in and plot the data: %f sec" % (t1-t0))
print("Time to calc DR: %f sec" % (t2-t1))
print("Time to calc DD: %f sec" % (t3-t2))
print("Time to calc RR: %f sec" % (t4-t3))

print()
print("Num calcs DR: %d" % tot_calc_dr)
print("Num calcs DD: %d" % tot_calc_dd)
print("Num calcs RR: %d" % tot_calc_rr)

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

plt.show()
