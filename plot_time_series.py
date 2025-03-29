import os
import sys
from astropy.io import fits
from astropy.time import Time
import numpy as np
import glob 
import datetime
import matplotlib.pyplot as plt
import tqdm

# List of FITS files
directory = sys.argv[1]
interval = float(sys.argv[2])

try:
    x = int(sys.argv[3])
    y = int(sys.argv[4])
except:
    x = 0
    y = 0

fits_files = glob.glob(f"{directory}/*.fits")

fits_files.sort()

name = '-'.join(fits_files[0].split('-')[:-2])

name = name.split('/')[-1]

time_stamps = []

# Read data and headers
time_series = []
rms_series = []
i = 0

with tqdm.tqdm(total=len(fits_files)) as pbar:
    for file in fits_files:
        with fits.open(file) as hdul:
            ddata = np.squeeze(hdul[0].data)

            if np.nansum(ddata) == 0:
                ddata = np.full_like(ddata, np.nan)    
                # continue

            if x:
                time_series.append(ddata[y, x])
            else:
                time_series.append(ddata[np.shape(ddata)[1]//2, np.shape(ddata)[2]//2])

            rms_series.append(np.nanstd(ddata))
            # print(f"RMS: {np.nanstd(ddata)}")
            i += 1

            if i == 0:
                obs_time = hdul[0].header['DATE-OBS']
                obs_time = Time(obs_time, format='isot', scale='utc')
            # time_stamps.append(Time(obs_time).mjd)
            pbar.update(1)

x_axis = np.arange(0, len(time_series)*interval, interval)

pulse = np.array(time_series)

mean_rms = np.nanmean(rms_series)

print(f"Mean RMS: {mean_rms}")

pulse = np.where(pulse<-5*mean_rms, 0, pulse)

plt.plot(x_axis, pulse)

plt.xlabel('Time (s)')
plt.ylabel('Flux (Jy/beam)')

plt.title(f'{name} Time Series')

plt.savefig(f"{name}-time-series.png")
