"""
Plot ENSO from 2015-2018 using daily oisstv2

Data : 18 March 2018
Author : Zachary M. Labe

"""

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import datetime
import cmocean

### Directory and time
directoryfigure = '/home/zlabe/Documents/Projects/IceVarFigs/Figures/' 
directorydata = '/home/zlabe/Documents/Projects/IceVarFigs/Data/'   
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday

data = Dataset(directorydata + 'sst.day.anom.2015.v2.nc')
sst15 = data.variables['anom'][180:]
data.close()

data = Dataset(directorydata + 'sst.day.anom.2016.nc')
sst16 = data.variables['anom'][:]
data.close()

data = Dataset(directorydata + 'sst.day.anom.2017.nc')
sst17 = data.variables['anom'][:]
data.close()

data = Dataset(directorydata + 'sst.day.anom.2018.nc')
sst18 = data.variables['anom'][:]
lat = data.variables['lat'][:]
lon = data.variables['lon'][:]
data.close()

lon2,lat2 = np.meshgrid(lon,lat)

sstnn = np.append(sst15,sst16,axis=0)
sstn = np.append(sstnn,sst17,axis=0)
sst = np.append(sstn,sst18,axis=0)

def groupedAvg(myArray, N):
    result = np.cumsum(myArray, 0)[N-1::N]/float(N)
    result[1:] = result[1:] - result[:-1]
    return result
smooth = groupedAvg(sst,10) # 10-day mean

year15 = np.repeat(np.array([2015]),18)
year16 = np.repeat(np.array([2016]),36)
year17 = np.repeat(np.array([2017]),36)
year18 = np.repeat(np.array([2018]),9)

year1 = np.append(year15,year16)
year2 = np.append(year1,year17)
years = np.append(year2,year18)

###########################################################################
###########################################################################
###########################################################################
### Create plot
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='dimgrey')
plt.rc('xtick',color='dimgrey')
plt.rc('ytick',color='dimgrey')
plt.rc('axes',labelcolor='white')
plt.rc('axes',facecolor='black')

def plot_rec(bmap, lower_left, upper_left, lower_right, upper_right):
    xs = [lower_left[0], upper_left[0],
          upper_right[0],lower_right[0],
          lower_left[0]]
    ys = [lower_left[1], upper_left[1],
          upper_right[1],lower_right[1],
          lower_left[1]]
    if np.nanmax(xs)==240:
        l=3.3
        aa = 0.8
    else:
        l=1.4
        aa = 0.6
    bmap.plot(xs, ys, latlon = True,color='k',alpha=aa,linewidth=l)
    
llcrnrlon = 270
urcrnrlon =  280
llcrnrlat =  -10
urcrnrlat =  0
lower_left1 = (llcrnrlon, llcrnrlat)
lower_right1= (urcrnrlon, llcrnrlat)
upper_left1 = (llcrnrlon, urcrnrlat)
upper_right1= (urcrnrlon, urcrnrlat)

llcrnrlon = 210
urcrnrlon =  270
llcrnrlat =  -5
urcrnrlat =  5
lower_left2 = (llcrnrlon, llcrnrlat)
lower_right2= (urcrnrlon, llcrnrlat)
upper_left2 = (llcrnrlon, urcrnrlat)
upper_right2= (urcrnrlon, urcrnrlat)

llcrnrlon = 190
urcrnrlon =  240
llcrnrlat =  -5
urcrnrlat =  5
lower_left3 = (llcrnrlon, llcrnrlat)
lower_right3= (urcrnrlon, llcrnrlat)
upper_left3 = (llcrnrlon, urcrnrlat)
upper_right3= (urcrnrlon, urcrnrlat)

llcrnrlon = 160
urcrnrlon =  210
llcrnrlat =  -5
urcrnrlat =  5
lower_left4 = (llcrnrlon, llcrnrlat)
lower_right4= (urcrnrlon, llcrnrlat)
upper_left4 = (llcrnrlon, urcrnrlat)
upper_right4= (urcrnrlon, urcrnrlat)

