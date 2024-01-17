import h5py
from numpy import *
from matplotlib import pyplot as plt
import wotan
from transitleastsquares import transitleastsquares

plt.rcParams['figure.figsize'] = (12, 7)




# time = array(h5py.File("/Volumes/My Passport/PLATO Project/Simulations/E-S_cont30_1.hdf5")["StarPositions"]["Time"])/(60*60*24)
# f1 = h5py.File("/Volumes/My Passport/PLATO Project/Simulations/E-S_cont30_1.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
# f2 = h5py.File("/Volumes/My Passport/PLATO Project/Simulations/E-S_cont30_2.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
# f3 = h5py.File("/Volumes/My Passport/PLATO Project/Simulations/E-S_cont30_3.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
# f4 = h5py.File("/Volumes/My Passport/PLATO Project/Simulations/E-S_cont30_4.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
# f5 = h5py.File("/Volumes/My Passport/PLATO Project/Simulations/E-S_cont30_5.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
# f6 = h5py.File("/Volumes/My Passport/PLATO Project/Simulations/E-S_cont30_6.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]

time = array(h5py.File("/Volumes/My Passport/PLATO Project/Simulations/2-1E-S_m11_1.hdf5")["StarPositions"]["Time"])/(60*60*24)
f1 = h5py.File("/Volumes/My Passport/PLATO Project/Simulations/2-1E-S_m11_1.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
f2 = h5py.File("/Volumes/My Passport/PLATO Project/Simulations/2-1E-S_m11_2.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
f3 = h5py.File("/Volumes/My Passport/PLATO Project/Simulations/2-1E-S_m11_3.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
f4 = h5py.File("/Volumes/My Passport/PLATO Project/Simulations/2-1E-S_m11_4.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
f5 = h5py.File("/Volumes/My Passport/PLATO Project/Simulations/2-1E-S_m11_5.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
f6 = h5py.File("/Volumes/My Passport/PLATO Project/Simulations/2-1E-S_m11_6.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]


flux_array = [f1[:], f2[:], f3[:], f4[:] , f5[:], f6[:]] #
mean_f = mean(flux_array, axis=0)

# flux = mean(flux_array, axis=0)

flat1, trend_lc1 = wotan.flatten(time, mean_f, method='rspline', window_length=4, return_trend=True)

new_flux = []
new_time = []

#in terms of indices
limit = 300 # < w
w = 1000      # width of box = 0.3 days of exposures
h = 0.1       # height of box - half the "width" of the signal?


def count(pt, width, height):   # counts number of points in box
    c = 0
    for i in range(round(width/2)):
        if abs(flat1[pt+i] - flat1[pt]) < height/2:
            c += 1 
        if abs(flat1[pt-i] - flat1[pt]) < height/2:
            c += 1
    return c

j = 0

while j < round(len(flat1) - w):
    if count(round(j + w/2), w, h) >= limit:
        # new_flux.append(mean(flux[round(j - w/2):round(j + w/2)])) # faster method
        new_flux.append(flat1[round(j + w/2)])
        new_time.append(time[round(j + w/2)])
        # j += round(w/2) # faster
        j += 1
    else:
        j += round(w/2)

plt.scatter(time, flat1, s=1, color='green')
plt.scatter(new_time, new_flux, s=1, color='black')
plt.show()

plt.scatter(new_time, new_flux, s=1, color='black')
plt.show()

# flat2, trend_lc2 = wotan.flatten(new_time, new_flux, method='biweight', window_length=0.5, return_trend=True)

# plt.scatter(new_time, flat2, s=1, color='blue')
# plt.show()

# plt.scatter(time, flat1, s=1, color='green')
# plt.show()

model = transitleastsquares(new_time, new_flux) #normalised flux against time 
results = model.power(oversampling_factor=1) #R_star=1, inc=87. , u=[0.1, 0.3], transit_depth_min=10e-7

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

plt.figure()
plt.scatter(results.folded_phase, results.folded_y, color='blue', s=10, alpha=0.5, zorder=2)
plt.plot(results.model_folded_phase, results.model_folded_model, color='red')
plt.ticklabel_format(useOffset=False)
plt.xlabel('Phase')
plt.ylabel('Relative flux');
plt.show()

plt.figure()
ax = plt.gca()
ax.axvline(results.period, alpha=0.4, lw=3)
plt.xlim(min(results.periods), max(results.periods))
for n in range(2, 10): 
    ax.axvline(n*results.period, alpha=0.4, lw=1, linestyle="dashed")
    if results.period / n >= 0.6: #I added
        ax.axvline(results.period / n, alpha=0.4, lw=1, linestyle="dashed")
plt.ylabel(r'SDE')
plt.xlabel('Period (days)')
plt.plot(results.periods, results.power, color='black', lw=0.5)
plt.xlim(0, max(results.periods))
plt.show()