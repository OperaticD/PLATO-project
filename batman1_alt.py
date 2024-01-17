import batman
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

params = batman.TransitParams()
params.per = 356.25                     #orbital period 
params.rp = 0.00915/2                  #planet radius (in units of stellar radii) // 0.00915
params.a = 214.9                       #semi-major axis (in units of stellar radii) // 214.9
params.inc = 90.                     #orbital inclination (in degrees) // 
params.ecc = 0.                      #eccentricity
params.w = 90.                       #longitude of periastron (in degrees)
params.u = [0.3985, 0.2586]               #limb darkening coefficients [u1, u2]// [0.5528, 0.1548]
params.limb_dark = "quadratic"       #limb darkening model
params.t0 = 1.                      #Central eclipse time / inferior conjunction

Vmag = 4.83

t = 10.
n_data = round(t*24*60*60/25 + 20)

time = np.linspace(0, t, n_data)

#Transit simulation
m1 = batman.TransitModel(params, time, transittype="primary")    #initializes model
flux1 = m1.light_curve(params)          #calculates light curve

#Eclipse simulation
params.fp = 0.0000042                   #Planet to star flux ratio // 0.002
params.t_secondary = params.t0 + params.per/2
m2 = batman.TransitModel(params, time, transittype="secondary")
flux2 = m2.light_curve(params)

flux = []
s = params.t_secondary
d = t/n_data
p = params.per

lows = []
highs = []
for j in range(0,round(t/p)+1):
    lows.append(round((s-0.02+p*j)/d))
    highs.append(round((s+0.02+p*j)/d))


for i in range(n_data):
    if np.any((np.array(lows) <= i) & (i <= np.array(highs))) == True: 
    # or i in range(round((s-0.02+p)/d),round((s+0.02+p)/d)) or i in range(round((s-0.02+2*p)/d), round((s+0.02+2*p)/d)), 
        # or i in range(round((s-0.02+3*p)/d), round((s+0.02+3*p)/d)) or i in range(round((s-0.02+4*p)/d), round((s+0.02+4*p)/d)):
        flux.append(flux2[i] - params.fp)
    else:
        flux.append(flux1[i])






delta_mag = (1-np.asarray(flux))*Vmag

t_seconds = np.linspace(0, t*24*60*60, n_data)
c = zip(t_seconds, delta_mag)

with open("model_file.txt", 'w') as outfile:
    for elem in c:
        outfile.write(repr(elem[0]) + " " + repr(elem[1]) +"\n")

plt.plot(time, flux)
plt.xlabel("Time (in days)")
plt.ylabel("Flux")
#plt.ylim(0.9999, 1.0001)
plt.show()
