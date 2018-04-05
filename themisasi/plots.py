from pathlib import Path
import xarray
import numpy as np
from matplotlib.pyplot import figure,draw,pause
from matplotlib.colors import LogNorm


def jointazel(w0:xarray.Dataset, ofn:Path=None, ttxt:str=''):

    fg,axs = plotazel(w0, ttxt)

    overlayrowcol(axs[0], w0['row1'], w0['col1'])
    overlayrowcol(axs[1], w0['row1'], w0['col1'])

    if ofn:
        ofn = Path(ofn).expanduser()
        print('saving',ofn)
        fg.savefig(ofn,bbox_inches='tight',dpi=100)


def plotazel(data:xarray.Dataset, ttxt:str=''):
    fg = figure(figsize=(12,6))
    ax = fg.subplots(1,2, sharey = True)

    fg.suptitle(data.filename + ' ' + ttxt)

    c = ax[0].contour(data['az'].x, data['az'].y, data['az'])
    ax[0].clabel(c, fmt='%0.1f')
    ax[0].set_title('azimuth')
    ax[0].set_xlabel('x-pixels')
    ax[0].set_ylabel('y-pixels')


    c = ax[1].contour(data['el'].x, data['el'].y, data['el'])
    ax[1].clabel(c, fmt='%0.1f')
    ax[1].set_title('elevation')
    ax[1].set_xlabel('x-pixels')

    return fg,ax


def overlayrowcol(ax,rows,cols):
    """
    plot FOV outline onto image via the existing axis "ax"

    inputs:
    ax: existing plot axis to overlay lines outlining FOV
    rows,cols: indices to plot
    """

    if rows is None or cols is None:
        return


    if len(rows) == 1 or isinstance(rows,(np.ndarray,xarray.DataArray)) and rows.ndim==1:
        ax.scatter(cols, rows, color='g',alpha=0.5, marker='.')
        return

# %%
def plotasi(data:xarray.Dataset, ofn:Path=None):
    """
    rows,cols expect lines to be along rows Nlines x len(line)
    list of 1-D arrays or 2-D array
    """
    if ofn:
        ofn = Path(ofn).expanduser()
        odir = ofn.parent


    fg = figure()
    ax = fg.gca()

    hi = ax.imshow(data['imgs'][0], cmap='gray',origin='lower',norm=LogNorm(),interpolation='none') # priming
    ttxt = f'Themis ASI {data.site}\n' # FOV vs. HST0,HST1: green,red '
    ht = ax.set_title(ttxt,color='g')
    ax.set_xlabel('x-pixels')
    ax.set_ylabel('y-pixels')
    ax.autoscale(True,tight=True)
    ax.grid(False)
#%% plot narrow FOV outline
    if 'imgs2' in data:
        overlayrowcol(ax, data)
#%% play video
    for im in data['imgs']:
        ts = im.time.values.astype(str)[:-6]
        hi.set_data(im)
        ht.set_text(ttxt+ ts)
        draw(); pause(0.01)
        if ofn:
            fn = odir / (ofn.stem + ts + ofn.suffix)
            print('saving',fn,end='\r')
            fg.savefig(fn, bbox_inches='tight', facecolor='k')

