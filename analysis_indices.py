# script to analyze the joint distribution of  climate indices 
# indices: ONI
#          MEO
#          PDO
#          AMO
#          SAM
#          DMI
from __future__ import unicode_literals
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# open data
ninio34 = xr.open_dataarray('ninio34.nc4')
mei = xr.open_dataarray('mei.nc4')
pdo = xr.open_dataarray('pdo.nc4')
amo = xr.open_dataarray('amo.nc4')
sam = xr.open_dataarray('sam.nc4')
dmi = xr.open_dataarray('dmi.nc4')

# select common period Jan 1957 - Sep 2009

ninio34 = ninio34.sel(time=slice('1957-01-01', '2009-09-30'))
mei = mei.sel(time=slice('1957-01-01', '2009-09-30'))
pdo = pdo.sel(time=slice('1957-01-01', '2009-09-30'))
amo = amo.sel(time=slice('1957-01-01', '2009-09-30'))
sam = sam.sel(time=slice('1957-01-01', '2009-09-30'))
dmi = dmi.sel(time=slice('1957-01-01', '2009-09-30'))

#plot all series

#relevant thresholds

# ninio/mei: +- 0.5
# pdo : +- 0.5
# amo :  + -
# sam: + -

# combinations relevants for droughts

# ninio/mei, pdo, dmi -
# sam, amo +

# todos favoreciendo sequia
index1 = np.logical_and(np.logical_and(np.logical_and(ninio34.values < -0.5, dmi < 0), np.logical_and(pdo < -0.5, amo > 0)), sam > 0)
# todos menos sam favoreciendo sequia
index2 = np.logical_and(np.logical_and(ninio34.values < -0.5, dmi < 0), np.logical_and(pdo < -0.5, amo > 0))
# todos menos iod favoreciendo sequia
index3 = np.logical_and(np.logical_and(ninio34.values < -0.5, np.logical_and(pdo < -0.5, amo > 0)), sam > 0)
# ninio pdo y amo favoreciendo sequia
index4 = np.logical_and(ninio34.values < -0.5, np.logical_and(pdo < -0.5, amo > 0))

#print('Todos los indices fav sequia:', ninio34.time[index1])
#print('Todos menos sam fav sequia:', ninio34.time[index2])
#print('Todos menos iod fav sequia:', ninio34.time[index3])
#print('Ninio, PDO and AMO fav sequia:', ninio34.time[index4])

ninio34 = ninio34.sel(time=slice('1959-09-30', '2009-09-30'))
mei = mei.sel(time=slice('1959-09-30', '2009-09-30'))
pdo = pdo.sel(time=slice('1959-09-30', '2009-09-30'))
amo = amo.sel(time=slice('1959-09-30', '2009-09-30'))
sam = sam.sel(time=slice('1959-09-30', '2009-09-30'))
dmi = dmi.sel(time=slice('1959-09-30', '2009-09-30'))

