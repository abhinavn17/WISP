import numpy as np
from datetime import datetime
from casatasks import mstransform

from .ugfunctions import *
import configparser
import argparse

def main():

    parser = argparse.ArgumentParser(description='WISP: WSClean Imaging and Selfcal Pipeline')
    parser.add_argument('config', help='Configuration file')

    args = parser.parse_args()

    config = configparser.ConfigParser()

    config.read(args.config)
    
    msfilename =config.get('SELFCAL','msfilename')
    ref_ant = config.get('SELFCAL','ref_ant')
    scaloops = config.getint('SELFCAL','scaloops')
    avg_bin = config.getint('SELFCAL','avg_bin')
    # mJythreshold = float(config.get('SELFCAL','mJythreshold'))
    clipresid = config.get('SELFCAL','clipresid')
    pcaloops = config.getint('SELFCAL','pcaloops')
    scalsolints = config.get('SELFCAL','scalsolints').split(',')
    niter_start = int(config.get('SELFCAL','niter_start'))
    nsubbands = config.getint('SELFCAL','nsubbands')
    #wscommand = config.get('SELFCAL','wsclean-command')
    uvrange = config.get('SELFCAL','uvrange')
    join_scans = config.getfloat('SELFCAL','join_scans')
    nproc = config.getint('SELFCAL','nproc')
    wsclean_params = {k: v for k, v in config.items('SELFCAL') if k.startswith('wsclean')}

    print("wsclean parameters:", wsclean_params)

    try:
        use_gnet = config.getboolean('SELFCAL','use_gnet')
    except:
        use_gnet = True

    print("Starting Wsclean Imaging and Selfcal Pipeline")

    if avg_bin > 1:
        print(f"Using {avg_bin} channel bin for averaging the data.")
        msfilename_avg = msfilename.replace('.ms', '_avg.ms')

        if os.path.exists(msfilename_avg):
            print(f"Removing existing averaged MS file: {msfilename_avg}")
            os.system(f'rm -rf {msfilename_avg}')

        mstransform(vis = msfilename, outputvis= msfilename_avg, datacolumn = 'data', chanaverage= True, chanbin = avg_bin, keepflags = True)
    
    myfile = msfilename_avg if avg_bin > 1 else msfilename
  
    myselfcal(myfile,ref_ant,scaloops,pcaloops,scalsolints,"",False,nsubbands,niter_start, uvrange, clipresid, wsclean_params, join_scans, nproc, use_gnet)


if __name__ == '__main__':

    main()