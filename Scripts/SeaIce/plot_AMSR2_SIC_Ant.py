"""
Plots JAXA AMSR2 3.125 km (UHH-Processed) Sea Ice Concentration Data
 
Source : http://osisaf.met.no/p/ice/
Author : Zachary Labe
Date : 27 February 2017
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import urllib.request as UL
import numpy as np
import datetime
import gzip
import cmocean

### Directory and time
directory = './Data/'
directoryfigure = './Figures/'
now = datetime.datetime.now()
currentyr = str(now.year)
    
for i in range(14,31): ### enter days
    currentdy = str(i+1)
    currentmn = '08'
    if int(currentdy) < 10:
        currentdy = '0' + currentdy
    currentyr = str(now.year)
    currenttime = currentmn + '_' + str(currentdy) + '_' + currentyr
    titletime = currentmn + '/' + str(currentdy) + '/' + currentyr
    print('\n' 'Current Time = %s' '\n' % titletime)
    
    ### Pick data set    
    url = 'ftp://ftp-projects.cen.uni-hamburg.de/seaice/AMSR2/3.125km/'
    filename = 'Ant_%s%s%s_res3.125_pyres.nc.gz' % (currentyr,currentmn,currentdy)
    filenameout = 'Arc_AMSR2_SIC.nc'
    UL.urlretrieve(url+filename, directory + filename)
    inF = gzip.open(directory + filename, 'rb')
    outF = open(directory + filenameout, 'wb')
    outF.write( inF.read() )
    inF.close()
    outF.close()
    
    data = Dataset(directory + filenameout)
    ice = data.variables['sea_ice_concentration'][:]
    lat = data.variables['latitude'][:]    
    lon = data.variables['longitude'][:]
    data.close()
    
    ice = np.asarray(np.squeeze(ice/100.))
    
    print('Completed: Data read!')
        
    ice[np.where(ice <= 0.20)] = np.nan
    ice[np.where((ice >= 0.999) & (ice <= 1))] = 0.999
    ice[np.where(ice > 1)] = np.nan
    ice = ice*100.
    
    print('Completed: Ice masked!')
    
    plt.rc('text',usetex=True)
    plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
    plt.rc('savefig',facecolor='black')
    plt.rc('axes',edgecolor='darkgrey')
    plt.rc('xtick',color='darkgrey')
    plt.rc('ytick',color='darkgrey')
    plt.rc('axes',labelcolor='darkgrey')
    plt.rc('axes',facecolor='black')
    
    def setcolor(x, color):
         for m in x:
             for t in x[m][1]:
                 t.set_color(color)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ### Enter lat/lon
    m = Basemap(projection='spstere',boundinglat=-56,lon_0=180,resolution='l',
            round=True,area_thresh=10000)
    m.drawcoastlines(color = 'r',linewidth=2.5)
    m.drawmapboundary(color='k')
    m.drawlsmask(land_color='k',ocean_color='k')
    
    cs = m.contourf(lon,lat,ice[:,:],np.arange(20,100.01,2),extend='min',latlon=True)
     
    cmap = cmocean.cm.ice     
    cs.set_cmap(cmap)
    
    m.fillcontinents(color='k')
    
    cbar = m.colorbar(cs,location='right',pad = 0.2)
    cbar.outline.set_edgecolor('k')
    barlim = np.arange(20,101,10)
    cbar.set_ticks(barlim)
    cbar.set_ticklabels(list(map(str,barlim)) )
    cbar.set_label(r'\textbf{Concentration (\%)}',fontsize=13,
                             alpha=1,color='darkgrey')
    cbar.ax.tick_params(axis='y', size=.01)
    
    fig.suptitle(r'\textbf{ANTARCTIC SEA ICE -- %s}' % titletime,
                 fontsize=22,color='darkgrey',alpha=1)
                             
    plt.annotate(r'\textbf{DATA:} AMSR2 3.125 km (JAXA/Uni Hamburg-Processing)',xy=(250,100),
                 xycoords='figure pixels',color='darkgrey',fontsize=6,
                 alpha=1,rotation=0) 
    plt.annotate(r'\textbf{SOURCE:} http://icdc.cen.uni-hamburg.de/daten/cryosphere.html',xy=(250,80),
                 xycoords='figure pixels',color='darkgrey',fontsize=6,
                 alpha=1,rotation=0) 
    plt.annotate(r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',xy=(250,60),
                 xycoords='figure pixels',color='darkgrey',fontsize=6,
                 alpha=1,rotation=0)
                
    plt.tight_layout()
    fig.subplots_adjust(top=0.89)
    
    print('Completed: Figure plotted!')
    plt.savefig(directoryfigure + 'seaiceconc_%s.png' % currenttime, dpi=300)
    
print('Completed: Script done!')