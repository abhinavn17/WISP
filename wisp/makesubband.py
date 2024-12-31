try:
    from casampi import MPIEnvironment, MPICommandClient
except:
    pass

import sys
import os
from casatasks import mstransform

def makesubbands(myfile,newfile,nsubbands):

        mstransform(vis=myfile,outputvis=newfile, datacolumn='DATA',regridms=True, nspw=nsubbands, combinespws= False, keepflags=True)
                
        return newfile

if __name__ == '__main__':

    makesubbands(sys.argv[1], sys.argv[2], int(sys.argv[3]))
