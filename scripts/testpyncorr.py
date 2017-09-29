import numpy as np
import pyncorr
import matplotlib.pylab as plt

nd = 1000
nr = 1000

x = np.random.random((nd,3))
y = np.random.random((nr,3))

d,edges = pyncorr.cartesian_distance(x,y,histrange=(0,1.5))
dr = d
print(d)
print(sum(d))
print()
print(edges)

print()

d,edges = pyncorr.cartesian_distance(x,x,histrange=(0,1.5),same_coords=True)
dd = d
print(d)
print(sum(d))
print()
print(edges)

d,edges = pyncorr.cartesian_distance(y,y,histrange=(0,1.5),same_coords=True)
rr = d
print(d)
print(sum(d))
print()
print(edges)

bin_centers = edges[0:-1] + (edges[1:] - edges[0:-1])

plt.figure()
plt.plot(bin_centers,dr,label='dr')
plt.plot(bin_centers,dd,label='dd')
plt.plot(bin_centers,rr,label='rr')
plt.legend()

ddnorm = (nd*nd - nd)/2.0
rrnorm = (nr*nr - nr)/2.0
drnorm = nr*nd

w = ((dd/ddnorm) - (2*dr/drnorm) + (rr/rrnorm))/(rr/rrnorm)

plt.figure()
plt.plot(bin_centers,w,label='w')
plt.legend()



plt.show()