fig2 = plt.figure(figsize = (10, 8), dpi=300)  #fig size in inches
for i in range(2):
    color = iter(cm.rainbow(np.linspace(0, 1, 5)))
    c = next(color)
    ax = plt.subplot(2, 1, i + 1)
    l1 = ax.plot(ninio34.time[i * 120 + 3 * 120: 3 * 120 + (i + 1) * 120], ninio34[(i + 3) * 120 : (i + 4) * 120],
            color = c, linewidth=1.5, label = 'Niño')
    c = next(color)
    l2 = ax.plot(pdo.time[i * 120 + 3 * 120: (i + 1) * 120 + 3 * 120], pdo[(i + 3) * 120 : (i + 4) * 120],
            color = c, linewidth=1.5, label = 'PDO')
    c = next(color)
    c = next(color)
    #ax.plot(amo.time[i * 120 + 3 * 120: (i + 1) * 120 + 3 * 120], amo[(i + 3) * 120 : (i + 4) * 120],
    #        color = c, linewidth=1.5, label = 'AMO')
    #c = next(color)
    l3 = ax.plot(sam.time[i * 120 + 3 * 120: (i + 1) * 120 + 3 * 120], sam[(i + 3) * 120 : (i + 4) * 120],
            color = c, linewidth=1.5, label = 'SAM')
    c = next(color)
 #   ax.plot(dmi.time[i * 120 + 3 * 120: (i + 1) * 120 + 3 * 120], dmi[(i + 3) * 120 : (i + 4) * 120],
 #           color = c, linewidth=1.5, label = 'DMI')
    ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
    l4 = ax2.plot(amo.time[i * 120 + 3 * 120: (i + 1) * 120 + 3 * 120], amo[(i + 3) * 120 : (i + 4) * 120],
            color = c, linewidth=1.5, label = 'AMO')
    ax2.tick_params(axis='y', labelcolor=c)

    ax.set_xlim((dmi.time[i * 120 + 3 * 120], dmi.time[(i + 1) * 120 + 3 * 120]))
    ax.hlines(0, dmi.time[i * 120 + 3 * 120], dmi.time[(i + 1) * 120 + 3 * 120], colors='black',
            linestyles='solid', label='')
    ax.set_ylim((-4, 4))
    ax2.set_ylim((-0.8, 0.8))
    if i ==1:
        ax.axvspan(np.datetime64('2007-09-01'), np.datetime64('2008-03-31') , alpha=0.4, color='gray')
    if i ==0:
        ax.axvspan(np.datetime64('1998-07-01'), np.datetime64('1999-06-30') , alpha=0.4, color='gray')
lns = l1 + l2 + l3 + l4
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, bbox_to_anchor=(0.2, -0.3), loc='lower left', ncol=5, borderaxespad=0.)
plt.suptitle('Time series climate indices' ,fontsize=12, x=0.52, y=0.93)
plt.savefig('ejemplo2.jpg', dpi=300)
plt.close()
fig1 = plt.figure(figsize = (10,17), dpi = 300)  #fig size in inches
for i in range(5):
    color = iter(cm.rainbow(np.linspace(0, 1, 5)))
    c = next(color)
    ax = plt.subplot(5, 1, i + 1)
    ax.plot(ninio34.time[i * 120 : (i + 1) * 120], ninio34[i * 120 : (i + 1) * 120],
            color = c, linewidth=1.5, label = 'Niño')
    c = next(color)
    ax.plot(pdo.time[i * 120 : (i + 1) * 120], pdo[i * 120 : (i + 1) * 120],
            color = c, linewidth=1.5, label = 'PDO')
    c = next(color)
#    c = next(color)
    ax.plot(amo.time[i * 120 : (i + 1) * 120], amo[i * 120 : (i + 1) * 120],
            color = c, linewidth=1.5, label = 'AMO')
    c = next(color)
    ax.plot(sam.time[i * 120 : (i + 1) * 120], sam[i * 120 : (i + 1) * 120],
            color = c, linewidth=1.5, label = 'SAM')
    c = next(color)
    ax.plot(dmi.time[i * 120 : (i + 1) * 120], dmi[i * 120 : (i + 1) * 120],
            color = c, linewidth=1.5, label = 'DMI')
    ax.set_xlim((dmi.time[i * 120], dmi.time[(i + 1) * 120]))
    ax.hlines(0, dmi.time[i * 120], dmi.time[(i + 1) * 120], colors='black', linestyles='solid',
            label='')
    ax.set_ylim((-4, 4))
    if i ==4:
        ax.axvspan(np.datetime64('2007-09-01'), np.datetime64('2008-03-31') , alpha=0.4, color='gray')
    if i ==3:
        ax.axvspan(np.datetime64('1998-07-01'), np.datetime64('1999-06-30') , alpha=0.4, color='gray')

plt.legend(bbox_to_anchor=(0.2, -0.3), loc='lower left', ncol=5, borderaxespad=0.)
plt.suptitle('Time series climate indices' ,fontsize=12, x=0.52, y=0.93)
plt.savefig('ejemplo.jpg', dpi=300)
plt.close()
