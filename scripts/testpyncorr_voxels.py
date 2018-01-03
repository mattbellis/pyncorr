import numpy as np
import pyncorr
import matplotlib.pylab as plt

import time 

nbins = 200

t0 = time.time()
print("Reading in some data....\n")

# Read in some data
data = np.loadtxt('../test_data/GRID_model_data.dat',unpack=True)
random = np.loadtxt('../test_data/GRID_model_random.dat',unpack=True)
#data = np.loadtxt('../test_data/GRID_model_data_LARGE_SAMPLE.dat',unpack=True)
#random = np.loadtxt('../test_data/GRID_model_random_LARGE_SAMPLE.dat',unpack=True)

nd = len(data[0])
nr = len(random[0])

################################################################################
# Do the voxelizing
voxel_widths = [150,150,350]

###########################################################
#x,y,z = pyncorr.radeccmd2xyz(data[0], data[1], data[2])
#data = np.array([x,y,z])

loedges = [np.min(data[0]), np.min(data[1]), np.min(data[2])]
hiedges = [np.max(data[0]), np.max(data[1]), np.max(data[2])]

print(loedges)
print(hiedges)

nvoxels_data = pyncorr.define_boundaries(loedges, hiedges, voxel_widths)
print(nvoxels_data)
vcoords_data = pyncorr.divide_into_voxels(data, loedges, hiedges, voxel_widths, nvoxels_data)
print(vcoords_data)
print(vcoords_data[0][vcoords_data[0]!=0])
print(vcoords_data[1][vcoords_data[1]!=0])
print(vcoords_data[2][vcoords_data[2]!=0])


###########################################################
#x,y,z = pyncorr.radeccmd2xyz(random[0], random[1], random[2])
#random = np.array([x,y,z])

loedges = [np.min(random[0]), np.min(random[1]), np.min(random[2])]
hiedges = [np.max(random[0]), np.max(random[1]), np.max(random[2])]

print(loedges)
print(hiedges)

nvoxels_random = pyncorr.define_boundaries(loedges, hiedges, voxel_widths)
print(nvoxels_random)
vcoords_random = pyncorr.divide_into_voxels(random, loedges, hiedges, voxel_widths, nvoxels_random)
print(vcoords_random)
print(vcoords_random[0][vcoords_random[0]!=0])
print(vcoords_random[1][vcoords_random[1]!=0])
print(vcoords_random[2][vcoords_random[2]!=0])

#exit()

################################################################################
data = data.transpose()
random = random.transpose()

#hrange = 450
hrange = 200

plt.figure()
plt.plot(data.transpose()[0],data.transpose()[1],',')


################ DR ##################################################
t1 = time.time()

d = np.zeros(nbins,dtype=int)

tot = 0
for i in range(nvoxels_data[0]):
    for j in range(nvoxels_data[1]):
        for k in range(nvoxels_data[2]):
            index = vcoords_data[0]==i
            index *= vcoords_data[1]==j
            index *= vcoords_data[2]==k
            data_temp = data[index]
            tot += len(data_temp)

            for ii in range(i-1,i+2):
                for jj in range(j-1,j+2):
                    for kk in range(k-1,k+2):
                        if ii<nvoxels_random[0] and jj<nvoxels_random[1] and kk<nvoxels_random[2] and ii>=0 and jj>=0 and kk>=0:
                            print(i,j,k,ii,jj,kk)
                            index = vcoords_random[0]==ii
                            index *= vcoords_random[1]==jj
                            index *= vcoords_random[2]==kk
                            random_temp = random[index]

                            if len(data_temp)>0 and len(random_temp)>0:
                                print("N galaxies: ",len(data_temp),len(random_temp))
                                hist_temp,edges = pyncorr.cartesian_distance(data_temp,random_temp,histrange=(0,hrange),nbins=nbins)
                                d += hist_temp
dr = d
pyncorr.write_out_paircounts(d,edges,nd,nr,filename='dr.dat',norm=nd*nr)
print("tot: ",tot)
#exit()

################ DD ##################################################
t2 = time.time()

d = np.zeros(nbins,dtype=int)

tot = 0
list_of_combos = []
for i in range(nvoxels_data[0]):
    for j in range(nvoxels_data[1]):
        for k in range(nvoxels_data[2]):
            index = vcoords_data[0]==i
            index *= vcoords_data[1]==j
            index *= vcoords_data[2]==k
            data_temp = data[index]
            tot += len(data_temp)

            for ii in range(i,i+2):
                for jj in range(j-1,j+2):
                    for kk in range(k-1,k+2):
                        vindex = "%03s%03s%03s%03s%03s%03s" % (i,j,k,ii,jj,kk)
                        if vindex not in list_of_combos:
                            list_of_combos.append(vindex)
                        if ii<nvoxels_data[0] and jj<nvoxels_data[1] and kk<nvoxels_data[2] and ii>=0 and jj>=0 and kk>=0:
                            print(i,j,k,ii,jj,kk)
                            index = vcoords_data[0]==ii
                            index *= vcoords_data[1]==jj
                            index *= vcoords_data[2]==kk
                            data_temp2 = data[index]

                            if len(data_temp)>0 and len(data_temp2)>0:
                                print("N galaxies: ",len(data_temp),len(data_temp2))
                                if i==ii and j==jj and k==kk:
                                    hist_temp,edges = pyncorr.cartesian_distance(data_temp,data_temp2,histrange=(0,hrange),nbins=nbins, same_coords=True)
                                else:
                                    hist_temp,edges = pyncorr.cartesian_distance(data_temp,data_temp2,histrange=(0,hrange),nbins=nbins)
                                d += hist_temp
dd = d
pyncorr.write_out_paircounts(d,edges,nd,nd,filename='dd.dat',norm=(nd*nd-nd)/2.0)
print("tot: ",tot)
#exit()

################ DR ##################################################
t3 = time.time()

d = np.zeros(nbins,dtype=int)

for i in range(nvoxels_random[0]):
    for j in range(nvoxels_random[1]):
        for k in range(nvoxels_random[2]):
            index = vcoords_random[0]==i
            index *= vcoords_random[1]==j
            index *= vcoords_random[2]==k
            random_temp = random[index]

            for ii in range(i,i+2):
                for jj in range(j,j+2):
                    for kk in range(k,k+2):
                        if ii<nvoxels_random[0] and jj<nvoxels_random[1] and kk<nvoxels_random[2]:
                            index = vcoords_random[0]==ii
                            index *= vcoords_random[1]==jj
                            index *= vcoords_random[2]==kk
                            random_temp2 = random[index]

                            if len(random_temp)>0 and len(random_temp2)>0:
                                print("N galaxies: ",len(random_temp),len(random_temp2))
                                if i==ii and j==jj and k==kk:
                                    hist_temp,edges = pyncorr.cartesian_distance(random_temp,random_temp2,histrange=(0,hrange),nbins=nbins, same_coords=True)
                                else:
                                    hist_temp,edges = pyncorr.cartesian_distance(random_temp,random_temp2,histrange=(0,hrange),nbins=nbins)
                                d += hist_temp
dd = d
pyncorr.write_out_paircounts(d,edges,nr,nr,filename='rr.dat',norm=(nr*nr-nr)/2.0)

#exit()
#exit()


################################################################################
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
