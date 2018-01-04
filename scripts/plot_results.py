import numpy as np
import pyncorr
import matplotlib.pylab as plt

import time 

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

fig = plt.figure()
#plt.subplot(1,1,1)
plt.plot(x,w,'o',label='w',markersize=10)
plt.xlabel(r'Comoving separation $r$ ($h^{-1}$ Mpc)',fontsize=18)
plt.ylabel(r'$\zeta$',fontsize=18)
plt.xlim(20,160)
plt.ylim(0,0.04)
plt.tight_layout()

left, bottom, width, height = [0.6, 0.6, 0.35, 0.35]
ax2 = fig.add_axes([left, bottom, width, height])
#a = plt.subplot(2,2,2)
plt.plot(x,x*x*w,'o',label='w',markersize=5)
plt.xlabel(r'Comoving separation $r$ ($h^{-1}$ Mpc)',fontsize=10)
plt.ylabel(r'$r^2 \zeta$',fontsize=12)
plt.xlim(20,160)
#plt.ylim(0,0.04)




plt.savefig('2pt_correlation_function.png')


plt.show()
