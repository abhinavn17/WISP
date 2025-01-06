import os
import sys
from astropy.io import fits
from astropy.time import Time
import numpy as np
import glob 
import datetime
import matplotlib.pyplot as plt
import tqdm

def snapshot_join(directory, new_file, interval):


    if os.path.exists(new_file):
        os.remove(new_file)

    fits_files = glob.glob(f"{directory}/*.fits")

    fits_files.sort()

    # Read data and headers
    data_list = []

    with tqdm.tqdm(total=len(fits_files)) as pbar:
        for file in fits_files:
            with fits.open(file) as hdul:
                
                ddata = np.squeeze(hdul[0].data)

                if np.nansum(ddata) == 0:
                    ddata = np.full_like(ddata, np.nan)    
                    # continue

                data_list.append(ddata)
                pbar.update(1)

    # Stack data along the time axis (assuming consistent dimensions)
    cube_data = np.stack(data_list, axis=0)

    # Load the header from the first FITS file and update it
    with fits.open(fits_files[0]) as hdul:
        header = hdul[0].header


    header['NAXIS'] = 3
    header['CFREQ'] = str(header['CRVAL3'] / 1e6) + 'MHz'
    header['BANDWID'] = str(header['CDELT3'] / 1e6) + 'MHz'

    del header['NAXIS4']
    del header['CRVAL4']
    del header['CDELT4']
    del header['CRPIX4']
    del header['CUNIT4']
    del header['CTYPE4']

    header['CTYPE3'] = 'TIME'
    header['CRVAL3'] = 1
    header['CDELT3'] = interval
    header['CRPIX3'] = 1
    header['CUNIT3'] = 'seconds'

    hdu = fits.PrimaryHDU(data=cube_data, header=header)

    hdu.writeto(new_file, overwrite=True)

    print(f"New FITS file written to {new_file}")

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: python snapshot_join.py <directory> <output>")
        sys.exit(1)

    snapshot_join(sys.argv[1], sys.argv[2])