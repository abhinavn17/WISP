from casatasks import gaincal, fluxscale, flagdata, split, applycal, exportfits, clearcal
import subprocess
import os
from wisp.makesubband import makesubbands

try:
        import gnet.gnet.rfi_cleaner as rfi_cleaner
        use_gnet = True
except ImportError:
        use_gnet = False
        print("gnet not installed. Defaulting to casa rflag for residual flagging.")
        pass

def flagsummary(myfile):
       
        s = flagdata(vis=myfile, mode='summary')
        allkeys = s.keys()
        print("\nFlagging percentage:")
        for x in allkeys:
                try:
                        for y in s[x].keys():
                                flagged_percent = 100.*(s[x][y]['flagged']/s[x][y]['total'])
#                                logging.info(x, y, "%0.2f" % flagged_percent, "% flagged.")
                                logstring = str(x)+' '+str(y)+' '+str(flagged_percent)
                                print(logstring)
                except AttributeError:
                        pass

def mywsclean(myfile,wsclean_params,myniter,srno):  
        nameprefix = myfile.split('-selfcal')[0]
        nameprefix = nameprefix.split('.')[0]
        print("The image files have the following prefix =",nameprefix)
        if myniter==0:
                myoutimg = nameprefix+'-dirty-img'
        else:
                myoutimg = nameprefix+'-selfcal'+'img'+str(srno)

        size = wsclean_params.get('wsclean_size')
        size = size.split(',')
        scale = wsclean_params.get('wsclean_scale')
        mgain = wsclean_params.get('wsclean_mgain')
        weight = wsclean_params.get('wsclean_weight')
        extra = wsclean_params.get('wsclean_extra')
        extra = extra.split(' ')

        threshold = wsclean_params.get('wsclean_auto_threshold')
        mask = wsclean_params.get('wsclean_auto_mask')

        threshold = threshold.split(',')
        mask = mask.split(',')

        if srno < len(threshold):
                auto_thresh = threshold[srno]
                auto_mask = mask[srno]
        else:
                auto_thresh = threshold[-1]
                auto_mask = mask[-1]

        command = ['wsclean', '-j', '32', '-size', size[0], size[1], '-scale', scale, '-mgain', mgain, '-weight', weight]

        if weight == 'briggs':

                robust = wsclean_params.get('wsclean_robust')
                command.extend([robust])

        if extra[0] != '':

                command.extend(extra)

        command.extend(['-auto-mask', str(auto_mask), '-auto-threshold', str(auto_thresh),'-niter', str(myniter), '-name', myoutimg, myfile])

        subprocess.call(command)

        return myoutimg


def mysplit(myfile, mygaintables, srno, nproc):

        filname_pre = myfile.split('-selfcal')[0]
        filname_pre = filname_pre.split('.')[0]     
        myoutvis=filname_pre+'-selfcal'+str(srno)+'.ms'

        print("Splitting into "+myoutvis + "...")

        if os.path.exists(myoutvis):
                print("File "+myoutvis+" already exists. Deleting it.")
                os.system(f'rm -rf {myoutvis}*') 
      
        # split(vis=myfile, field='0', datacolumn='corrected', outputvis=myoutvis, keepmms=True)

        subprocess.call(['mpirun', '-np', f'{nproc}', 'python', '-m', 'wisp.applycal', f'{myfile}', f'{mygaintables}', f'{srno}'])
        return myoutvis

def mygaincal_ap(myfile,myref,srno,pap,mysolint,myuvrascal,mygainspw):

        print("\nRunning gaincal...")

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
                uvrange=myuvrascal, solint = mysol, refant = myref, minsnr = 2.0, solmode='L1R', gaintype = 'G',
                solnorm= mysolnorm, calmode = mycalmode, gaintable = [], interp = ['nearest,nearestflag', 'nearest,nearestflag' ], 
                parang = True )
        mycal = fprefix+str(pap)+str(srno)+'.GT'
        return mycal



def myapplycal(myfile,mygaintables):

        print('\nRunning applycal...')        
        applycal(vis=myfile, spw = '', field='0', gaintable=mygaintables, gainfield=['0'], applymode='calflag', 
                 interp=['linearperobs,linearflagrel'], calwt=False, parang=False)


def flagresidual(myfile, gnet, myclipresid, join_scans = -1, nproc = 16):

        if gnet:

                rfi_cleaner.clean(myfile, field = 0, datacolumn = 'residual', use_gnet= False, join_scans= join_scans, nproc=nproc, extend=False)
        else:

                print("Running residual flagging using rflag...")

                subprocess.call(['mpirun', '-np', f'{nproc}', 'python', '-m', 'wisp.rflag', f'{myfile}', f'{myclipresid}'])
        
        # flagdata(vis=myfile, mode='clip', clipminmax=[0, 0.75], datacolumn= 'RESIDUAL_DATA')
        # flagdata(vis=myfile, mode='extend', extendpols=False, growtime=75, growfreq=75, growaround=True)
        
        flagsummary(myfile)

