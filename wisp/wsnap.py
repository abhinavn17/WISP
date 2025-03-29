import os
from casatools import msmetadata
from argparse import ArgumentParser
import subprocess
from wisp.snapshot_join import snapshot_join
import glob

def main():

    parser = ArgumentParser(description='A WISP module that does snapshot imaging')

    parser.add_argument('msfile', type=str, help='Measurement set file to image')

    parser.add_argument('-j', '--nthreads', type=int, default=16, help='Number of threads to use')

    parser.add_argument('-s', '--size', type=int, nargs=2, default=[512, 512], help='Image size')

    parser.add_argument('-c', '--cell', type=float, default=1, help='Cell size in arcsec')

    parser.add_argument('-d', '--delta', type=int, default=1, help='Interval between snapshots in integers of integration time')

    parser.add_argument('-n', '--niter', type=int, default=5000, help='Number of iterations')

    args = parser.parse_args()

    msfile, nprocs, imsize, cell, delta, niter = args.msfile, args.nthreads, args.size, args.cell, args.delta, args.niter

    msfile = os.path.abspath(msfile)

    workdir = msfile.split('/')[:-1]

    workdir = '/'.join(workdir)

    msfilename = msfile.split('/')[-1].split('.')[0]

    outdir = f'{workdir}/{msfilename}_snapshot'

    if not os.path.exists(outdir):
        os.makedirs(outdir)
        run_imaging = True
    else:
        ask = input(f'{outdir} already exists. Do you want to overwrite it? (y/n): ')
        if ask == 'y':
            os.system(f'rm -rf {outdir}')
            os.makedirs(outdir)
            run_imaging = True
        else:
            run_imaging = False

    msmd = msmetadata()
    msmd.open(msfile)

    nrows = msmd.nrows()    
    nbaselines = msmd.nbaselines()
    
    integration_time = msmd.timesforfield(0)[1] - msmd.timesforfield(0)[0]

    ntimes = nrows // nbaselines

    msmd.close()


    if run_imaging:

        nsteps = ntimes // delta

        wsclean_command = ['wsclean', '-j', f'{nprocs}',  '-size', f'{imsize[0]}', f'{imsize[1]}', '-scale', f'{cell}asec', '-weight', 'uniform', '-niter', f'{niter}', '-mgain', '0.8', '-auto-mask', '3', '-auto-threshold', '0.3', '-intervals-out', f'{nsteps}', '-name', f'{outdir}/{msfilename}', msfile]

        subprocess.run(wsclean_command)

        for file in glob.glob(f'{outdir}/*-dirty.fits'):
            os.remove(file)
        for file in glob.glob(f'{outdir}/*-psf.fits'):
            os.remove(file)
        for file in glob.glob(f'{outdir}/*-model.fits'):
            os.remove(file)
        for file in glob.glob(f'{outdir}/*-residual.fits'):
            os.remove(file)

    snapshot_join(outdir, f'{workdir}/{msfilename}_snapshot.fits', integration_time*delta)

if __name__ == '__main__':

    main()