barlim=np.arange(-3,4,3)
for i in range(smooth.shape[0]):

    fig = plt.figure(figsize=(9,5))
    ax = plt.subplot(111)
    
    m = Basemap(projection='merc',llcrnrlat=-17,urcrnrlat=17,\
                llcrnrlon=180,urcrnrlon=290,resolution='l')
    m.drawcoastlines()
    m.fillcontinents(color='k',lake_color='k')
    m.drawmapboundary(fill_color='k')
    
    cs=m.contourf(lon2,lat2,smooth[i],np.arange(-3,3.02,0.1),latlon=True,
                  extend='both')
    cs.set_cmap(cmocean.cm.balance)
    
    cbar = plt.colorbar(cs,drawedges=False,orientation='horizontal',
                        pad = 0.04,fraction=0.047,extend='both')
    cbar.set_ticks(barlim)
    cbar.set_ticklabels(list(map(str,barlim)))  
    cbar.ax.tick_params(axis='x', size=.001)
    cbar.ax.tick_params(labelsize=13) 
    cbar.set_label(r'\textbf{%s}' % years[i],color='darkgrey',
                   fontsize=30)
    
    ### Draw ENSO boxes
    plot_rec(m, lower_left1, upper_left1, lower_right1, upper_right1)
    plot_rec(m, lower_left2, upper_left2, lower_right2, upper_right2)
    plot_rec(m, lower_left3, upper_left3, lower_right3, upper_right3)
    plot_rec(m, lower_left4, upper_left4, lower_right4, upper_right4)
    
    plt.title(r'\textbf{SEA SURFACE TEMPERATURE ANOMALIES}',color='darkgrey',
              fontsize=30)
    
    plt.annotate(r'\textbf{DATA}: NOAA OISSTv2  [\textbf{BASE: 1971-2000}]',
                 textcoords='axes fraction',xy=(0,0),xytext=(0.76,-0.08),
                 fontsize=5,color='darkgrey',ha='left',va='center')        
    plt.annotate(r'\textbf{SOURCE}: http://www.esrl.noaa.gov/psd/',
                 textcoords='axes fraction',xy=(0,0),xytext=(0.76,-0.11),
                 fontsize=5,color='darkgrey',ha='left',va='center')
    plt.annotate(r'\textbf{GRAPHIC}: Zachary Labe (@ZLabe)',
                 textcoords='axes fraction',xy=(0,0),xytext=(0.76,-0.14),
                 fontsize=5,color='darkgrey',ha='left',va='center')
    plt.annotate(r'\textbf{$^\circ$C}',
                 textcoords='axes fraction',xy=(0,0),xytext=(0.2,-0.11),
                 fontsize=20,color='darkgrey',ha='left',va='center')
    
    plt.subplots_adjust(bottom=0.2)
    
    if i < 10:        
        plt.savefig(directoryfigure + 'sstq_00%s.png' % (i),
                    dpi=170)
    elif i < 100:
        plt.savefig(directoryfigure + 'sstq_0%s.png' % (i),
            dpi=170)
    elif i==98:
        plt.savefig(directoryfigure + 'sstq_991.png',
            dpi=170)
        plt.savefig(directoryfigure + 'sstq_992.png',
            dpi=170)
        plt.savefig(directoryfigure + 'sstq_993.png',
            dpi=170)
        plt.savefig(directoryfigure + 'sstq_994.png',
            dpi=170)    
        plt.savefig(directoryfigure + 'sstq_995.png',
            dpi=170)  
        plt.savefig(directoryfigure + 'sstq_996.png',
            dpi=170)  
        plt.savefig(directoryfigure + 'sstq_997.png',
            dpi=170) 
        plt.savefig(directoryfigure + 'sstq_998.png',
            dpi=170) 
        plt.savefig(directoryfigure + 'sstq_999.png',
            dpi=170)                 
    else:
        plt.savefig(directoryfigure + 'sstq_%s.png' % (i),
                    dpi=170)
