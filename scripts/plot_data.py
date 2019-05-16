import numpy as np
import pyncorr
import matplotlib.pylab as plt

import time

#from astropy.cosmology import FlatLambdaCDM
#cosmo = FlatLambdaCDM(H0=70, Om0=0.3)

nbins = 50

t0 = time.time()
print("Reading in some data....\n")

# Read in some data
data = pyncorr.read_in_columnar_data('../test_data/GRID_model_data.dat',cols_to_use=[0,1,2],convert=None)
random = pyncorr.read_in_columnar_data('../test_data/GRID_model_random.dat',cols_to_use=[0,1,2],convert=None)

#data = pyncorr.read_in_columnar_data('../test_data/GRID_model_data_LARGE_SAMPLE.dat',cols_to_use=[0,1,2],convert=None)
#random = pyncorr.read_in_columnar_data('../test_data/GRID_model_random_LARGE_SAMPLE.dat',cols_to_use=[0,1,2],convert=None)

# REAL DATA
#data = pyncorr.read_in_columnar_data('../../cmass/samples/10k_weighted_nortest_data/sdss_datae=[0,1,2],convert='radecredz2xyz')
#random = pyncorr.read_in_columnar_data('../../cmass/samples/10k_weighted_random.dat',cols_to_use=[0,1,2],convert='radecredz2xyz')
#data = pyncorr.read_in_columnar_data('../../cmass/samples/100k_weighted_nortest_data/sdss_datae=[0,1,2],convert='radecredz2xyz')
#random = pyncorr.read_in_columnar_data('../../cmass/samples/100k_weighted_random.dat',cols_to_use=[0,1,2],convert='radecredz2xyz')

# Do this just to plot RA vs DEC
#data = pyncorr.read_in_columnar_data('../test_data/sdss_data/100k_weighted_north_cmass.dat',cols_to_use=[0,1,2],convert=None)
#random = pyncorr.read_in_columnar_data('../test_data/sdss_data/100k_weighted_random.dat',cols_to_use=[0,1,2],convert=None)


t1 = time.time()
print("Time to read in the data: {0:f} sec".format(t1-t0))



# 2D plots
plt.figure(figsize=(10,7))

plt.subplot(2,3,1)
plt.plot(data[0],data[1],'.',markersize=0.5,alpha=0.2)
plt.xlabel('RA (degrees)',fontsize=14)
plt.ylabel('DEC (degrees)',fontsize=14)

plt.subplot(2,3,2)
plt.plot(data[0],data[2],'.',markersize=0.5,alpha=0.2)
plt.xlabel('RA (degrees)',fontsize=14)
plt.ylabel('CMD (Mpc)',fontsize=14)

plt.subplot(2,3,3)
plt.plot(data[1],data[2],'.',markersize=0.5,alpha=0.2)
plt.xlabel('DEC (degrees)',fontsize=14)
plt.ylabel('CMD (Mpc)',fontsize=14)


plt.subplot(2,3,4)
plt.plot(random[0],random[1],'.',markersize=0.5,alpha=0.2)
plt.xlabel('RA (degrees)',fontsize=14)
plt.ylabel('DEC (degrees)',fontsize=14)

plt.subplot(2,3,5)
plt.plot(random[0],random[2],'.',markersize=0.5,alpha=0.2)
plt.xlabel('RA (degrees)',fontsize=14)
plt.ylabel('CMD (Mpc)',fontsize=14)

plt.subplot(2,3,6)
plt.plot(random[1],random[2],'.',markersize=0.5,alpha=0.2)
plt.xlabel('DEC (degrees)',fontsize=14)
plt.ylabel('CMD (Mpc)',fontsize=14)

plt.tight_layout()



# 3D plots
'''
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
###plt.plot(ra,dec,cmd,'.',markersize=0.5,alpha=0.2)
#plt.plot(data[0],data[1],'.',markersize=0.5,alpha=0.2)
ax.plot(data[0],data[1],data[2],'.',markersize=0.5,alpha=0.2)
'''
plt.show()


