import numpy as np
from scipy import spatial
import matplotlib.pylab as plt
#import seaborn as sn


d = np.random.random((100,3))
d1=spatial.distance.cdist(d,d,metric='euclidean')
d2=spatial.distance.pdist(d,metric='euclidean')

plt.figure()

plt.hist(np.concatenate(d1),bins=100)
plt.hist(d2,bins=100)

print(len(d2),len(np.concatenate(d1)))

plt.show()

