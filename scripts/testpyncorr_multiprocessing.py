import numpy as np
import pyncorr
import matplotlib.pylab as plt

from multiprocessing import Pool

if __name__ == '__main__':

    # Read in some data
    data = np.loadtxt('../test_data/GRID_model_data.dat',unpack=True)
    random = np.loadtxt('../test_data/GRID_model_random.dat',unpack=True)

    nd = len(data[0])
    nr = len(random[0])

    data = data.transpose()
    random = random.transpose()

    x = data
    y = random
    hrange = 450
    nbins = 200

    with Pool(3) as p:
        result = p.starmap(pyncorr.cartesian_distance, [(x,x),(y,y),(x,y)], kwds={'histrange':(0,hrange),'nbins':nbins})
        print(result[0])
        print(result[1])
        print(result[2])

    #'''
    pyncorr.write_out_paircounts(result[0][0],result[0][1],nd,nr,filename='dr.dat',norm=nd*nr)
    pyncorr.write_out_paircounts(result[1][0],result[1][1],nd,nd,filename='dd.dat',norm=(nd*nd-nd)/2.0)
    pyncorr.write_out_paircounts(result[2][0],result[2][1],nr,nr,filename='rr.dat',norm=(nr*nr-nr)/2.0)
    #'''


