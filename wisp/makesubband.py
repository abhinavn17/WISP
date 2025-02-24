try:
    from casampi import MPIEnvironment, MPICommandClient
except:
    pass

import sys
import os
from casatasks import mstransform

def makesubbands(myfile,newfile,nsubbands):
        
        mstransform(vis=myfile, outputvis=newfile, datacolumn='DATA',regridms=True, nspw=nsubbands, keepflags=True)
                
        return newfile

def joinsubbands(myfiles,newfile):
        
        mstransform(vis=myfiles, outputvis=newfile, datacolumn='DATA',regridms=False, keepflags=True, combinespws=True)
                
        return newfile

if __name__ == '__main__':

    if len(sys.argv) == 4:
        makesubbands(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    elif len(sys.argv) == 3:
        joinsubbands(sys.argv[1], sys.argv[2])
