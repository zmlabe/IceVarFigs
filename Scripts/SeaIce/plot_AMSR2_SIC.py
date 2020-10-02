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
import cmocean

### Directory and time
directory = './Data/'
directoryfigure = './Figures/'

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
icedataset = 'AMSR2'
    
if icedataset == 'AMSR2':
    
    url = 'ftp://ftp-projects.cen.uni-hamburg.de/seaice/AMSR2/3.125km/'
    filename = 'Arc_%s%s%s_res3.125_pyres.nc.gz' % (currentyr,currentmn,currentdy)
    filenameout = 'Arc_AMSR2_SIC.nc'
    UL.urlretrieve(url+filename, directory + filename)
    inF = gzip.open(directory + filename, 'rb')
    outF = open(directory + filenameout, 'wb')
    outF.write( inF.read() )
    inF.close()
    outF.close()
    
    data = Dataset(directory + filenameout,'r')
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
plt.rc('axes',edgecolor='darkgrey')
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
m = Basemap(projection='npstere',boundinglat=57,lon_0=270,resolution='l',
            round =True,area_thresh=10000)
m.drawcoastlines(color = 'tomato',linewidth=0.4)
m.drawmapboundary(color='k')

cs = m.contourf(lon,lat,ice[:,:]*100.,np.arange(20,101,2),extend='min',latlon=True)
    
cmap = cmocean.cm.ice     
cs.set_cmap(cmap)

m.fillcontinents(color='k')

cbar = m.colorbar(cs,location='right',pad = 0.55)
ticks = np.arange(20,101,10)
labels = map(str,np.arange(20,101,10))
cbar.set_ticklabels(ticks,labels)
cbar.set_label(r'\textbf{CONCENTRATION [\%]}',fontsize=13,color='darkgrey')
cbar.ax.tick_params(axis='y', size=.001)

fig.suptitle(r'\textbf{ARCTIC SEA ICE -- %s}' % titletime,
             fontsize=21,color='darkgrey')
                         
plt.annotate(r'\textbf{DATA:} AMSR2 3.125 km (JAXA/Uni Hamburg-Processing)',xy=(250,80),
             xycoords='figure pixels',color='darkgrey',fontsize=6) 
plt.annotate(r'\textbf{SOURCE:} http://icdc.cen.uni-hamburg.de/daten/cryosphere.html',xy=(250,55),
             xycoords='figure pixels',color='darkgrey',fontsize=6) 
plt.annotate(r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',xy=(250,30),
             xycoords='figure pixels',color='darkgrey',fontsize=6)
            
fig.subplots_adjust(top=0.905)

print('Completed: Figure plotted!')

plt.savefig(directoryfigure + 'seaiceconc_%s.png' % currenttime, dpi=300)

print('Completed: Script done!')