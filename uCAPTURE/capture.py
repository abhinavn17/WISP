###################################################################
# CAPTURE: CAsa Pipeline-cum-Toolkit for Upgraded GMRT data REduction
###################################################################
# Pipeline for analysing data from the GMRT and the uGMRT.
# Combination of pipelines done by Ruta Kale based on pipelines developed independently by Ruta Kale 
# and Ishwar Chandra.
# Date: 8th Aug 2019
# README : Please read the following instructions to run this pipeline on your data
# Files and paths required
# 0. This files from git should be placed and executed in the directory where your data files are located.
# 1. If starting from lta file, please provide the paths to the listscan and gvfits executable binaries in "gvbinpath" as shown.
# 2. Keep the vla-cals.list file in the same area.
# Please email ruta@ncra.tifr.res.in if you run into any issue and cannot solve.
# 


import sys
import logging
import os
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