def final_split(myfile, nproc):

        filname_pre = myfile.split('-selfcal')[0]
        filname_pre = filname_pre.split('.')[0]     
        myoutvis=filname_pre+'-spw_joined.ms'

        print("Splitting into "+myoutvis + "...")

        if os.path.exists(myoutvis):

                print("File "+myoutvis+" already exists. Deleting it.")
                os.system(f'rm -rf {myoutvis}*')
        
        subprocess.call(['mpirun', '-np', f'{nproc}', 'python', '-m', 'wisp.makesubband', f'{myfile}', f'{myoutvis}'])

        return myoutvis
      

def myselfcal(myfile,myref,nloops,nploops,mysolint1,mygainspw2,mymakedirty, nsubbands, niterstart, uvrascal, myclipresid, wsclean_params, join_scans, nproc, use_gnet = True):
        myref = myref
        nscal = nloops # number of selfcal loops
        npal = nploops # number of phasecal loops
        # selfcal loop
        myimages=[]
        mygt=[]
        myniterstart = niterstart
        # print(myfile)

        if nsubbands > 1:
                print("Making subbands...")

                subband_file = myfile.split('.ms')[0]+'_subbands.ms'
                
                subprocess.call(['mpirun', '-np', f'{nproc}', 'python', '-m', 'wisp.makesubband', f'{myfile}', f'{subband_file}', f'{nsubbands}'])

                myfile = subband_file

                # myfile = [myfile
                # print(myfile)
                # mygainspw2 = mysubbands[1]

        clearcal(vis=myfile)

        myfile = [myfile]  # list of visibilities

        if nscal == 0:
                i = nscal
                myniter = 0 # this is to make a dirty image
                # mythresh = str(myvalinit/(i+1))+'mJy'
                print("Using "+ myfile[i]+" for making only an image.")
                myimg = mywsclean(myfile[i],wsclean_params,myniter,i)   # tclean
                exportfits(imagename=myimg+'.image.tt0', fitsimage=myimg+'.fits')
                
        else:
                for i in range(0,nscal+1): 

                        # if os.path.exists(mygt[i-1]) and skip_loops:
                        #         print("Gaintable "+mygt[i-1]+" exists, skipping selfcal loop{0}".format(i))
                        #         continue

                        if mymakedirty == True:
                                if i == 0:
                                        myniter = 0 # this is to make a dirty image
                                        # mythresh = str(myvalinit/(i+1))+'mJy'
                                        print("Using "+ myfile[i]+" for making only a dirty image.")
                                        myimg = mywsclean(myfile[i],wsclean_params,myniter,i)   # tclean

                        else:
                                myniter=int(myniterstart*2**i) #myniterstart*(2**i)  # niter is doubled with every iteration int

                                if i < npal:
                                        mypap = 'p'       
                                else:
                                        mypap = 'ap'
#                                       
                                myimg = mywsclean(myfile[i],wsclean_params,myniter,i)   # wsclean
                                myimages.append(myimg)        # list of all the images created so far
                                flagresidual(myfile[i], use_gnet, myclipresid, join_scans, nproc)
                                # full list of gaintables
                                
                                if i < nscal:

                                        myctables = mygaincal_ap(myfile[i],myref,i,mypap,mysolint1,uvrascal,mygainspw2)
                                        mygt.append(myctables) 
                                        # myapplycal(myfile[i],mygt[i])
                                        myoutfile = mysplit(myfile[i], mygt[i], i, nproc)
                                        myfile.append(myoutfile)

                                        if i != 0:
                 
                                                print("Visibilities from the previous selfcal will be deleted.")
                                                myoldvis = myfile[i]    
                                                print("Deleting "+str(myoldvis))
                                                os.system('rm -rf '+str(myoldvis)+ '*')

                                elif i == nscal and nsubbands > 1:

                                        myoutfile = final_split(myfile[i], nproc)
                                        myimg = mywsclean(myoutfile,wsclean_params,myniter,i)
                                        flagresidual(myoutfile, use_gnet, myclipresid, join_scans, nproc)
                                        mypap = 'ap'
                                        myctables = mygaincal_ap(myoutfile,myref,i-1,mypap,mysolint1,uvrascal,mygainspw2)
                                        mygt.append(myctables)

                                        mysplit(myoutfile, mygt[i], i, nproc)

        return myfile, mygt, myimages

