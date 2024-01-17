import h5py
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# f = h5py.File('/Volumes/My Passport/PLATO Project/test.hdf5', 'r')
f = h5py.File('test.hdf5', 'r')
print(list(f.keys()))
Im = f['Images']
SC = f['StarCatalog']
# Phot = f['/Photometry/Lightcurves/starID69324/estimatedFlux']
starIDs = SC['starIDs']

# print(list(f['StarPositions'].keys()))
# plt.imshow(Im, cmap=cm.pink, interpolation="nearest", origin='lower')
# plt.show()

names = list(Im.keys())


for i in range(len(names)):

      plt.imshow(Im[str(names[i])], cmap=cm.pink, interpolation="nearest", origin='lower')
      plt.show()