import sys
import os
from casatasks import mstransform, concat
from casatools import msmetadata

def makesubbands(myfile,nsubbands):

        newfile=myfile.split('.ms')[0]+'_subbands.ms'
        
        if os.path.exists(newfile):
                # os.system('rm -rf '+newfile)
                return newfile
        
        if os.path.exists(myfile+'_tmp0'):
                os.system('rm -rf '+myfile+'_tmp*')

        splitspw=[]
        msspw=[]
        gainsplitspw=[]
        ms = msmetadata()
        ms.open(myfile)
        myx=ms.nchan(0)
        msmetadata().close()
        xchan=int(myx/nsubbands)

        if myx>xchan:
                mynchani=myx
                xs=0
                while mynchani>0:
                        if mynchani>xchan:
                            spwi='0:'+str(xs*xchan)+'~'+str(((xs+1)*xchan)-1)
                            if xs==0:
                                gspwi='0:'+str(0)+'~'+str(((xs+1)*xchan)-1)
                            else:
                                gspwi='0:'+str(0)+'~'+str(xchan-1)
                        if mynchani<=xchan:
                            spwi='0:'+str(xs*xchan)+'~'+str((xs*xchan)+mynchani-1)
                            gspwi='0:'+str(0)+'~'+str(mynchani-1)
                        gainsplitspw.append(gspwi)
                        msspw.append(spwi)
                        mynchani=mynchani-xchan
                        myfilei=myfile+'_tmp'+str(xs)
                        xs=xs+1
                        splitspw.append(myfilei)
                for numspw in range(0,len(msspw)):
                        mstransform(vis=myfile,outputvis=splitspw[numspw],spw=msspw[numspw],chanaverage=False,datacolumn='all',realmodelcol=True)
                concat(vis=splitspw,concatvis=newfile)
        mygainspw2=gainsplitspw
                
        # if os.path.exists(myfile+'_tmp'):
        os.system('rm -rf '+myfile+'_tmp*')
        return newfile

if __name__ == '__main__':

    makesubbands(sys.argv[1],sys.argv[2],int(sys.argv[3]))

