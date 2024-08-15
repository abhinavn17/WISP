
# FUNCTIONS
###############################################################
# A library of function that are used in the pipeline

from casatasks import gaincal, fluxscale, flagdata, mstransform, applycal, exportfits
import subprocess
import os

def flagsummary(myfile):
       
        s = flagdata(vis=myfile, mode='summary')
        allkeys = s.keys()
        print("Flagging percentage:")
        for x in allkeys:
                try:
                        for y in s[x].keys():
                                flagged_percent = 100.*(s[x][y]['flagged']/s[x][y]['total'])
#                                logging.info(x, y, "%0.2f" % flagged_percent, "% flagged.")
                                logstring = str(x)+' '+str(y)+' '+str(flagged_percent)
                                print(logstring)
                except AttributeError:
                        pass


def mygaincal_ap1(myfile,mycal,myref,myflagspw,myuvracal,calsuffix):

        gtable = [str(myfile)+'.K1', str(myfile)+'.B1' ]
        gaincal(vis=myfile, caltable=str(myfile)+'.AP.G', spw =myflagspw,uvrange=myuvracal,append=True,
                field=mycal,solint = '120s',refant = myref, minsnr = 2.0, solmode ='L1R', gaintype = 'G', calmode = 'ap',
                gaintable = gtable, interp = ['nearest,nearestflag', 'nearest,nearestflag' ], parang = True )
        return gtable


def mygaincal_ap2(myfile,mycal,myref,myflagspw,myuvracal,calsuffix,appflag):

        gtable = [str(myfile)+'.K1'+calsuffix, str(myfile)+'.B1'+calsuffix ]
        gaincal(vis=myfile, caltable=str(myfile)+'.AP.G'+calsuffix, spw =myflagspw,uvrange=myuvracal,append=appflag,
                field=mycal,solint = '120s',refant = myref, minsnr = 2.0, solmode ='L1R', gaintype = 'G', calmode = 'ap',
                gaintable = gtable, interp = ['nearest,nearestflag', 'nearest,nearestflag' ], parang = True )
        return gtable

def getfluxcal(myfile,mycalref,myscal):
        myscale = fluxscale(vis=myfile, caltable=str(myfile)+'.AP.G', fluxtable=str(myfile)+'.fluxscale', reference=mycalref, transfer=myscal,
                    incremental=False)
        return myscale


def getfluxcal2(myfile,mycalref,myscal,calsuffix):
        myscale = fluxscale(vis=myfile, caltable=str(myfile)+'.AP.G'+calsuffix, fluxtable=str(myfile)+'.fluxscale'+calsuffix, reference=mycalref,
                    transfer=myscal, incremental=False)
        return myscale



def mygaincal_ap_redo(myfile,mycal,myref,myflagspw,myuvracal):
   
        gtable = [str(myfile)+'.K1'+'recal', str(myfile)+'.B1'+'recal' ]
        gaincal(vis=myfile, caltable=str(myfile)+'.AP.G.'+'recal', append=True, spw =myflagspw, uvrange=myuvracal,
                field=mycal,solint = '120s',refant = myref, minsnr = 2.0,solmode ='L1R', gaintype = 'G', calmode = 'ap',
                gaintable = gtable, interp = ['nearest,nearestflag', 'nearest,nearestflag' ], parang = True )
        return gtable

def getfluxcal_redo(myfile,mycalref,myscal):
        myscale = fluxscale(vis=myfile, caltable=str(myfile)+'.AP.G'+'recal', fluxtable=str(myfile)+'.fluxscale'+'recal', reference=mycalref,
                    transfer=myscal, incremental=False)
        return myscale

def mytfcrop(myfile,myfield,myants,tcut,fcut,mydatcol,myflagspw):
   
        flagdata(vis=myfile, antenna = myants, field = myfield,        spw = myflagspw, mode='tfcrop', ntime='300s', combinescans=False,
                datacolumn=mydatcol, timecutoff=tcut, freqcutoff=fcut, timefit='line', freqfit='line', flagdimension='freqtime',
                usewindowstats='sum', extendflags = False, action='apply', display='none')
        return


def myrflag(myfile,myfield, myants, mytimdev, myfdev,mydatcol,myflagspw):
   
        flagdata(vis=myfile, field = myfield, spw = myflagspw, antenna = myants, mode='rflag', ntime='scan', combinescans=False,
                datacolumn=mydatcol, winsize=3, timedevscale=mytimdev, freqdevscale=myfdev, spectralmax=1000000.0, spectralmin=0.0,
                extendflags=False, channelavg=False, timeavg=False, action='apply', display='none')
        return


def myrflagavg(myfile,myfield, myants, mytimdev, myfdev,mydatcol,myflagspw):
   
        flagdata(vis=myfile, field = myfield, spw = myflagspw, antenna = myants, mode='rflag', ntime='300s', combinescans=True,
                datacolumn=mydatcol, winsize=3,        minchanfrac= 0.8, flagneartime = True, basecnt = True, fieldcnt = True,
                timedevscale=mytimdev, freqdevscale=myfdev, spectralmax=1000000.0, spectralmin=0.0, extendflags=False,
                channelavg=False, timeavg=False, action='apply', display='none')
        return



