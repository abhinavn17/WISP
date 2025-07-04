import configparser
import os
import sys
import numpy as np
from casatools import table
import argparse

def main():

    argparser = argparse.ArgumentParser(description='Create a configuration file for GNET calibration pipeline.')

    argparser.add_argument('--cfgfile', '-c',  type=str, default= 'wisp.ini', help='output configuration file name for calibration.')
    argparser.add_argument('msfile', type=str, help='Measurement set file to be calibrated.')

    args = argparser.parse_args()

    cffile = args.cfgfile
    msfile = args.msfile

    path = os.path.dirname(os.path.abspath(__file__))

    cffile = os.path.abspath(cffile)

    msfile = os.path.abspath(msfile)

    if not os.path.isfile(cffile):
        os.system(f'cp {path}/config.ini ' + cffile)

    cfg = configparser.ConfigParser()
    cfg.read(cffile)

    cfg.set('SELFCAL', 'msfilename', msfile)

    with open(cffile, 'w') as configfile:
        cfg.write(configfile)

if __name__ == '__main__':

    main()