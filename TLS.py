from matplotlib import pyplot as plt
from numpy import *
import h5py

# workDir = '/Users/daria/Desktop/DEUP/Work_Directory'
# globals()['PLATO_WORKDIR']  = '/Users/daria/Desktop/DEUP/Work_Directory'

plt.rcParams['figure.figsize'] = (10, 4)

# T = 10*24*60*60 #period in seconds

f = h5py.File("/Volumes/My Passport/PLATO Project/Work_Directory1-3/WASP-14.hdf5")
fl = f["/Photometry/Lightcurves/starID69324/estimatedFlux"]
n = mean(fl[:346])
flux = fl/n
time = array(f["StarPositions"]["Time"])/(60*60*24)

# f1 = h5py.File("/Users/daria/Desktop/DEUP/Work_Directory/WASP-166/W166_t1.hdf5")
# f2 = h5py.File("/Users/daria/Desktop/DEUP/Work_Directory/WASP-166/W166_e1.hdf5")
# f3 = h5py.File("/Users/daria/Desktop/DEUP/Work_Directory/WASP-166/W166_t2.hdf5")
# f4 = h5py.File("/Users/daria/Desktop/DEUP/Work_Directory/WASP-166/W166_e2.hdf5")
# f5 = h5py.File("/Users/daria/Desktop/DEUP/Work_Directory/WASP-166/W166_t3.hdf5")
# f6 = h5py.File("/Users/daria/Desktop/DEUP/Work_Directory/WASP-166/W166_e3.hdf5")

# fl1 = f1["/Photometry/Lightcurves/starID69324/estimatedFlux"]
# fl2 = f2["/Photometry/Lightcurves/starID69324/estimatedFlux"]
# fl3 = f3["/Photometry/Lightcurves/starID69324/estimatedFlux"]
# fl4 = f4["/Photometry/Lightcurves/starID69324/estimatedFlux"]
# fl5 = f5["/Photometry/Lightcurves/starID69324/estimatedFlux"]
# fl6 = f6["/Photometry/Lightcurves/starID69324/estimatedFlux"]
# t1 = array(f1["StarPositions"]["Time"])/(60*60*24)
# t2 = array(f2["StarPositions"]["Time"])/(60*60*24)
# t3 = array(f3["StarPositions"]["Time"])/(60*60*24)
# t4 = array(f4["StarPositions"]["Time"])/(60*60*24)
# t5 = array(f5["StarPositions"]["Time"])/(60*60*24)
# t6 = array(f6["StarPositions"]["Time"])/(60*60*24)


# There must be a better way to do that...
# for i in range(1,6):
#         fl%s = f%s["/Photometry/Lightcurves/starID69324/estimatedFlux"] , % i
#         t%s = array(f%s["StarPositions"]["Time"])/(60*60*24) , % i


# interval = t1[1]-t1[0]
# interval_e = t2[1]-t2[0]
# print(interval)
# print(interval_e)
# time = arange(0, round(T*3/(24*60*60)), step=interval) #in days  

# flux = []
# b = 668225.4735244141 #typical flux value outside of transit / eclipse
# # 0.1*24*60*60/25 = 346
# n = mean(fl1[:346]) #mean
# end1 = round(t1[-1]/interval) #or len(t1)
# start2 = round(t2[0]/interval_e)
# end2 = round(t2[-1]/interval_e)
# start3 = round(t3[0]/interval)
# end3 = round(t3[-1]/interval)
# start4 = round(t4[0]/interval_e)
# end4 = round(t4[-1]/interval_e)
# start5 = round(t5[0]/interval)
# end5 = round(t5[-1]/interval)
# start6 = round(t6[0]/interval_e)
# end6 = round(t6[-1]/interval_e)

# for i in range(len(time)): 
#         if i < end1:
#                 flux.append(fl1[i])
#         elif start2 <= i < end2:
#                 flux.append(fl2[i-start2])
#         elif start3 <= i < end3:
#                 flux.append(fl3[i-start3])
#         elif start4 <= i < end4:
#                 flux.append(fl4[i-start4])
#         elif start5 <= i < end5:
#                 flux.append(fl5[i-start5])
#         elif start6 <= i < end6:
#                 flux.append(fl6[i-start6])
#         else:
#                 flux.append(n)


