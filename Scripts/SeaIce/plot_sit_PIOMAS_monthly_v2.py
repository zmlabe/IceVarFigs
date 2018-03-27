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
import cmocean

### Define constants
### Directory and time
directoryfigure = '/home/zlabe/Documents/Projects/IceVarFigs/Figures/' 
directorydata = '/home/zlabe/Documents/Projects/IceVarFigs/Data/'  
now = datetime.datetime.now()
month = now.month
years = np.arange(1979,2019,1)
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
                           unpack=True,delimiter='',usecols=[0,2])
                           
climyr = np.where((years2 >= 1981) & (years2 <= 2010))[0]  
clim = np.nanmean(aug[climyr])  

### Select month
sit = sit[:,1,:,:]

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
plt.rc('axes',edgecolor='k')
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
    m.drawcoastlines(color='aqua',linewidth=0.7)
    
    # Make the plot continuous
    barlim = np.arange(0,6,1)
    
    cmap = cmocean.cm.thermal
    cs = m.contourf(lons,lats,var,
                    np.arange(0,5.1,0.25),extend='max',
                    alpha=1,latlon=True,cmap=cmap)
                
    if i >= 39:
        ccc = 'slateblue'
    else:
        ccc = 'w'
    t1 = plt.annotate(r'\textbf{%s}' % years[i],textcoords='axes fraction',
                xy=(0,0), xytext=(-0.54,0.815),
            fontsize=50,color=ccc)
            
    t2 = plt.annotate(r'\textbf{GRAPHIC}: Zachary Labe (@ZLabe)',
                      textcoords='axes fraction',
                      xy=(0,0), xytext=(1.02,-0.0),
                      fontsize=4.5,color='darkgrey',rotation=90,va='bottom')
    t3 = plt.annotate(r'\textbf{SOURCE}: http://psc.apl.washington.edu/zhang/IDAO/data.html',
                      textcoords='axes fraction',
                      xy=(0,0), xytext=(1.05,-0.0),
                      fontsize=4.5,color='darkgrey',rotation=90,va='bottom')
    t4 = plt.annotate(r'\textbf{DATA}: PIOMAS v2.1 (Zhang and Rothrock, 2003) (\textbf{February})',
                      textcoords='axes fraction',
                      xy=(0,0), xytext=(1.08,-0.0),
                      fontsize=4.5,color='darkgrey',rotation=90,va='bottom')
                
    cbar = m.colorbar(cs,drawedges=True,location='bottom',pad = 0.14,size=0.07)
    ticks = np.arange(0,8,1)
    cbar.set_ticks(barlim)
    cbar.set_ticklabels(list(map(str,barlim)))
    cbar.set_label(r'\textbf{SEA ICE THICKNESS [m]}',fontsize=10,
                             color='darkgrey')
    cbar.ax.tick_params(axis='x', size=.0001)
    cbar.ax.tick_params(labelsize=7) 

###########################################################################
###########################################################################  
    ### Create subplot         
    a = plt.axes([.2, .225, .08, .4], axisbg='k')
    
    N = 1
    ind = np.linspace(N,0.2,1)
    width = .33
    
    meansiv = np.nanmean(aug)

    rects = plt.bar(ind,[aug[i]],width,zorder=2)
    
#    plt.plot(([meansiv]*2),zorder=1)    
    
    rects[0].set_color('aqua')
    if i == 39:
        rects[0].set_color('slateblue')

    adjust_spines(a, ['left', 'bottom'])
    a.spines['top'].set_color('none')
    a.spines['right'].set_color('none')
    a.spines['left'].set_color('none')
    a.spines['bottom'].set_color('none')
    plt.setp(a.get_xticklines()[0:-1],visible=False)
    a.tick_params(labelbottom='off')
    a.tick_params(labelleft='off')
    a.tick_params('both',length=0,width=0,which='major')
    
    plt.yticks(np.arange(0,31,5),map(str,np.arange(0,31,5)))
    plt.xlabel(r'\textbf{SEA ICE VOLUME [km$^{3}$]}',
           fontsize=10,color='darkgrey',labelpad=1)
    
    for rectq in rects:
        height = rectq.get_height()
        cc = 'darkgrey'
        if i == 39:
            cc ='slateblue'
        plt.text(rectq.get_x() + rectq.get_width()/2.0, 
                 height+1, r'\textbf{%s}' % format(int(height*1000),",d"), 
                 ha='center', va='bottom',color=cc,fontsize=20)
           
    fig.subplots_adjust(right=1.1)
    
###########################################################################
###########################################################################
         
    if i < 10:        
        plt.savefig(directory + 'icy_0%s.png' % i,dpi=300)
    else:
        plt.savefig(directory + 'icy_%s.png' % i,dpi=300)
        if i == 39:
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
