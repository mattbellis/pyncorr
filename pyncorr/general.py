import numpy as np

from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=70, Om0=0.3)


################################################################################
def read_in_columnar_data(filename, cols_to_use=[0,1,2], delimiter=None, convert=None):

    vals = np.loadtxt(filename,unpack=True,delimiter=delimiter)

    # Assume that we will always read in at least 3 values
    A,B,C = vals[cols_to_use[0]], vals[cols_to_use[1]], vals[cols_to_use[2]]

    if convert=="redz2cmd":
        # We read in ra, dec, and redz
        redz = C
        cmd = cosmo.comoving_distance(redz)
        cmd = cmd.value * 0.7
        return np.array([A, B, cmd])
    elif convert=="radecredz2xyz":
        # We read in ra, dec, and redz
        redz = C
        cmd = cosmo.comoving_distance(redz)
        cmd = cmd.value * 0.7
        x,y,z = radeccmd2xyz(A,B,cmd)
        return np.array([x,y,z])
    elif convert=="radeccmd2xyz":
        # We read in ra, dec, and cmd
        x,y,z = radeccmd2xyz(A,B,C)
        return np.array([x,y,z])
    else:
        # We read in either ra, dec, cmd, or x,y,z
        return np.array([A,B,C])


    

################################################################################
def write_out_paircounts(counts, bin_edges, n0, n1, filename="output.dat", norm=None):

    if norm==None:
        norm = n0*n1

    bin_lo = bin_edges[0:-1]
    bin_hi = bin_edges[1:]

    bin_centers = bin_lo + (bin_hi - bin_lo)

    # We add some zeros for padding, just to make reading in the files
    # a bit easier later on. 
    output = "%d 0 0 0\n" % (n0)
    output += "%d 0 0 0\n" % (n1)
    output += "%d 0 0 0\n" % (norm)

    for a,b,c,d in zip(bin_lo, bin_centers, bin_hi, counts):

        output += "%f %f %f %d\n" % (a,b,c,d)

    outfile = open(filename,'w+')

    outfile.write(output)

    outfile.close()


################################################################################
def radeccmd2xyz(ra, dec, cmd):

    # cmd is comoving distance
    rarad = np.deg2rad(ra)
    decrad = np.deg2rad(dec)

    x=cmd*np.cos(rarad)*np.cos(decrad)
    y=cmd*np.sin(rarad)*np.cos(decrad)
    z=cmd*np.sin(decrad)

    return x,y,z


################################################################################
########### NOT WORKING RIGHT NOW ##############################################
def write_out_tripletcounts(H, edges, n0, n1, n2, filename="output.dat", norm=None):

    if norm==None:
        norm = n0*n1

    # We add some zeros for padding, just to make reading in the files
    # a bit easier later on. 
    output = "{0:d} {1:d} {2:d}\n".format(n0, n1, n2)
    output += "{0:d} {1:d} {2:d}\n".format(H.shape[0], H.shape[1], H.shape[2])
    output += "{0}\n".format(norm)
    for i in range(3):
        for edge in edges[i]:
            output += "{0:.3f} ".format(edge)
        output += "\n"

    for i in range(H.shape[0]):
        for j in range(H.shape[1]):
            for k in range(H.shape[2]):
                output += "{0:d} ".format(int(H[i][j][k]))
            output += "\n"
        output += "\n"


    outfile = open(filename,'w+')

    outfile.write(output)

    outfile.close()

