
# import os, sys

# varExists = True
# projectDir = '/Users/daria/.conda/envs/platosim'
# workDir = '/Users/daria/Desktop/DEUP/Work_Directory'

# globals()['projectDir'] = '/Users/daria/.conda/envs/platosim'
# globals()['PLATO_WORKDIR']  = '/Users/daria/Desktop/DEUP/Work_Directory'

# if not 'projectDir' in globals():
#     varExists = False
#     print ("The global variable projectDir does not exist, set projectDir to the proper location in your environment.")

# if not 'PLATO_WORKDIR' in globals():
#     varExists = False
#     print ("The global variable workDir does not exist, set workDir to the proper location in your environment.")

# if varExists:
#     os.environ['PLATO_PROJECT_HOME'] = projectDir
#     os.environ['PLATO_WORKDIR'] = workDir
#     sys.path.append(projectDir + "/python")


from matplotlib import pyplot as plt

from numpy import *
import h5py



plt.rcParams['figure.figsize'] = (10, 4)


# f = h5py.File("/Volumes/My Passport/PLATO Project/test.hdf5")


f = h5py.File("0-7E-S_m9_a.hdf5")
# f = h5py.File("t1_P=35_6.hdf5")
# print(len(array(f["StarPositions"]["Time"])))
# print(list(f.keys()))
time = array(f["StarPositions"]["Time"])/(60*60*24)
stars = ['69324', '69387', '69376']
#print(list(f["/Photometry/Lightcurves"].keys()))
for i in range(1):
    Flux = f["/Photometry/Lightcurves/starID%s/estimatedFlux" % stars[i] ]
    print(len(Flux))
    # relativeFlux = (Flux - mean(Flux))/mean(Flux) 
    # normFlux = Flux/mean(Flux[:622])
    # print("mean ", mean(Flux))
    # print("standard deviation ", std(Flux))
    # print("mean - min ", mean(Flux) - min(Flux))
    # print("max - mean",  max(Flux) - mean(Flux))
    # print(time[13820])
    plt.scatter(time[:], Flux[:], marker='.', s=1)
    plt.ylabel('Flux')
    plt.xlabel('time (days)')
    # plt.title('Star %s' % stars[i])
    plt.show()

# from scipy import stats
# bins = len(time)/(60*60/25)
# bin_means, bin_edges, binnumber = stats.binned_statistic(
#     time, Flux,
#     statistic='mean',
#     bins=bins)
# bin_stds, _, _ = stats.binned_statistic(
#     time, Flux,
#     statistic='std',
#     bins=bins)
# bin_width = (bin_edges[1] - bin_edges[0])
# bin_centers = bin_edges[1:] - bin_width/2

# plt.errorbar(
#     bin_centers,
#     bin_means,
#     # yerr=bin_stds/2,
#     # xerr=bin_width/2,
#     marker='.',
#     markersize=6,
#     color='black',
#     #capsize=10,
#     linestyle='none')
# plt.show()