# for i in range(len(time)): 
#         if i < end1:
#                 flux.append(fl1[i]/n)
#         elif start2 <= i < end2:
#                 flux.append(fl2[i-start2]/n)
#         elif start3 <= i < end3:
#                 flux.append(fl3[i-start3]/n)
#         elif start4 <= i < end4:
#                 flux.append(fl4[i-start4]/n)
#         elif start5 <= i < end5:
#                 flux.append(fl5[i-start5]/n)
#         elif start6 <= i < end6:
#                 flux.append(fl6[i-start6]/n)
#         else:
#                 flux.append(1.)



# norm_flux = flux/mean(flux) #mean gets set to 1


# print(mean(flux))

# plt.scatter(time, flux, marker='.')
# plt.show()

from transitleastsquares import transitleastsquares
model = transitleastsquares(time, flux) #normalised flux against time
results = model.power() #R_star=1., n_transits_max=3, inc=87. , u=[0.1, 0.3]

print('Period', format(results.period, '.5f'), 'd')
print("Period uncertainty: ", results.period_uncertainty)
print(len(results.transit_times), 'transit times in time series:', \
        ['{0:0.5f}'.format(i) for i in results.transit_times])
print('Transit depth', format(results.depth, '.5f'))
print(len(results.transit_depths_uncertainties), 'Transit depth uncertainties:', \
        ['{0:0.5f}'.format(i) for i in results.transit_depths_uncertainties])
print('Best duration (days)', format(results.duration, '.5f'))
print('Signal detection efficiency (SDE):', results.SDE)
print("FAP: ", results.FAP)



# from transitleastsquares import period_grid
# periods = period_grid(R_star=1, M_star=1, time_span=10)
# plt.plot(periods)
# plt.show()



# #Periodogram
# plt.figure()
# ax = plt.gca()
# ax.axvline(results.period, alpha=0.4, lw=3)
# plt.xlim(min(results.periods), max(results.periods))
# for n in range(2, 10): 
#     ax.axvline(n*results.period, alpha=0.4, lw=1, linestyle="dashed")
#     if results.period / n >= 0.6: #I added
#         ax.axvline(results.period / n, alpha=0.4, lw=1, linestyle="dashed")
# plt.ylabel(r'SDE')
# plt.xlabel('Period (days)')
# plt.plot(results.periods, results.power, color='black', lw=0.5)
# plt.xlim(0, max(results.periods))
# plt.show()

# #Phase folded light curve
# plt.figure()
# plt.plot(results.model_folded_phase, results.model_folded_model, color='red')
# plt.scatter(results.folded_phase, results.folded_y, color='blue', s=10, alpha=0.5, zorder=2)
# #plt.xlim(0.48, 0.52)
# plt.ticklabel_format(useOffset=False)
# plt.xlabel('Phase')
# plt.ylabel('Relative flux');
# plt.show()


# # from scipy import stats
# # bins = 500
# # bin_means, bin_edges, binnumber = stats.binned_statistic(
# #     results.folded_phase,
# #     results.folded_y,
# #     statistic='mean',
# #     bins=bins)
# # bin_stds, _, _ = stats.binned_statistic(
# #     results.folded_phase,
# #     results.folded_y,
# #     statistic='std',
# #     bins=bins)
# # bin_width = (bin_edges[1] - bin_edges[0])
# # bin_centers = bin_edges[1:] - bin_width/2

# # plt.plot(results.model_folded_phase, results.model_folded_model, color='red')
# # plt.scatter(results.folded_phase, results.folded_y, color='blue', s=10, alpha=0.5, zorder=2)
# # plt.errorbar(
# #     bin_centers,
# #     bin_means,
# #     yerr=bin_stds/2,
# #     xerr=bin_width/2,
# #     marker='o',
# #     markersize=8,
# #     color='black',
# #     #capsize=10,
# #     linestyle='none')
# # plt.xlim(0.48, 0.52)
# # plt.ticklabel_format(useOffset=False)
# # plt.xlabel('Phase')
# # plt.ylabel('Relative flux');
# # plt.show()