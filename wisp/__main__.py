import numpy as np
from datetime import datetime
from casatasks import clearcal, delmod

from .ugfunctions import *
import configparser
import argparse

def main():

    parser = argparse.ArgumentParser(description='uCAPTURE: CAsa Pipeline-cum-Toolkit for Upgraded GMRT data REduction')
    parser.add_argument('config', help='Configuration file')

    args = parser.parse_args()

    config = configparser.ConfigParser()

    config.read(args.config)
    
    msfilename =config.get('default','msfilename')
    ref_ant = config.get('default','ref_ant')
    scaloops = config.getint('default','scaloops')
    # mJythreshold = float(config.get('default','mJythreshold'))
    clipresid = config.get('default','clipresid')
    pcaloops = config.getint('default','pcaloops')
    scalsolints = config.get('default','scalsolints').split(',')
    niter_start = int(config.get('default','niter_start'))
    # use_nterms = config.getint('default','use_nterms')
    # nwprojpl = config.getint('default','nwprojpl')
    nsubbands = config.getint('default','nsubbands')
    wscommand = config.get('default','wsclean-command')
    uvrange = config.get('default','uvrange')
    join_scans = config.getfloat('default','join_scans')
    nproc = config.getint('default','nproc')

    try:
        use_gnet = config.getboolean('default','use_gnet')
    except:
        use_gnet = True

    print("Starting Wsclean Imaging and Selfcal Pipeline")
    
    # flagsummary(msfilename)
    clearcal(vis = msfilename)
    # delmod(vis = msfilename)
    myfile2 = [msfilename]
    myselfcal(myfile2,ref_ant,scaloops,pcaloops,scalsolints,"",False,nsubbands,niter_start, uvrange, clipresid, wscommand, join_scans, nproc, use_gnet)


if __name__ == '__main__':

    main()