def mysplitinit(myfile,myfield,myspw,mywidth,split_filename):
        '''function to split corrected data for any field'''
        #mstransform(vis=myfile, field=myfield, spw=myspw, chanaverage=False, chanbin=mywidth, datacolumn='corrected', outputvis=str(myfield)+'.split.ms')
        mstransform(vis=myfile, field=myfield, spw=myspw, chanaverage=False, chanbin=mywidth, datacolumn='corrected', outputvis=split_filename)
        #myoutvis=str(myfield)+'.split.ms'
        #return myoutvis
        return split_filename


def mysplitavg(myfile,myfield,myspw,mywidth,split_avg_filename):
        '''function to split corrected data for any field'''
#        myoutname=myfile.split('s')[0]+'avg-split.ms'
        #myoutname='avg-'+myfile
        #mstransform(vis=myfile, field=myfield, spw=myspw, chanaverage=True, chanbin=mywidth, datacolumn='data', outputvis=myoutname)
        mstransform(vis=myfile, field=myfield, spw=myspw, chanaverage=True, chanbin=mywidth, datacolumn='data', outputvis=split_avg_filename)
        #return myoutname
        return split_avg_filename


def mytclean(myfile,myniter,mythresh,srno,cell,imsize, mynterms1,mywproj,clean_robust):    # you may change the multi-scale inputs as per your field
        nameprefix = myfile.split('-selfcal')[0]
        nameprefix = nameprefix.split('.')[0]
        print("The image files have the following prefix =",nameprefix)
        if myniter==0:
                myoutimg = nameprefix+'-dirty-img'
        else:
                myoutimg = nameprefix+'-selfcal'+'img'+str(srno)

        print(myfile)

        # command = ['wsclean', '-j', '64', '-size', '8000', '8000', '-scale', '1asec', '-niter', f'{myniter}', '-mgain', '0.8', '-auto-threshold', '3', '-name', f'{myoutimg}', f'{myfile}']

        # wsclean -name Final -size 8000 8000 -scale 1arcsec -weight briggs 0.0 -niter 100000 -mgain 0.5 -abs-threshold 1e-6 -multiscale -multiscale-scales 0,5,15     -pol i -apply-primary-beam avg-Triang-II_15-02-2024_B3-selfcal7.ms

        command = ['wsclean', '-j', '64', '-name', f'{myoutimg}', '-size', f'{imsize}', f'{imsize}', '-scale', '1asec', '-weight', 'briggs', f'{clean_robust}', '-niter', f'{myniter}', '-mgain', '0.8', '-auto-mask', '3', '-auto-threshold', '0.3', '-multiscale', '-multiscale-scales', '0,5,15', '-channels-out', '2', '-join-channels', '-pol', 'i', f'{myfile}']

        subprocess.call(command)

        return myoutimg


def mysplit(myfile,srno):
        filname_pre = myfile.split('-selfcal')[0]
        filname_pre = filname_pre.split('.')[0]     
      
        mstransform(vis=myfile, field='0', spw='', datacolumn='corrected', outputvis=filname_pre+'-selfcal'+str(srno)+'.ms')
        myoutvis=filname_pre+'-selfcal'+str(srno)+'.ms'
        return myoutvis

def mygaincal_ap(myfile,myref,mygtable,srno,pap,mysolint,myuvrascal,mygainspw):
        fprefix = myfile.split('-selfcal')[0]
        fprefix = fprefix.split('.')[0]
        if pap=='ap':
                mycalmode='ap'
                mysol= mysolint[srno] 
                mysolnorm = True
        else:
                mycalmode='p'
                mysol= mysolint[srno] 
                mysolnorm = False
        if os.path.isdir(fprefix+str(pap)+str(srno)+'.GT'):
                os.system('rm -rf '+fprefix+str(pap)+str(srno)+'.GT')

        gaincal(vis=myfile, caltable=fprefix+str(pap)+str(srno)+'.GT', append=False, field='0', spw=mygainspw,
                uvrange=myuvrascal, solint = mysol, refant = myref, minsnr = 2.0,solmode='L1R', gaintype = 'G',
                solnorm= mysolnorm, calmode = mycalmode, gaintable = [], interp = ['nearest,nearestflag', 'nearest,nearestflag' ], 
                parang = True )
        mycal = fprefix+str(pap)+str(srno)+'.GT'
        return mycal



def myapplycal(myfile,mygaintables):

        applycal(vis=myfile, field='0', gaintable=mygaintables, gainfield=['0'], applymode='calflag', 
                 interp=['linear'], calwt=False, parang=False)
        print('Ran applycal.')        


