try:
    from casampi import MPIEnvironment, MPICommandClient
except:
    pass

import sys
import os
from casatasks import mstransform
# from casatools import msmetadata

def makesubbands(myfile,nsubbands):

        newfile=myfile.split('.ms')[0]+'_subbands.ms'
        
        if os.path.exists(newfile):
                
            print("Subband MS already exists. Skipping...")

            return newfile

        mstransform(vis=myfile,outputvis=newfile, datacolumn='DATA',regridms=True, nspw=nsubbands, combinespws= False, keepflags=True)
                
        return newfile

if __name__ == '__main__':

    makesubbands(sys.argv[1],int(sys.argv[2]))

