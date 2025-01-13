try:
    from casampi import MPIEnvironment, MPICommandClient
except:
    pass

from casatasks import split, applycal
import os
import sys

myfile = sys.argv[1]
mygaintables = sys.argv[2]  
srno = int(sys.argv[2])


filname_pre = myfile.split('-selfcal')[0]
filname_pre = filname_pre.split('.')[0]     
myoutvis=filname_pre+'-selfcal'+str(srno)+'.ms'

print('\nRunning applycal...')        
applycal(vis=myfile, spw = '', field='0', gaintable=mygaintables, gainfield=['0'], applymode='calflag', 
            interp=['linearperobs,linearflagrel'], calwt=False, parang=False)

print("Splitting into "+myoutvis + "...")

if os.path.exists(myoutvis):
        print("File "+myoutvis+" already exists. Deleting it.")
        os.system(f'rm -rf {myoutvis}*') 

split(vis=myfile, field='0', datacolumn='corrected', outputvis=myoutvis, keepmms=True)