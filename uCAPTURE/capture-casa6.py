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

from ugfunctions import *
import configparser
config = configparser.ConfigParser()
config.read('config_capture.ini')

fromlta = config.getboolean('basic', 'fromlta')
fromfits = config.getboolean('basic', 'fromfits')
frommultisrcms = config.getboolean('basic','frommultisrcms')
findbadants = config.getboolean('basic','findbadants')                          
flagbadants= config.getboolean('basic','flagbadants')                      
findbadchans = config.getboolean('basic','findbadchans')                         
flagbadfreq= config.getboolean('basic','flagbadfreq')                           
flaginit = config.getboolean('basic','flaginit')                             
doinitcal = config.getboolean('basic','doinitcal')                              
doflag = config.getboolean('basic','doflag')                              
redocal = config.getboolean('basic','redocal')                              
dosplit = config.getboolean('basic','dosplit')                               
flagsplitfile = config.getboolean('basic','flagsplitfile')                            
dosplitavg = config.getboolean('basic','dosplitavg')                             
doflagavg = config.getboolean('basic','doflagavg')                             
makedirty = config.getboolean('basic','makedirty')                            
doselfcal = config.getboolean('basic','doselfcal') 
dosubbandselfcal = config.getboolean('basic','dosubbandselfcal')
usetclean = config.getboolean('default','usetclean')                        
ltafile =config.get('basic','ltafile')
gvbinpath = config.get('basic', 'gvbinpath').split(',')
fits_file = config.get('basic','fits_file')
msfilename =config.get('basic','msfilename')
splitfilename =config.get('basic','splitfilename')
splitavgfilename = config.get('basic','splitavgfilename')
setquackinterval = config.getfloat('basic','setquackinterval')
ref_ant = config.get('basic','ref_ant')
clipfluxcal = [float(config.get('basic','clipfluxcal').split(',')[0]),float(config.get('basic','clipfluxcal').split(',')[1])]
clipphasecal =[float(config.get('basic','clipphasecal').split(',')[0]),float(config.get('basic','clipphasecal').split(',')[1])]
cliptarget =[float(config.get('basic','cliptarget').split(',')[0]),float(config.get('basic','cliptarget').split(',')[1])]   
clipresid=[float(config.get('basic','clipresid').split(',')[0]),float(config.get('basic','clipresid').split(',')[1])]
chanavg = config.getint('basic','chanavg')
subbandchan = config.getint('basic','subbandchan')
imcellsize = [config.get('basic','imcellsize')]
imsize_pix = int(config.get('basic','imsize_pix'))
clean_robust = float(config.get('basic','clean_robust'))
scaloops = config.getint('basic','scaloops')
mJythreshold = float(config.get('basic','mJythreshold'))
pcaloops = config.getint('basic','pcaloops')
scalsolints = config.get('basic','scalsolints').split(',')
niter_start = int(config.get('basic','niter_start'))
use_nterms = config.getint('basic','use_nterms')
nwprojpl = config.getint('basic','nwprojpl')
uvracal=config.get('default','uvracal')
uvrascal=config.get('default','uvrascal')
target = config.getboolean('default','target')

flagsummary(msfilename)
clearcal(vis = msfilename)
myfile2 = [msfilename]
myselfcal(myfile2,ref_ant,scaloops,pcaloops,mJythreshold,imcellsize,imsize_pix,use_nterms,nwprojpl,scalsolints,clipresid,"","",False,niter_start,clean_robust, clipresid, uvrascal)
