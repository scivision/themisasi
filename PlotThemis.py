#!/usr/bin/env python3

from themisasi.readthemis import plotthemis,readthemis,altfiducial

def playThemis(fn,t,site,odir):
    plotthemis(imgs,t,site,odir)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description = ' reads THEMIS GBO ASI CDF files and plays high speed video')
    p.add_argument('asifn',help='ASI file to play')
    p.add_argument('--asical',help='ASI az/el cal file to read')
    p.add_argument('--ocal',help='other camera (narrow FOV) cal file')
    p.add_argument('-t','--treq',help='time requested',nargs=2)
    p.add_argument('-o','--odir',help='write video to this directory')
    p = p.parse_args()

    if p.asical:
        altfiducial(p.asifn,p.asical,p.ocal,p.treq,p.odir) #paint HiST field of view onto Themis
    else:
        imgs,t,site = readthemis(p.asifn,p.treq,p.odir)
        try:
            imgs,t = playThemis(p.asifn,t,site,p.odir)
        except KeyboardInterrupt:
            pass