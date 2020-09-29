"""
Plot sea ice concentration from last 100 years using the Walsh reconstruction
for version 2

Website   : https://nsidc.org/data/g10010
Author    : Zachary M. Labe
Date      : 2 June 2020
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
directorydata = './Data/'
directoryfigure = './Figures/'
now = datetime.datetime.now()
month = now.month

### Input years
years = np.arange(1918,2017+1,1)

### Read data from server
data = Dataset(directorydata + 'G10010_SIBT1850_v2.0.nc')
lats = data.variables['latitude'][:]
lons = data.variables['longitude'][:]
sic = data.variables['seaice_conc'][-1200:,:,:]
data.close()

### Reshape concentration
sic = np.reshape(sic,(sic.shape[0]//12,12,lats.shape[0],lons.shape[0]),)

### Slice month
sicmo = sic[:,8,:,:].astype(np.float64)
sicmo[np.where(sicmo == 0)] = np.nan
sicmo[np.where(sicmo > 100)] = np.nan
sicmo = sicmo/100.

###############################################################################
###############################################################################
###############################################################################
### Plot figure

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

### Create 2d arrays of latitude and longitude
lon2,lat2 = np.meshgrid(lons,lats)

### Define figure
if style == 'ortho':
    m = Basemap(projection='ortho',lon_0=-90,
                lat_0=70,resolution='l',round=True)
elif style == 'polar':
    m = Basemap(projection='npstere',boundinglat=50,lon_0=270,
                resolution='l',round =True,area_thresh=10000)

for i in range(sicmo.shape[0]): # 100 years
    fig = plt.figure()
    ax = plt.subplot(111)
    
    ### Hide data for transparent background
    for txt in fig.texts:
        txt.set_visible(False)
    
    ### Loop through 100 years
    var = sicmo[i,:,:]

    ### Create polar map
    m.drawmapboundary(fill_color='k',zorder=1)
    m.drawlsmask(land_color='k',ocean_color='k')
    
    # Make the plot continuous
    barlim = np.arange(0.1,1.1,1)
    
    ### Plot filled contours
    cs = m.contourf(lon2,lat2,var,
                    np.arange(0.1,1.1,0.05),extend='both',
                    alpha=1,latlon=True,zorder=2)
    
    ### Color map
    cmap = cmocean.cm.ice
    cs.set_cmap(cmap)
    
    ### Mask land
    m.fillcontinents(color='k')
    m.drawcoastlines(color='darkred',linewidth=0.6)
    
    ### Fill page
    plt.tight_layout()
    
    ### Data information
    t = plt.annotate(r'\textbf{%s}' % years[i],textcoords='axes fraction',
                xy=(0,0), xytext=(-0.06,0.88),
            fontsize=50,color='w',ha='center',va='center')
            
    t = plt.annotate(r'\textbf{GRAPHIC}: Zachary Labe (@ZLabe)',
                 textcoords='axes fraction',
            xy=(0,0), xytext=(-0.28,-0.01),
        fontsize=5,color='darkgrey')
    t = plt.annotate(r'\textbf{SOURCE}: https://nsidc.org/data/g10010',
                 textcoords='axes fraction',
            xy=(0,0), xytext=(-0.28,0.03),
        fontsize=5,color='darkgrey')
    t = plt.annotate(r'\textbf{REFERENCE}: Walsh et al. [2016], Version 2',
             textcoords='axes fraction',
             xy=(0,0), xytext=(-0.28,0.01),
                fontsize=5,color='darkgrey')
    t = plt.annotate(r'\textbf{DATA}: Sea Ice Concentration \textbf{[SEPTEMBER}',
             textcoords='axes fraction',
             xy=(0,0), xytext=(-0.28,0.05),
                fontsize=5,color='darkgrey')
    
    ### Save images for creating GIF using ImageMagick
    if i < 10:        
        plt.savefig(directoryfigure + 'Walsh_v2_0%s.png' % i,dpi=300)
    else:
        plt.savefig(directoryfigure + 'Walsh_v2_%s.png' % i,dpi=300)
        if i == 99:
            plt.savefig(directoryfigure + 'Walsh_v2_99.png',dpi=300)
            plt.savefig(directoryfigure + 'Walsh_v2_991.png',dpi=300)
            plt.savefig(directoryfigure + 'Walsh_v2_992.png',dpi=300)
            plt.savefig(directoryfigure + 'Walsh_v2_993.png',dpi=300)
            plt.savefig(directoryfigure + 'Walsh_v2_994.png',dpi=300)
            plt.savefig(directoryfigure + 'Walsh_v2_995.png',dpi=300)
            plt.savefig(directoryfigure + 'Walsh_v2_996.png',dpi=300)
            plt.savefig(directoryfigure + 'Walsh_v2_997.png',dpi=300)
            plt.savefig(directoryfigure + 'Walsh_v2_998.png',dpi=300)
            plt.savefig(directoryfigure + 'Walsh_v2_999.png',dpi=300)
    t.remove()
