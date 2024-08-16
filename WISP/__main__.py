import numpy as np
from datetime import datetime
from casatasks import clearcal

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
    clipfluxcal = [float(config.get('default','clipfluxcal').split(',')[0]),float(config.get('default','clipfluxcal').split(',')[1])]
    clipphasecal =[float(config.get('default','clipphasecal').split(',')[0]),float(config.get('default','clipphasecal').split(',')[1])]
    cliptarget =[float(config.get('default','cliptarget').split(',')[0]),float(config.get('default','cliptarget').split(',')[1])]   
    clipresid=[float(config.get('default','clipresid').split(',')[0]),float(config.get('default','clipresid').split(',')[1])]
    # imcellsize = [config.get('default','imcellsize')]
    # imsize_pix = int(config.get('default','imsize_pix'))
    # clean_robust = float(config.get('default','clean_robust'))
    scaloops = config.getint('default','scaloops')
    mJythreshold = float(config.get('default','mJythreshold'))
    pcaloops = config.getint('default','pcaloops')
    scalsolints = config.get('default','scalsolints').split(',')
    niter_start = int(config.get('default','niter_start'))
    # use_nterms = config.getint('default','use_nterms')
    # nwprojpl = config.getint('default','nwprojpl')
    wscommand = config.get('default','wsclean-command')
    uvrange = config.get('default','uvrange')

    print("Starting uCAPTURE Imaging pipeline")
    
    flagsummary(msfilename)
    clearcal(vis = msfilename)
    myfile2 = [msfilename]
    myselfcal(myfile2,ref_ant,scaloops,pcaloops,mJythreshold,scalsolints,clipresid,"",False,niter_start, uvrange, wscommand)


if __name__ == '__main__':

    main()