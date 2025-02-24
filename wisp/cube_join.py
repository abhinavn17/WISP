import os
import sys
from astropy.io import fits
from astropy.time import Time
import numpy as np
import glob 
import datetime
import matplotlib.pyplot as plt
import tqdm

def cube_join(directory, new_file):


    if os.path.exists(new_file):
        os.remove(new_file)

    restfreq = 1420.40575177*1e6

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
        cval1 = header['CRVAL3']

    with fits.open(fits_files[1]) as hdul:
        header2 = hdul[0].header
        cval2 = header2['CRVAL3']

    header['CRVAL3'] = cval1
    header['CDELT3'] = cval2 - cval1
    header['CRPIX3'] = 1

    # Add alternate axis for velocity

    c = 299792458.0
    vopt = c*((restfreq - cval1)/restfreq)

    header['RESTFRQ'] = (restfreq, 'Rest frequency (Hz)')
    header['SPECSYS'] = ('BARYCENT', 'Spectral reference frame')
    header['ALTRVAL'] = ( vopt , 'Alternate frequency reference value')
    header['ALTRPIX'] = 1

    header['COMMENT'] = 'Frequency cube made from WSClean output. Author: Abhinav Narayan'
                         
    hdu = fits.PrimaryHDU(data=cube_data, header=header)

    hdu.writeto(new_file, overwrite=True)

    print(f"New FITS file written to {new_file}")

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: python snapshot_join.py <directory> <output>")
        sys.exit(1)

    cube_join(sys.argv[1], sys.argv[2])