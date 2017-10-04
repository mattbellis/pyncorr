import numpy as np

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

    # com is comoving distance
    rarad = np.deg2rad(ra)
    decrad = np.deg2rad(dec)

    x=cmd*np.cos(ra)*np.cos(dec)
    y=cmd*np.sin(ra)*np.cos(dec)
    z=cmd*np.sin(dec)

    return x,y,z