def flagresidual(myfile,myclipresid,myflagspw):

        print("Flagging residual data...")
      
        flagdata(vis=myfile, mode ='rflag', datacolumn="RESIDUAL_DATA", field='', timecutoff=6.0,  freqcutoff=6.0,
                timefit="line", freqfit="line",        flagdimension="freqtime", extendflags=False, timedevscale=6.0,
                freqdevscale=6.0, spectralmax=500.0, extendpols=False, growaround=False, flagneartime=False,
                flagnearfreq=False, action="apply", flagbackup=True, overwrite=True, writeflags=True)
      
        flagdata(vis=myfile, mode ='clip', datacolumn="RESIDUAL_DATA", clipminmax=myclipresid,
                clipoutside=True, clipzeros=True, field='', spw=myflagspw, extendflags=False,
                extendpols=False, growaround=False, flagneartime=False,        flagnearfreq=False,
                action="apply",        flagbackup=True, overwrite=True, writeflags=True)
      
        flagdata(vis=myfile,mode="summary",datacolumn="RESIDUAL_DATA", extendflags=False, 
                name=myfile+'temp.summary', action="apply", flagbackup=True,overwrite=True, writeflags=True)
#


         

def myselfcal(myfile,myref,nloops,nploops,myvalinit,mycellsize,myimagesize,mynterms2,mywproj1,mysolint1,myclipresid,myflagspw,mygainspw2,mymakedirty,niterstart,clean_robust, clipresid, uvrascal):
        myref = myref
        nscal = nloops # number of selfcal loops
        npal = nploops # number of phasecal loops
        # selfcal loop
        myimages=[]
        mygt=[]
        myniterstart = niterstart
        myniterend = 200000        
        if nscal == 0:
                i = nscal
                myniter = 0 # this is to make a dirty image
                mythresh = str(myvalinit/(i+1))+'mJy'
                print("Using "+ myfile[i]+" for making only an image.")
                myimg = mytclean(myfile[i],myniter,mythresh,i,mycellsize,myimagesize,mynterms2,mywproj1,clean_robust)   # tclean
                exportfits(imagename=myimg+'.image.tt0', fitsimage=myimg+'.fits')
                
        else:
                for i in range(0,nscal+1): # plan 4 P and 4AP iterations
                        if mymakedirty == True:
                                if i == 0:
                                        myniter = 0 # this is to make a dirty image
                                        mythresh = str(myvalinit/(i+1))+'mJy'
                                        print("Using "+ myfile[i]+" for making only a dirty image.")
                                        myimg = mytclean(myfile[i],myniter,mythresh,i,mycellsize,myimagesize,mynterms2,mywproj1,clean_robust)   # tclean

                        else:
                                myniter=int(myniterstart*2**i) #myniterstart*(2**i)  # niter is doubled with every iteration int(startniter*2**count)
                                if myniter > myniterend:
                                        myniter = myniterend
                                mythresh = str(myvalinit/(i+1))+'mJy'
                                if i < npal:
                                        mypap = 'p'
#                                        print("Using "+ myfile[i]+" for imaging.")
                                
                                        myimg = mytclean(myfile[i],myniter,mythresh,i,mycellsize,myimagesize,mynterms2,mywproj1,clean_robust)   # tclean
                                        myimages.append(myimg)        # list of all the images created so far
                                        flagresidual(myfile[i],clipresid,'')
                                        if i>0:
                                                myctables = mygaincal_ap(myfile[i],myref,mygt[i-1],i,mypap,mysolint1,uvrascal,mygainspw2)
                                        else:                                        
                                                myctables = mygaincal_ap(myfile[i],myref,mygt,i,mypap,mysolint1,uvrascal,mygainspw2)                                                
                                        mygt.append(myctables) # full list of gaintables
                                        if i < nscal+1:
                                                myapplycal(myfile[i],mygt[i])
                                                myoutfile= mysplit(myfile[i],i)
                                                myfile.append(myoutfile)
                                else:
                                        mypap = 'ap'
#                                        print("Using "+ myfile[i]+" for imaging.")
                                        
                                        myimg = mytclean(myfile[i],myniter,mythresh,i,mycellsize,myimagesize,mynterms2,mywproj1,clean_robust)   # tclean
                                        myimages.append(myimg)        # list of all the images created so far
                                        flagresidual(myfile[i],clipresid,'')
                                        if i!= nscal:
                                                myctables = mygaincal_ap(myfile[i],myref,mygt[i-1],i,mypap,mysolint1,'',mygainspw2)
                                                mygt.append(myctables) # full list of gaintables
                                                if i < nscal+1:
                                                        myapplycal(myfile[i],mygt[i])
                                                        myoutfile= mysplit(myfile[i],i)
                                                        myfile.append(myoutfile)
#                                print("Visibilities from the previous selfcal will be deleted.")
                                print("Visibilities from the previous selfcal will be deleted.")
                                if i < nscal and i != 0:
                                        # fprefix = myfile[i].split('.')[0]
                                        # myoldvis = fprefix+'-selfcal'+str(i-1)+'.ms'
                                        myoldvis = myfile[i]    
                                        print("Deleting "+str(myoldvis))
                                        os.system('rm -rf '+str(myoldvis)+ '*')
#                        print('Ran the selfcal loop')
        return myfile, mygt, myimages



#def getspws(myfile):
#        ms.open(myfile)
#        metadata = ms.metadata()
#        ms.done()
#        nspw = metadata.nspw()
#        metadata.done()
#        return nspw

#############End of functions##############################################################################
