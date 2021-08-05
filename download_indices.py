# code to download several climate indices 
# indices: ONI-MEI-SOI
#          PDO
#          MAO
#          SAM
#          DMI
#          Polar vortex

import requests
import xarray as xr
import numpy as np
import pandas as pd
# download indices
# ninio
url = 'https://psl.noaa.gov/data/correlation/nina34.anom.data'

r = requests.get(url)

with open('nino34.data', 'wb') as f:
    f.write(r.content)
f.close()
FILE = 'nino34.data'
data = []

with open(FILE) as f:
    f.readline()
    for line in f:
        columns = line.split()
        data.append(np.asarray([float(i) for i in columns[1:]]))
        if columns[0] == '2020': break
data = np.concatenate(data, axis=0)
data[data==-99.99] = np.nan
time = pd.date_range('1948-01-15', freq='M', periods=np.shape(data)[0])
ninio34 = xr.DataArray(data=data, coords={'time':(['time'], time)}, dims=['time'])
ninio34 = ninio34.sel(time=slice('1950-01-01', '2020-12-31'))
#compute monthly anomalies
ninio34 = ninio34.groupby('time.month') - ninio34.groupby('time.month').mean('time', skipna=True)
#compute 3-month running mean
ninio34_filtered = np.convolve(ninio34.values, np.ones((3,))/3, mode='same')
ninio34_f = xr.DataArray(ninio34_filtered, coords=[ninio34.time.values], dims=['time'])
ninio34_f.to_netcdf('ninio34.nc4')

# mei
url = 'https://psl.noaa.gov/enso/mei.old/table.html'
r = requests.get(url)

with open('mei.data', 'wb') as f:
    f.write(r.content)
f.close()

FILE = 'mei.data'
data = []
with open(FILE) as f:
    for i in range(14):
        line = f.readline()
    while line:
        line = f.readline()
        columns = line.split()
        data.append(np.asarray([float(i) for i in columns[1:]]))
        if columns[0] == '2018':
            break
data = np.concatenate(data, axis=0)
data[data==-99.99] = np.nan
time = pd.date_range('1950-01-15', freq='M', periods=np.shape(data)[0])
mei = xr.DataArray(data, coords=[time], dims=['time'])
mei = mei.sel(time=slice('1950-01-01', '2017-12-31'))
mei.to_netcdf('mei.nc4')


# pdo
url = 'https://www.ncdc.noaa.gov/teleconnections/pdo/data.txt'
r = requests.get(url)

with open('pdo.data', 'wb') as f:
    f.write(r.content)
f.close()

FILE = 'pdo.data'
data = []
with open(FILE) as f:
    f.readline()
    f.readline()
    for line in f:
        columns = line.split()
        data.append(np.asarray([float(i) for i in columns[1:]]))
        if columns[0] == '2020':
            break
data = np.concatenate(data, axis=0)
data[data==-99.99] = np.nan
time = pd.date_range('1854-01-15', freq='M', periods=np.shape(data)[0])
pdo = xr.DataArray(data, coords=[time], dims=['time'])
pdo = pdo.sel(time=slice('1950-01-01', '2020-12-31'))
pdo.to_netcdf('pdo.nc4')

# amo
url = 'https://psl.noaa.gov/data/correlation/amon.us.data'
r = requests.get(url)

with open('amo.data', 'wb') as f:
    f.write(r.content)
f.close()

FILE = 'amo.data'
data = []
with open(FILE) as f:
    f.readline()
    for line in f:
        columns = line.split()
        data.append(np.asarray([float(i) for i in columns[1:]]))
        if columns[0] == '2020': break
data = np.concatenate(data, axis=0)
data[data==-99.99] = np.nan
time = pd.date_range('1948-01-15', freq='M', periods=np.shape(data)[0])
amo = xr.DataArray(data, coords=[time], dims=['time'])
amo = amo.sel(time=slice('1950-01-01', '2020-12-31'))
amo.to_netcdf('amo.nc4')

# sam
url = 'http://www.nerc-bas.ac.uk/public/icd/gjma/newsam.1957.2007.txt'
r = requests.get(url)
with open('sam.data', 'wb') as f:
    f.write(r.content)
f.close()
FILE = 'sam.data'
data = []
with open(FILE) as f:
    f.readline()
    f.readline()
    f.readline()
    for line in f:
        columns = line.split()
        data.append(np.asarray([float(i) for i in columns[1:]]))
data = np.concatenate(data, axis=0)
time = pd.date_range('1957-01-15', freq='M', periods=np.shape(data)[0])
sam = xr.DataArray(data, coords=[time], dims=['time'])
# 3-month running mean
sam_filtered = np.convolve(sam.values, np.ones((3,))/3, mode='same')
sam_f = xr.DataArray(sam_filtered, coords=[sam.time.values], dims=['time'])
sam = sam_f.sel(time=slice('1957-01-01', '2020-12-31'))
sam.to_netcdf('sam.nc4')

# dmi
url = 'https://psl.noaa.gov/gcos_wgsp/Timeseries/Data/dmi.had.long.data'
r = requests.get(url)

with open('dmi.data', 'wb') as f:
    f.write(r.content)
f.close()

FILE = 'dmi.data'
data = []
with open(FILE) as f:
    f.readline()
    for line in f:
        columns = line.split()
        data.append(np.asarray([float(i) for i in columns[1:]]))
        if columns[0] == '2020': break
data = np.concatenate(data, axis=0)
data[data==-9999.0] = np.nan
time = pd.date_range('1870-01-15', freq='M', periods=np.shape(data)[0])
dmi = xr.DataArray(data, coords=[time], dims=['time'])
dmi = dmi.sel(time=slice('1950-01-01', '2020-12-31'))
dmi.to_netcdf('dmi.nc4')

