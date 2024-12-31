try:
    from casampi import MPIEnvironment, MPICommandClient
except:
    pass

from casatasks import flagdata
import os
import sys

myfile = sys.argv[1]
myclipresid = sys.argv[2]

myclipresid = myclipresid.split(',')
myclipresid = [float(myclipresid[0]), float(myclipresid[1])]

flagdata(vis=myfile, mode ='rflag', datacolumn="RESIDUAL_DATA", field='', timecutoff=6.0,  freqcutoff=6.0,
                        timefit="line", freqfit="line",        flagdimension="freqtime", extendflags=False, timedevscale=6.0,
                        freqdevscale=6.0, spectralmax=500.0, extendpols=False, growaround=False, flagneartime=False,
                        flagnearfreq=False, action="apply", flagbackup=True, overwrite=True, writeflags=True)

flagdata(vis=myfile, mode ='clip', datacolumn="RESIDUAL_DATA", clipminmax=myclipresid,
                        clipoutside=True, clipzeros=True, field='', spw='', extendflags=False,
                        extendpols=False, growaround=False, flagneartime=False,        flagnearfreq=False,
                        action="apply",        flagbackup=True, overwrite=True, writeflags=True)