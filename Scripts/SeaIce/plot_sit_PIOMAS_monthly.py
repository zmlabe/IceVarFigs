"""
Author    : Zachary M. Labe
Date      : 23 August 2016
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import datetime
import calendar as cal
import matplotlib.colors as c

#### Define constants
directory = '/home/zlabe/Documents/Projects/Tests/Piomas/Monthly/'
directorydata = '/home/zlabe/surt/seaice_obs/PIOMAS/Thickness/'
directorydata2 = '/home/zlabe/surt/seaice_obs/PIOMAS/' 
directorydata3 = '/home/zlabe/Documents/Projects/Tests/SIV_animate/Data/' 
now = datetime.datetime.now()
month = now.month
years = np.arange(1979,2018,1)
months = np.arange(1,13,1)

def readPiomas(directory,vari,years,thresh):
    """
    Reads binary PIOMAS data
    """
    
    ### Retrieve Grid
    grid = np.genfromtxt(directory + 'grid.txt')
    grid = np.reshape(grid,(grid.size))  
    
    ### Define Lat/Lon
    lon = grid[:grid.size//2]   
    lons = np.reshape(lon,(120,360))
    lat = grid[grid.size//2:]
    lats = np.reshape(lat,(120,360))
    
    ### Call variables from PIOMAS
    if vari == 'thick':
        files = 'heff'
        directory = directory + 'Thickness/'
    elif vari == 'sic':
        files = 'area'
        directory = directory + 'SeaIceConcentration/'
    elif vari == 'snow':
        files = 'snow'
        directory = directory + 'SnowCover/'   
    elif vari == 'oflux':
        files = 'oflux'
        directory = directory + 'OceanFlux/'
    
    ### Read data from binary into numpy arrays
    var = np.empty((len(years),12,120,360))
    for i in range(len(years)):
        data = np.fromfile(directory + files + '_%s.H' % (years[i]),
                           dtype = 'float32')

    ### Reshape into [year,month,lat,lon]
        months = int(data.shape[0]/(120*360))
        if months != 12:
            lastyearq = np.reshape(data,(months,120,360))
            emptymo = np.empty((12-months,120,360))
            emptymo[:,:,:] = np.nan
            lastyear = np.append(lastyearq,emptymo,axis=0)
            var[i,:,:,:] = lastyear
        else:
            dataq = np.reshape(data,(12,120,360))        
            var[i,:,:,:] = dataq
    
    ### Mask out threshold values
    var[np.where(var <= thresh)] = np.nan

    print('Completed: Read "%s" data!' % (vari))   
    
    return lats,lons,var
lats,lons,sit = readPiomas(directorydata2,'thick',years,0.1)

### Read SIV data
years2,aug = np.genfromtxt(directorydata3 + 'monthly_piomas.txt',
                           unpack=True,delimiter='',usecols=[0,9])
                           
climyr = np.where((years2 >= 1981) & (years2 <= 2010))[0]  
clim = np.nanmean(aug[climyr])  

def colormapSIT():
    cmap1 = plt.get_cmap('BuPu')
    cmap2 = plt.get_cmap('RdPu_r')
    cmap3 = plt.get_cmap('gist_heat_r')
    cmaplist1 = [cmap1(i) for i in range(30,cmap1.N-10)]
    cmaplist2 = [cmap2(i) for i in range(15,cmap2.N)]
    cmaplist3 = [cmap3(i) for i in range(cmap2.N-15)]
    cms_sit = c.ListedColormap(cmaplist1 + cmaplist2 + cmaplist3)
    return cms_sit

### Select month
sit = sit[:,8,:,:]

### Adjust axes in time series plots 
def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 5))
        else:
            spine.set_color('none')  
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        ax.xaxis.set_ticks([])

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

### Define figure
if style == 'ortho':
    m = Basemap(projection='ortho',lon_0=-90,
                lat_0=70,resolution='l',round=True)
elif style == 'polar':
    m = Basemap(projection='npstere',boundinglat=67,lon_0=270,resolution='l',round =True)

for i in range(aug.shape[0]):
    fig = plt.figure()
    ax = plt.subplot(111)
    for txt in fig.texts:
        txt.set_visible(False)
    
    var = sit[i,:,:]
    m.drawmapboundary(fill_color='k')
    m.drawlsmask(land_color='k',ocean_color='k')
    m.drawcoastlines(color='mediumseagreen',linewidth=0.4)
    
    # Make the plot continuous
    barlim = np.arange(0,9,1)
    
#    cmap = colormapSIT()
    cmap = colormapSIT()
    cs = m.contourf(lons,lats,var,
                    np.arange(0,7.1,0.25),extend='max',
                    alpha=1,latlon=True,cmap=cmap)
                
    if i >= 38:
        ccc = 'mediumseagreen'
    else:
        ccc = 'w'
    t1 = plt.annotate(r'\textbf{%s}' % years[i],textcoords='axes fraction',
                xy=(0,0), xytext=(-0.45,0.85),
            fontsize=50,color=ccc)
            
    t2 = plt.annotate(r'\textbf{GRAPHIC}: Zachary Labe (@ZLabe)',
                 textcoords='axes fraction',
            xy=(0,0), xytext=(-0.43,-0.06),
        fontsize=4.5,color='darkgrey')
    t3 = plt.annotate(r'\textbf{SOURCE}: http://psc.apl.washington.edu/zhang/IDAO/data.html',
                 textcoords='axes fraction',
            xy=(0,0), xytext=(-0.43,-0.03),
        fontsize=4.5,color='darkgrey')
    t4 = plt.annotate(r'\textbf{DATA}: PIOMAS v2.1 (Zhang and Rothrock, 2003) (\textbf{September})',
             textcoords='axes fraction',
             xy=(0,0), xytext=(-0.43,0.0),
                fontsize=4.5,color='darkgrey')
                
    cbar = m.colorbar(cs,drawedges=True,location='bottom',pad = 0.14,size=0.07)
    ticks = np.arange(0,8,1)
    cbar.set_ticks(barlim)
    cbar.set_ticklabels(list(map(str,barlim)))
    cbar.set_label(r'\textbf{Sea Ice Thickness (m)}',fontsize=10,
                             color='darkgrey')
    cbar.ax.tick_params(axis='x', size=.0001)
    cbar.ax.tick_params(labelsize=7) 

###########################################################################
###########################################################################  
    ### Create subplot         
    a = plt.axes([.24, .27, .08, .4], axisbg='k')
    
    N = 1
    ind = np.linspace(N,0.2,1)
    width = .33
    
    meansiv = np.nanmean(aug)

    rects = plt.bar(ind,[aug[i]],width,zorder=2)
    
#    plt.plot(([meansiv]*2),zorder=1)    
    
    rects[0].set_color('powderblue')
    if i == 38:
        rects[0].set_color('mediumseagreen')

    adjust_spines(a, ['left', 'bottom'])
    a.spines['top'].set_color('none')
    a.spines['right'].set_color('none')
    a.spines['left'].set_color('none')
    a.spines['bottom'].set_color('none')
    plt.setp(a.get_xticklines()[0:-1],visible=False)
    a.tick_params(labelbottom='off')
    a.tick_params('both',length=4,width=2,which='major')
    
    plt.yticks(np.arange(0,36,5),map(str,np.arange(0,36,5)))
    plt.ylabel(r'\textbf{Sea Ice Volume [$\times$1000 km$^{3}$]}',
           fontsize=8,color='darkgrey')
           
    fig.subplots_adjust(right=1.1)
    
###########################################################################
###########################################################################
         
    if i < 10:        
        plt.savefig(directory + 'icy_0%s.png' % i,dpi=300)
    else:
        plt.savefig(directory + 'icy_%s.png' % i,dpi=300)
        if i == 38:
            plt.savefig(directory + 'icy_38.png',dpi=300)
            plt.savefig(directory + 'icy_39.png',dpi=300)
            plt.savefig(directory + 'icy_40.png',dpi=300)
            plt.savefig(directory + 'icy_41.png',dpi=300)
            plt.savefig(directory + 'icy_42.png',dpi=300)
            plt.savefig(directory + 'icy_43.png',dpi=300)
            plt.savefig(directory + 'icy_44.png',dpi=300)
            plt.savefig(directory + 'icy_45.png',dpi=300)
            plt.savefig(directory + 'icy_46.png',dpi=300)
            plt.savefig(directory + 'icy_47.png',dpi=300)
            plt.savefig(directory + 'icy_48.png',dpi=300)
            plt.savefig(directory + 'icy_49.png',dpi=300)
            plt.savefig(directory + 'icy_50.png',dpi=300)
            plt.savefig(directory + 'icy_51.png',dpi=300)
    t1.remove()
    t2.remove()
    t3.remove()
    t4.remove()
