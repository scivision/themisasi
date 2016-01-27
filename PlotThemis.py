#!/usr/bin/env python3

from themisasi.readthemis import readthemis,plotthemis,calthemis

def playThemis(fn,t,site,odir):
    plotthemis(imgs,t,site,odir)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description = ' reads THEMIS GBO ASI CDF files and plays high speed video')
    p.add_argument('f',help='file to play')
    p.add_argument('-c','--cal',help='az/el cal file to real')
    p.add_argument('-t','--treq',help='time requested',nargs=2)
    p.add_argument('-o','--odir',help='write video to this directory')
    p = p.parse_args()

    if p.cal:
        imgs,t,site = readthemis(p.f,p.treq,p.odir)
        altfiducial(imgs,t) #paint HiST field of view onto Themis


    try:
        imgs,t = playThemis(p.f,t,site,p.odir)
    except KeyboardInterrupt:
        pass