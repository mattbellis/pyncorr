import numpy as np
import pyncorr
import matplotlib.pylab as plt

import time 

from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=70, Om0=0.3)

nbins = 50

t0 = time.time()
print("Reading in some data....\n")

# Read in some data
#data = pyncorr.read_in_columnar_data('../test_data/GRID_model_data.dat',cols_to_use=[0,1,2],convert=None)
#random = pyncorr.read_in_columnar_data('../test_data/GRID_model_random.dat',cols_to_use=[0,1,2],convert=None)

#data = pyncorr.read_in_columnar_data('../test_data/GRID_model_data_LARGE_SAMPLE.dat',cols_to_use=[0,1,2],convert=None)
#random = pyncorr.read_in_columnar_data('../test_data/GRID_model_random_LARGE_SAMPLE.dat',cols_to_use=[0,1,2],convert=None)

# REAL DATA
#data = pyncorr.read_in_columnar_data('../../cmass/samples/10k_weighted_north_cmass.dat',cols_to_use=[0,1,2],convert='radecredz2xyz')
#random = pyncorr.read_in_columnar_data('../../cmass/samples/10k_weighted_random.dat',cols_to_use=[0,1,2],convert='radecredz2xyz')
data = pyncorr.read_in_columnar_data('../../cmass/samples/100k_weighted_north_cmass.dat',cols_to_use=[0,1,2],convert='radecredz2xyz')
random = pyncorr.read_in_columnar_data('../../cmass/samples/100k_weighted_random.dat',cols_to_use=[0,1,2],convert='radecredz2xyz')

# Do this just to plot RA vs DEC
#data = pyncorr.read_in_columnar_data('../../cmass/samples/100k_weighted_north_cmass.dat',cols_to_use=[0,1,2],convert=None)
#random = pyncorr.read_in_columnar_data('../../cmass/samples/100k_weighted_random.dat',cols_to_use=[0,1,2],convert=None)

#data = np.loadtxt('../../cmass/samples/100k_weighted_north_cmass.dat',unpack=True)
#random = np.loadtxt('../../cmass/samples/100k_weighted_random.dat',unpack=True)
#data = np.loadtxt('../../cmass/samples/500k_weighted_north_cmass.dat',unpack=True)
#random = np.loadtxt('../../cmass/samples/1mil_weighted_random.dat',unpack=True)


#from mpl_toolkits.mplot3d import Axes3D
#fig = plt.figure()
##ax = fig.add_subplot(111, projection='3d')
###plt.plot(ra,dec,cmd,'.',markersize=0.5,alpha=0.2)
#plt.plot(data[0],data[1],'.',markersize=0.5,alpha=0.2)
#plt.plot(data[0],data[1],data[2],'.',markersize=0.5,alpha=0.2)
#plt.show()
#exit()

#############

nd = len(data[0])
nr = len(random[0])

################################################################################
# Do the voxelizing
#voxel_widths = [100,100,100]
#voxel_widths = [300,300,700]
#voxel_widths = [7100,7100,7100]
voxel_widths = [200,200,200]
hrange=200 # The range over which we will plot the correlation functions

###########################################################
voxels_data, dim_data = pyncorr.return_voxelized_data(data,voxel_widths,verbose=True)
nvoxels_data = dim_data["nvoxels"]

voxels_random, dim_random = pyncorr.return_voxelized_data(random,voxel_widths,verbose=True)
nvoxels_random = dim_random["nvoxels"]
################################################################################


################ DR ##################################################
t1 = time.time()

d = np.zeros(nbins,dtype=int)

