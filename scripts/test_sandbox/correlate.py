# this is a file where I am comparing data between raw pyncorr output and mpi output.
# nothing is working as it should be and I don't know why


import numpy as np
import matplotlib.pyplot as plt
import pyncorr

dd_data = np.loadtxt('dd_10k.dat',unpack=True)
dr_data = np.loadtxt('dr_10k.dat',unpack=True)
rr_data = np.loadtxt('rr_10k.dat',unpack=True)

# Pull out the bin centers from the first one.
x = dr_data[1][3:]
#print(dd_data[1][3:])
#print(dr_data[1][3:])
print(rr_data[1][3:]/4)

# Get the pair counts and normalizations
dd,ddnorm = dd_data[3][3:],dd_data[0][2]
dr,drnorm = dr_data[3][3:],dr_data[0][2]
rr,rrnorm = rr_data[3][3:],rr_data[0][2]

print(np.sum(dd))

#plt.figure()
#plt.plot(x,dr,'o',label='dr')
#plt.plot(x,dd,'o',label='dd')
#plt.plot(x,rr,'o',label='rr')
#plt.legend()

w = ((dd/ddnorm) - (2*dr/drnorm) + (rr/rrnorm))/(rr/rrnorm)
#w = ((dd) - (2*dr) + (rr))/(rr)

plt.figure()
plt.plot(x,w,'o',label='w')

fstr = "10k"

test_d = pyncorr.read_in_columnar_data('../../../cmass/%s_weighted_random.dat'%(fstr),convert='radecredz2xyz')
test_r = pyncorr.read_in_columnar_data('../../../cmass/%s_weighted_random.dat'%(fstr),convert='radecredz2xyz')

test_d = test_d.transpose()
test_r = test_r.transpose()

hist1,edges1 = pyncorr.cartesian_distance(test_d,test_d,histrange=(0,3000),same_coords=True,nbins=100)
hist2,edges2 = pyncorr.cartesian_distance(test_d,test_r,histrange=(0,3000),nbins=100)
hist3,edges3 = pyncorr.cartesian_distance(test_r,test_r,histrange=(0,3000),same_coords=True,nbins=100)

dd=hist1
dr=hist2
rr=hist3

w2 = ((dd/ddnorm) - (2*dr/drnorm) + (rr/rrnorm))/(rr/rrnorm)

plt.plot(x,w2,'o')
plt.legend()
plt.show()

