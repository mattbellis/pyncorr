import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt

seed = np.random.seed(seed=5)
data = np.random.random((100,3))
seed = np.random.seed(seed=10)
random = np.random.random((100,3))

d_split = np.array_split(data,3)

d1 = spatial.distance.cdist(d_split[0][:],random[:])
d2 = spatial.distance.cdist(d_split[1][:],random[:])
d3 = spatial.distance.cdist(d_split[2][:],random[:])


d = np.concatenate( (np.concatenate(d1[:]),np.concatenate(d2[:]),np.concatenate(d3[:])) )
#d1=np.concatenate(d1[:])

plt.figure()
plt.hist(d,bins=100)
plt.show()