tot = 0
tot_calc_dr = 0
for i in range(nvoxels_data[0]):
    for j in range(nvoxels_data[1]):
        for k in range(nvoxels_data[2]):
            data_temp = voxels_data[i][j][k]
            if data_temp is not None:
                print(i,j,k)
                tot += len(data_temp)

                for ii in range(i-1,i+2):
                    for jj in range(j-1,j+2):
                        for kk in range(k-1,k+2):
                            if ii<nvoxels_random[0] and jj<nvoxels_random[1] and kk<nvoxels_random[2] and ii>=0 and jj>=0 and kk>=0:
                                #print(i,j,k,ii,jj,kk)
                                random_temp = voxels_random[ii][jj][kk]

                                if data_temp is not None and random_temp is not None:
                                    print("DR %d(%d) %d(%d) %d(%d) N galaxies: %d %d"% (i,nvoxels_data[0],j,nvoxels_data[1],k,nvoxels_data[2],len(data_temp),len(random_temp)))
                                    tot_calc_dr += len(data_temp)*len(random_temp)
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
tot_calc_dd = 0
list_of_combos = []
list_of_combos_reversed = []
for i in range(nvoxels_data[0]):
    for j in range(nvoxels_data[1]):
        for k in range(nvoxels_data[2]):
            data_temp = voxels_data[i][j][k]
            if data_temp is not None:
                print(i,j,k)
                tot += len(data_temp)

                for ii in range(i-1,i+2):
                    for jj in range(j-1,j+2):
                        for kk in range(k-1,k+2):

                            # Do this to make sure we don't double count
                            vindex = "%03s%03s%03s%03s%03s%03s" % (i,j,k,ii,jj,kk)
                            vindex_reversed = "%03s%03s%03s%03s%03s%03s" % (ii,jj,kk,i,j,k)
                            do_calc = True
                            if vindex not in list_of_combos_reversed:
                                do_calc = True
                            else:
                                do_calc = False

                            # Do this part only after we've checked everything else. 
                            list_of_combos_reversed.append(vindex_reversed)

                            if do_calc and ii<nvoxels_data[0] and jj<nvoxels_data[1] and kk<nvoxels_data[2] and ii>=0 and jj>=0 and kk>=0:
                                #print(i,j,k,ii,jj,kk)
                                data_temp2 = voxels_data[ii][jj][kk]

                                if data_temp is not None and data_temp2 is not None:
                                    print("DD N galaxies: ",len(data_temp),len(data_temp2))
                                    if i==ii and j==jj and k==kk:
                                        tot_calc_dd += (len(data_temp)*len(data_temp2) - len(data_temp2))/2
                                        hist_temp,edges = pyncorr.cartesian_distance(data_temp,data_temp2,histrange=(0,hrange),nbins=nbins, same_coords=True)
                                    else:
                                        tot_calc_dd += (len(data_temp)*len(data_temp2))
                                        hist_temp,edges = pyncorr.cartesian_distance(data_temp,data_temp2,histrange=(0,hrange),nbins=nbins)
                                    d += hist_temp
dd = d
pyncorr.write_out_paircounts(d,edges,nd,nd,filename='dd.dat',norm=(nd*nd-nd)/2.0)
print("tot: ",tot)
#exit()

################ DR ##################################################
t3 = time.time()

d = np.zeros(nbins,dtype=int)

list_of_combos = []
list_of_combos_reversed = []
tot_calc_rr = 0
for i in range(nvoxels_random[0]):
    for j in range(nvoxels_random[1]):
        for k in range(nvoxels_random[2]):
            random_temp = voxels_random[i][j][k]
            if random_temp is not None:
                print(i,j,k)

                for ii in range(i-1,i+2):
                    for jj in range(j-1,j+2):
                        for kk in range(k-1,k+2):
                            if ii<nvoxels_random[0] and jj<nvoxels_random[1] and kk<nvoxels_random[2]:
                                random_temp2 = voxels_random[ii][jj][kk]

                                # Do this to make sure we don't double count
                                vindex = "%03s%03s%03s%03s%03s%03s" % (i,j,k,ii,jj,kk)
                                vindex_reversed = "%03s%03s%03s%03s%03s%03s" % (ii,jj,kk,i,j,k)
                                do_calc = True
                                if vindex not in list_of_combos_reversed:
                                    do_calc = True
                                else:
                                    do_calc = False

                                # Do this part only after we've checked everything else. 
                                list_of_combos_reversed.append(vindex_reversed)

                                if do_calc and ii<nvoxels_random[0] and jj<nvoxels_random[1] and kk<nvoxels_random[2] and ii>=0 and jj>=0 and kk>=0:
                                    #print(i,j,k,ii,jj,kk)
                                    if random_temp is not None and random_temp2 is not None:
                                        print("RR N galaxies: ",len(random_temp),len(random_temp2))
                                        if i==ii and j==jj and k==kk:
                                            hist_temp,edges = pyncorr.cartesian_distance(random_temp,random_temp2,histrange=(0,hrange),nbins=nbins, same_coords=True)
                                            tot_calc_rr += (len(random_temp)*len(random_temp2) - len(random_temp2))/2
                                        else:
                                            hist_temp,edges = pyncorr.cartesian_distance(random_temp,random_temp2,histrange=(0,hrange),nbins=nbins)
                                            tot_calc_rr += (len(random_temp)*len(random_temp2))
                                        d += hist_temp
dd = d
pyncorr.write_out_paircounts(d,edges,nr,nr,filename='rr.dat',norm=(nr*nr-nr)/2.0)

#exit()
#exit()


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
