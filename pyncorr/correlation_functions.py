import numpy as np
import scipy.spatial as spatial

def cartesian_distance(coord0, coord1, nbins=100, histrange=(0,200), same_coords=False):

    # For debugging
    #hist = np.histogram(coord0.transpose()[0], bins=nbins, range=histrange)
    #hist_tot = hist[0]
    #bin_edges = hist[1]
    #return hist_tot,bin_edges

    # Assume the data is coming in ngals x 3 arrays
    # x, y, z (all in Mpc)
    # For example, 
    # [ [ 1253.0, 2384.4, 3425.24], 
    #   [ 1987.5, 2564.7, 2439.42], 
    #   ......................... ]

    #print("Ngals: %d %d" % (len(coord0), len(coord1)))
    nc0 = len(coord0)
    nc1 = len(coord1)

    print("sizes: ",nc0,nc1)

    big_Ngals = False
    if nc0>=5000 or nc1>5000:
        big_Ngals = True

    ############### THIS WILL BE FOR OTHER STUFF ################
    # ra (radians), dec (radians), r (co-moving distance, Mpc)
    # For example,
    # [ [ 0.3242, 0.2384, 3425.24], 
    #   [ 0.9871, 0.5647, 2439.42], 
    #   ......................... ]
    ########################################################

    hist_tot = np.zeros(nbins,dtype=int)
    bin_edges = None

    #if len(coord0)<=10000 and len(coord1)<=10000:
    # Get the limits of the cdist to do
    div = 10000 # Max number of coords to do at once
    limits0 = np.arange(0,nc0,div)
    if limits0[-1]<nc0:
        limits0 = np.concatenate((limits0,np.array([nc0])))
    limits1 = np.arange(0,nc1,div)
    if limits1[-1]<nc1:
        limits1 = np.concatenate((limits1,np.array([nc1])))

    print(limits0)
    print(limits1)

    for i in range(len(limits0)-1):
        for j in range(len(limits1)-1):
            print(i,j)
            if same_coords:
                if j>=i:
                    idx0 = limits0[i]
                    idx1 = limits0[i+1]
                    jdx0 = limits1[j]
                    jdx1 = limits1[j+1]
                    if i==j:
                        dist = spatial.distance.pdist(coord0[idx0:idx1], 'euclidean')
                    else:
                        dist = spatial.distance.cdist(coord0[idx0:idx1], coord1[jdx0:jdx1], 'euclidean')
                        dist = dist.flatten()
            else:
                #idx0 = i
                #idx1 = i+1
                #jdx0 = j
                #jdx1 = j+1
                idx0 = limits0[i]
                idx1 = limits0[i+1]
                jdx0 = limits1[j]
                jdx1 = limits1[j+1]
                #dist = spatial.distance.cdist(coord0, coord1, 'euclidean')
                dist = spatial.distance.cdist(coord0[idx0:idx1], coord1[jdx0:jdx1], 'euclidean')
                dist = dist.flatten()

            hist = np.histogram(dist, bins=nbins, range=histrange)

            hist_tot += hist[0]
            bin_edges = hist[1]

    return hist_tot,bin_edges

    if 0:
    #else:
        coord1_T = coord1.transpose() 

        ncoord0 = len(coord0)
        #print(ncoord0)

        #hist_tot = np.zeros(nbins,dtype=int)
        #bin_edges = None

        # Loop over each point in ncoord0 and calculate
        # the distance with *all* of ncoord1 at once. 
        for i in range(ncoord0):

            '''
            if i%1000==0:
                print("On %d out of %d gals" % (i, ncoord0))
            '''

            temp_coord = coord0[i]

            if same_coords:
                dx = temp_coord[0] - coord1_T[0][i+1:]
                dy = temp_coord[1] - coord1_T[1][i+1:]
                dz = temp_coord[2] - coord1_T[2][i+1:]
            else:
                dx = temp_coord[0] - coord1_T[0]
                dy = temp_coord[1] - coord1_T[1]
                dz = temp_coord[2] - coord1_T[2]

            dist = np.sqrt(dx*dx + dy*dy + dz*dz)
            #temp = dist[dist<=1]
            #if len(temp)>0:
                #print(temp)

            # Histogram it here. This is efficient if we pass in a large number of
            # galaxies, but it can become slower if the numbers are small.
            hist = np.histogram(dist, bins=nbins, range=histrange)

            hist_tot += hist[0]
            bin_edges = hist[1]

    return hist_tot,bin_edges






