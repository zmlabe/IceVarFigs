"""
HadCRUT4 Temperature anomalies (gridded)
Website   : https://crudata.uea.ac.uk/cru/data/temperature/
Author    : Zachary M. Labe
Date      : 15 June 2016
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import numpy as np
import datetime
import calendar as cal
from matplotlib.colors import ListedColormap, BoundaryNorm
import cmocean

### Define constants
directorydata = '/surtsey/zlabe/seaice_obs/seaice_reconstruct/'
directoryfigure = '/home/zlabe/Documents/Projects/Tests/SIC_Reconst/'
now = datetime.datetime.now()
month = now.month

years = np.arange(1914,2013+1,1)

data = Dataset(directorydata + 'G10010_SIBT1850_v1.1.nc')
lats = data.variables['latitude'][:]
lons = data.variables['longitude'][:]
sic = data.variables['seaice_conc'][768:,:,:]
data.close()

### Reshape concentration
sic = np.reshape(sic,(sic.shape[0]//12,12,lats.shape[0],lons.shape[0]))

### Slice month
sicmo = sic[:,8,:,:]
sicmo[np.where(sicmo < 0.1)] = np.nan
sicmo = sicmo/100.

### Define parameters (dark)
def setcolor(x, color):
     for m in x:
         for t in x[m][1]:
             t.set_color(color)

plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='white')
plt.rc('xtick',color='white')
plt.rc('ytick',color='white')
plt.rc('axes',labelcolor='white')
plt.rc('axes',facecolor='black')

## Plot global temperature anomalies
style = 'polar'

lon2,lat2 = np.meshgrid(lons,lats)

### Define figure
if style == 'ortho':
    m = Basemap(projection='ortho',lon_0=-90,
                lat_0=70,resolution='l',round=True)
elif style == 'polar':
    m = Basemap(projection='npstere',boundinglat=65,lon_0=270,resolution='l',round =True)

for i in range(sicmo.shape[0]):
    fig = plt.figure()
    ax = plt.subplot(111)
    for txt in fig.texts:
        txt.set_visible(False)
    
    var = sicmo[i,:,:]

    m.drawmapboundary(fill_color='k')
    m.drawlsmask(land_color='k',ocean_color='k')
    m.drawcoastlines(color='dimgrey',linewidth=0.8)
    
    # Make the plot continuous
    barlim = np.arange(0.1,1.1,1)
    
#    var, lons_cyclic = addcyclic(var, lons)
#    var, lons_cyclic = shiftgrid(180., var, lons_cyclic, start=False)
#    lon2d, lat2d = np.meshgrid(lons_cyclic, lats)
#    x, y = m(lon2d, lat2d)
    
    cs = m.contourf(lon2,lat2,var,
                    np.arange(0.1,1.1,0.05),extend='both',
                    alpha=1,latlon=True)
    
    cmap = cmocean.cm.tempo_r   
    cs.set_cmap(cmap)
    t = plt.annotate(r'\textbf{%s}' % years[i],textcoords='axes fraction',
                xy=(0,0), xytext=(-0.3,0.88),
            fontsize=50,color='darkgrey')
            
    t = plt.annotate(r'\textbf{GRAPHIC}: Zachary Labe (@ZLabe)',
                 textcoords='axes fraction',
            xy=(0,0), xytext=(-0.28,-0.01),
        fontsize=5,color='darkgrey')
    t = plt.annotate(r'\textbf{SOURCE}: https://nsidc.org/data/g10010',
                 textcoords='axes fraction',
            xy=(0,0), xytext=(-0.28,0.02),
        fontsize=5,color='darkgrey')
    t = plt.annotate(r'\textbf{DATA}: Walsh et al. [2015], Version 1',
             textcoords='axes fraction',
             xy=(0,0), xytext=(-0.28,0.05),
                fontsize=5,color='darkgrey')
    if i < 10:        
        plt.savefig(directoryfigure + 'icy_0%s.png' % i,dpi=300)
    else:
        plt.savefig(directoryfigure + 'icy_%s.png' % i,dpi=300)
        if i == 99:
            plt.savefig(directoryfigure + 'icy_99.png',dpi=300)
            plt.savefig(directoryfigure + 'icy_991.png',dpi=300)
            plt.savefig(directoryfigure + 'icy_992.png',dpi=300)
            plt.savefig(directoryfigure + 'icy_993.png',dpi=300)
            plt.savefig(directoryfigure + 'icy_994.png',dpi=300)
            plt.savefig(directoryfigure + 'icy_995.png',dpi=300)
            plt.savefig(directoryfigure + 'icy_996.png',dpi=300)
            plt.savefig(directoryfigure + 'icy_997.png',dpi=300)
            plt.savefig(directoryfigure + 'icy_998.png',dpi=300)
            plt.savefig(directoryfigure + 'icy_999.png',dpi=300)
    t.remove()