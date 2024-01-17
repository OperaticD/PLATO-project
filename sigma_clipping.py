from astropy.stats import sigma_clip
import h5py
import numpy as np
from matplotlib import pyplot as plt
import wotan
import pandas as pd
from transitleastsquares import transitleastsquares


time = np.array(h5py.File("/Volumes/My Passport/PLATO Project/Unprocessed/0-7E-S_m9_1.hdf5")["StarPositions"]["Time"])/(60*60*24)
f1 = h5py.File("/Volumes/My Passport/PLATO Project/Unprocessed/0-7E-S_m9_1.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
f2 = h5py.File("/Volumes/My Passport/PLATO Project/Unprocessed/0-7E-S_m9_2.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
f3 = h5py.File("/Volumes/My Passport/PLATO Project/Unprocessed/0-7E-S_m9_3.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
f4 = h5py.File("/Volumes/My Passport/PLATO Project/Unprocessed/0-7E-S_m9_4.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
f5 = h5py.File("/Volumes/My Passport/PLATO Project/Unprocessed/0-7E-S_m9_a.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]
f6 = h5py.File("/Volumes/My Passport/PLATO Project/Unprocessed/0-7E-S_m9_b.hdf5")["/Photometry/Lightcurves/starID69324/estimatedFlux"]


flux_array = [f1[:], f2[:], f3[:], f4[:], f5[:], f6[:]] # , f4[:], f5[:], f6[:]
flux = np.mean(flux_array, axis=0)



flatten_lc = wotan.flatten(time, flux, method='rspline', window_length=2, return_trend=False)

# flatten_lc = wotan.flatten(time, flux, method='biweight', window_length=1, return_trend=False)

plt.scatter(time, flatten_lc, s=1, color='black')
plt.xlabel('Time (days)')
plt.ylabel('Detrended flux')
plt.show()

day = round(24*60*60/25)
window = round(day*0.2)

pd_f = pd.Series(flatten_lc)
sigma = pd_f.rolling(window).std()
med = pd_f.rolling(window).median()

f_clip = []

for i in range(len(time)):
    if flatten_lc[i] < med[i] - 3*sigma[i] or flatten_lc[i] > med[i] + 3*sigma[i]:
        f_clip.append(np.nan)
    else:
        f_clip.append(flatten_lc[i])


plt.scatter(time[window:], f_clip[window:], s=1, color='black')
plt.xlabel('Time (days)')
plt.ylabel('Clipped & Detrended Flux')
plt.show()


def p2p_rms(fl):
    dflux = np.diff(fl)
    med_dflux = np.nanmedian(dflux)
    up_p2p = (
        np.nanpercentile( np.sort(dflux-med_dflux), 84 )
        -
        np.nanpercentile( np.sort(dflux-med_dflux), 50 )
    )
    lo_p2p = (
        np.nanpercentile( np.sort(dflux-med_dflux), 50 )
        -
        np.nanpercentile( np.sort(dflux-med_dflux), 16 )
    )
    p2p = np.mean([up_p2p, lo_p2p])
    return p2p

dy = np.ones_like(time)*p2p_rms(f_clip)

model = transitleastsquares(time[window:], f_clip[window:], dy=dy) #np.full(len(f_clip), 0.01)
results = model.power(oversampling_factor=1, R_star=1., M_star=1., transit_depth_min=0.00005) #R_star=1., n_transits_max=3, inc=87. , u=[0.1, 0.3]
# f_clip_flat = wotan.flatten(time, f_clip, method='biweight', window_length=1., return_trend=False)
print('Signal detection efficiency (SDE):', results.SDE)
print('Period', format(results.period, '.5f'), 'd')
print("Period uncertainty: ", results.period_uncertainty)
print(len(results.transit_times), 'transit times in time series:', \
        ['{0:0.5f}'.format(i) for i in results.transit_times])
print('Transit depth', format(results.depth, '.5f'))
print(len(results.transit_depths_uncertainties), 'Transit depth uncertainties:', \
        ['{0:0.5f}'.format(i) for i in results.transit_depths_uncertainties])
print('Best duration (days)', format(results.duration, '.5f'))
print("FAP: ", results.FAP)

# while results.period < 48.0 or results.period == np.nan:
#     model = transitleastsquares(time[window:], f_clip[window:], dy=dy) #np.full(len(f_clip), 0.01)
#     results = model.power(oversampling_factor=1, R_star=1., M_star=1., transit_depth_min=(1 - results.depth + (1 - results.depth)/10)) #R_star=1., n_transits_max=3, inc=87. , u=[0.1, 0.3]
#     print("transit depth min:", 1 - results.depth + results.depth/10)
#     print('Signal detection efficiency (SDE):', results.SDE)
#     print('Period', format(results.period, '.5f'), 'd')
#     print("Period uncertainty: ", results.period_uncertainty)
#     print(len(results.transit_times), 'transit times in time series:', \
#             ['{0:0.5f}'.format(i) for i in results.transit_times])
#     print('Transit depth', format(results.depth, '.5f'))
#     print(len(results.transit_depths_uncertainties), 'Transit depth uncertainties:', \
#             ['{0:0.5f}'.format(i) for i in results.transit_depths_uncertainties])
#     print('Best duration (days)', format(results.duration, '.5f'))
#     print("FAP: ", results.FAP)


plt.figure()
plt.scatter(results.folded_phase, results.folded_y, color='blue', s=10, alpha=0.5, zorder=2)
plt.plot(results.model_folded_phase, results.model_folded_model, color='red')
plt.ticklabel_format(useOffset=False)
plt.xlabel('Phase', fontsize=20)
plt.ylabel('Relative flux', fontsize=20)
plt.show()

plt.figure()
ax = plt.gca()
ax.axvline(results.period, alpha=0.4, lw=3)
plt.xlim(min(results.periods), max(results.periods))
for n in range(2, 10): 
    ax.axvline(n*results.period, alpha=0.4, lw=1, linestyle="dashed")
    if results.period / n >= 0.6: #I added
        ax.axvline(results.period / n, alpha=0.4, lw=1, linestyle="dashed")
plt.ylabel(r'Signal Detection Efficiency', fontsize=20)
plt.xlabel('Period (days)', fontsize=20)
plt.plot(results.periods, results.power, color='black', lw=0.5)
plt.xlim(0, max(results.periods))
plt.show()
