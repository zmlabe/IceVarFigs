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
import calendar as cal
import gzip
import nclcmaps as ncm

### Directory and time
directory = '/home/zlabe/Documents/Projects/SeaIceConc_AMSR/'
directorys = '/home/zlabe/Documents/Projects/SeaIceConc_AMSR/Figures/Year_2017/'

now = datetime.datetime.now()
currentmn = str(now.month)
if now.day == 1:
    currentdy = str(cal.monthrange(now.year,now.month-1)[1])
    currentmn = str(now.month-1)
else:
    currentdy = str(now.day-2)
if int(currentdy) < 10:
    currentdy = '0' + currentdy
    
currentyr = str(now.year)

if int(currentmn) < 10:
    currentmn = '0' + currentmn

currenttime = currentmn + '_' + str(currentdy) + '_' + currentyr
titletime = currentmn + '/' + str(currentdy) + '/' + currentyr

print('\n' 'Current Time = %s' '\n' % titletime)

### Pick data set
icedataset = 'AMSR2'
    
if icedataset == 'AMSR2':
    
    url = 'ftp://ftp-projects.cen.uni-hamburg.de/seaice/AMSR2/3.125km/'
    filename = 'Arc_%s%s%s_res3.125_pyres.nc.gz' % (currentyr,currentmn,currentdy)
    filenameout = 'Arc_AMSR2_SIC.nc'
    UL.urlretrieve(url+filename, filename)
    inF = gzip.open(filename, 'rb')
    outF = open(filenameout, 'wb')
    outF.write( inF.read() )
    inF.close()
    outF.close()
    
    data = Dataset(filenameout)
    ice = data.variables['sea_ice_concentration'][:]
    lat = data.variables['latitude'][:]    
    lon = data.variables['longitude'][:]
    data.close()
    
    ice = np.asarray(np.squeeze(ice/100.))
    
    print('Completed: Data read!')
    
ice[np.where(ice <= 0.15)] = np.nan
ice[np.where((ice >= 0.999) & (ice <= 1))] = 0.999
ice[np.where(ice > 1)] = np.nan

print('Completed: Ice masked!')

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
m = Basemap(projection='npstere',boundinglat=57,lon_0=270,resolution='l',round =True)
m.drawcoastlines(color = 'y',linewidth=0.4)
m.drawmapboundary(color='white')
#m.drawlsmask(land_color='k',ocean_color='k')

#parallels = np.arange(50,86,5)
#meridians = np.arange(-180,180,30)
#m.drawparallels(parallels,labels=[False,False,False,False],linewidth=0.0,color='w')
#par=m.drawmeridians(meridians,labels=[True,True,False,False],linewidth=0.0,fontsize=6,color='w')
#setcolor(par,'white')

cs = m.contourf(lon,lat,ice[:,:],np.arange(0.2,1.01,.02),extend='min',latlon=True)
#cs.set_cmap('GMT_relief_oceanography')

cmap = ncm.cmap('MPL_YlGnBu')         
cs.set_cmap(cmap)

m.fillcontinents(color='k')

cbar = m.colorbar(cs,location='right',pad = 0.55)
ticks = np.arange(0.2,1.05,0.1)
labels = map(str,np.arange(0.2,1.05,0.1))
cbar.set_ticklabels(ticks,labels)
cbar.set_label(r'\textbf{SIC ($\bf{\times}$100\%)}',fontsize=13)
cbar.ax.tick_params(axis='y', size=.001)

fig.suptitle(r'\textbf{Sea Ice Concentration (SIC) -- %s}' % titletime,
             fontsize=16,color='white')
                         
plt.annotate(r'\textbf{Data:} AMSR2 3.125 km (JAXA/Uni Hamburg-Processing)',xy=(250,80),
             xycoords='figure pixels',color='white',fontsize=6) 
plt.annotate(r'\textbf{CSV:} http://icdc.cen.uni-hamburg.de/daten/cryosphere.html',xy=(250,55),
             xycoords='figure pixels',color='white',fontsize=6) 
plt.annotate(r'\textbf{Graphic:} Zachary Labe (@ZLabe)',xy=(250,30),
             xycoords='figure pixels',color='white',fontsize=6)
            
fig.subplots_adjust(top=0.905)

print('Completed: Figure plotted!')

plt.savefig(directorys + 'seaiceconc_%s.png' % currenttime, dpi=300)

print('Completed: Script done!')