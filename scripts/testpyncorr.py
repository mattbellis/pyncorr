import numpy as np
import pyncorr
import matplotlib.pylab as plt

nbins = 200

#nd = 1000
#nr = 1000
#x = np.random.random((nd,3))
#y = np.random.random((nr,3))

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

x = data
y = random
hrange = 450

plt.figure()
plt.plot(x.transpose()[0],x.transpose()[1],',')


d,edges = pyncorr.cartesian_distance(x,y,histrange=(0,hrange),nbins=nbins)
dr = d
pyncorr.write_out_paircounts(d,edges,nd,nr,filename='dr.dat',norm=nd*nr)

print()

d,edges = pyncorr.cartesian_distance(x,x,histrange=(0,hrange),same_coords=True,nbins=nbins)
dd = d
pyncorr.write_out_paircounts(d,edges,nd,nd,filename='dd.dat',norm=(nd*nd-nd)/2.0)

d,edges = pyncorr.cartesian_distance(y,y,histrange=(0,hrange),same_coords=True,nbins=nbins)
rr = d
pyncorr.write_out_paircounts(d,edges,nr,nr,filename='rr.dat',norm=(nr*nr-nr)/2.0)


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
