"""
Plots SSMIS (F18) or OISSTv2 Sea Ice Concentration Data
 
Source : http://osisaf.met.no/p/ice/
A uthor : Zachary Labe
Date : 30 May 2016
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import urllib.request as UL
import numpy as np
import datetime
import calendar as cal

### Directory and time
directory = '/home/zlabe/Documents/Projects/SeaIceConc/'
directorys = '/home/zlabe/Documents/Projects/SeaIceConc/Figures/Year_2017/'

now = datetime.datetime.now()
currentmn = str(now.month)
if now.day == 1:
    currentdy = str(cal.monthrange(now.year,now.month-1)[1])
    currentmn = str(now.month-1)
else:
    currentdy = str(now.day-1)
if int(currentdy) < 10:
    currentdy = '0' + currentdy
    
currentyr = str(now.year)

if int(currentmn) < 10:
    currentmn = '0' + currentmn

currenttime = currentmn + '_' + str(currentdy) + '_' + currentyr
titletime = currentmn + '/' + str(currentdy) + '/' + currentyr

print('\n' 'Current Time = %s' '\n' % titletime)

### Pick data set
icedataset = 'SSMIS'

if icedataset == 'oisstv2':
    
    url = 'ftp://ftp.cdc.noaa.gov/Datasets/noaa.oisst.v2.highres/icec.day.mean.2016.v2.nc'
    UL.urlretrieve(url, 'icec.day.mean.2016.v2.nc')
    
    data = Dataset(directory + 'icec.day.mean.2016.v2.nc')
    ice = data.variables['icec'][:]
    lat = data.variables['lat'][:]
    lon = data.variables['lon'][:]
    data.close()
    
    print('Completed: Data read!')
    
elif icedataset == 'SSMIS':
    
    url = 'ftp://osisaf.met.no/prod/ice/conc/'
    filename = 'ice_conc_nh_polstere-100_multi_%s1200.nc' % (currentyr+currentmn+currentdy)
    UL.urlretrieve(url+filename, filename)
    
    data = Dataset(directory + filename)
    ice = data.variables['ice_conc'][:]
    lat = data.variables['lat'][:]    
    lon = data.variables['lon'][:]
    data.close()
    
    ice = np.asarray(np.squeeze(ice/100.))
    
    print('Completed: Data read!')

### Find missing data, mask below 15% SIC    
ice[np.where(ice <= 0.15)] = np.nan
ice[np.where(ice > .999)] = .95

print('Completed: Ice masked!')

###############################################################################
###############################################################################
###############################################################################
### Plot figure

plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='white')
plt.rc('xtick',color='white')
plt.rc('ytick',color='white')
plt.rc('axes',labelcolor='white')
plt.rc('axes',facecolor='black')

def setcolor(x, color):
     for m in x:
         for t in x[m][1]:
             t.set_color(color)

fig = plt.figure()
ax = fig.add_subplot(111)
m = Basemap(projection='npstere',boundinglat=66,lon_0=270,resolution='l',round =True)
m.drawcoastlines(color = 'k',linewidth=0.7)
m.drawcountries(color='k',linewidth=0.5)
m.drawmapboundary(color='white')

parallels = np.arange(50,86,5)
meridians = np.arange(-180,180,30)
m.drawparallels(parallels,labels=[False,False,False,False],linewidth=0.5,color='w')
par=m.drawmeridians(meridians,labels=[True,True,False,False],linewidth=0.5,fontsize=6,color='w')
setcolor(par,'white')
m.shadedrelief()

cs = m.contourf(lon,lat,ice[:,:],np.arange(0.15,1.04,.05),extend='min',latlon=True)
cs2 = m.contour(lon,lat,ice[:,:],np.arange(0.15,0.5,0.1),latlon=True,colors='gold',linewidths=1.5)
cs.set_cmap('plasma_r')

cbar = m.colorbar(cs,drawedges=True,location='right',pad = 0.55)
ticks = np.arange(0.2,1.05,0.1)
labels = map(str,np.arange(0.2,1.05,0.1))
cbar.set_ticklabels(ticks,labels)
cbar.set_label(r'\textbf{Sea Ice Concentration ($\bf{\times}$100\%)}',fontsize=13)
cbar.ax.tick_params(axis='y', size=.01)

fig.suptitle(r'\textbf{SSMIS (F18) Sea Ice Concentration -- %s}' % titletime,
             fontsize=16,color='white')
                         
plt.annotate(r'\textbf{Data:} EUMETSAT OSI SAF',xy=(150,90),
             xycoords='figure pixels',color='white',fontsize=9) 
plt.annotate(r'\textbf{Graphic:} Zachary Labe (@ZLabe)',xy=(150,30),
             xycoords='figure pixels',color='white',fontsize=9,
             bbox=dict(boxstyle="square, pad=0.3",fc='k',edgecolor='w',
                       linewidth=0.2)) 
            
fig.subplots_adjust(top=0.88)

print('Completed: Figure plotted!')

plt.savefig(directorys + 'seaiceconc_%s.png' % currenttime, dpi=300)

print('Completed: Script done!')