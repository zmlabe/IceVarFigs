"""
ERSSTv5 plot of 100 years

Website   : https://www1.ncdc.noaa.gov/pub/data/cmb/ersst/v5/netcdf//
Author    : Zachary M. Labe
Date      : 22 July 2017
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import numpy as np
import datetime
import calendar as cal
from matplotlib.colors import ListedColormap, BoundaryNorm
import nclcmaps as ncm

### Define constants
directorydata = '/surtsey/zlabe/ersst5/'
directoryfigure = '/home/zlabe/Documents/Projects/Tests/ersst5/Figures/'
now = datetime.datetime.now()
month = now.month

monthsq = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan'] 

years = np.arange(1992,2016+1,1)
months = np.arange(1,12+1,1)
sst = np.empty((25,12,89,180))
for i in range(years.shape[0]):
    for j in range(months.shape[0]):
        filename = directorydata + 'ersst.v5.%s%02d.nc' % (years[i],
                                                           months[j])
        
        data = Dataset(filename)
        lats = data.variables['lat'][:]
        lons = data.variables['lon'][:]
        sst[i,j,:,:] = data.variables['sst'][0,0,:,:]
        data.close()
    
    print('Completed: Read %s year!' % years[i])

### Slice month
sst[np.where(sst == -999)] = np.nan

sst = np.reshape(sst,(300,89,180))
yearsqq = np.repeat(years,12)

### Define parameters (dark)
def setcolor(x, color):
     for m in x:
         for t in x[m][1]:
             t.set_color(color)

plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='k')
plt.rc('xtick',color='white')
plt.rc('ytick',color='white')
plt.rc('axes',labelcolor='white')
plt.rc('axes',facecolor='black')

## Plot global temperature anomalies
style = 'global'

### Define figure
if style == 'ortho':
    m = Basemap(projection='ortho',lon_0=-90,
                lat_0=70,resolution='l',round=True)
elif style == 'polar':
    m = Basemap(projection='npstere',boundinglat=67,lon_0=270,resolution='l',round =True)
elif style == 'global':
#    m = Basemap(projection='robin',lon_0=0,resolution='l')
    m = Basemap(projection='moll',lon_0=0,resolution='l',area_thresh=10000)

for i in range(sst.shape[0]):
    fig = plt.figure()
    ax = plt.subplot(111)
    for txt in fig.texts:
        txt.set_visible(False)
    
    var = sst[i,:,:]

    m.drawmapboundary(fill_color='k')
    m.drawcoastlines(color='k',linewidth=0.4)
    
    # Make the plot continuous
    barlim = np.arange(0,31,5)
    
    var, lons_cyclic = addcyclic(var, lons)
    var, lons_cyclic = shiftgrid(180., var, lons_cyclic, start=False)
    lon2d, lat2d = np.meshgrid(lons_cyclic, lats)
    x, y = m(lon2d, lat2d)
    
    cs = plt.contourf(x,y,var,np.arange(-1.8,31.1,1),
                    extend='max')
#    cs1 = m.contour(x,y,var,np.arange(-1.8,36.1,2.5),linewidths=0.3,
#                   colors='darkgrey')
                    
    cmap = ncm.cmap('MPL_gnuplot')            
    cs.set_cmap(cmap)
    t = plt.annotate(r'\textbf{%s}' % yearsqq[i],textcoords='axes fraction',
            xy=(0,0), xytext=(0.34,1.03),
            fontsize=50,color='w',alpha=0.6)
#        t5 = plt.annotate(r'\textbf{%s}' % (years[i]),
#                         textcoords='axes fraction',
#                    xy=(0,0), xytext=(0.5,1.03),
#                fontsize=50,color='w',alpha=0.6)
            
    t1 = plt.annotate(r'\textbf{GRAPHIC}: Zachary Labe (@ZLabe)',
                 textcoords='axes fraction',
            xy=(0,0), xytext=(0.02,-0.167),
        fontsize=4.5,color='w',alpha=0.6)
    t2 = plt.annotate(r'\textbf{SOURCE}: https://www1.ncdc.noaa.gov/',
                 textcoords='axes fraction',
            xy=(0,0), xytext=(0.02,-0.197),
        fontsize=4.5,color='w',alpha=0.6)
    t3 = plt.annotate(r'\textbf{DATA}: NOAA ERSSTv5, Huang et al. (2017)',
             textcoords='axes fraction',
             xy=(0,0), xytext=(0.02,-0.227),
                fontsize=4.5,color='w',alpha=0.6)
    t4 = plt.annotate(r'\textbf{SEA SURFACE TEMPERATURES}',
         textcoords='axes fraction',
         xy=(0,0), xytext=(0.24,-0.036),fontsize=13,color='w',alpha=0.6)
                
    m.fillcontinents(color='k')
                
    cbar = plt.colorbar(cs,drawedges=False,orientation='horizontal',
                        pad = 0.04,fraction=0.035)
    cbar.set_ticks(barlim)
    cbar.set_ticklabels(list(map(str,barlim)))  
    cbar.set_label(r'\textbf{$\bf{^\circ}$\textbf{C}}',fontsize=13,
                   color='w')
    cbar.ax.tick_params(axis='x', size=.001)
    cbar.ax.tick_params(labelsize=6) 
    
    plt.subplots_adjust(bottom=0.2)
    
    if i < 10:        
        plt.savefig(directoryfigure + 'sstq_00%s.png' % (i),
                    dpi=200)
    elif i < 100:
        plt.savefig(directoryfigure + 'sstq_0%s.png' % (i),
            dpi=200)
    else:
        plt.savefig(directoryfigure + 'sstq_%s.png' % (i),
                    dpi=200)
    t.remove()
    t1.remove()
    t2.remove()
    t3.remove()
    t4.remove()