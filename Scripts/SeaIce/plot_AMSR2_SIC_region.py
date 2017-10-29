"""
Plots JAXA AMSR2 3.125 km (Univ Hamburg-Processed) Sea Ice Concentration Data
 
Author : Zachary Labe
Date : 27 February 2017
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import urllib
import numpy as np
import datetime
import calendar as cal
import gzip
import nclcmaps as ncm
import math

### Directory and time
directory = '/home/zlabe/Documents/Projects/SeaIceConc_AMSR/'
directorys = '/home/zlabe/Documents/Projects/SeaIceConc_AMSR/Figures/Year_2017/Regions/'

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

### Pick data set [AMSR2] only available so far
icedataset = 'AMSR2'
    
if icedataset == 'AMSR2':
    
    url = 'ftp://ftp-projects.cen.uni-hamburg.de/seaice/AMSR2/3.125km/'
    filename = 'Arc_%s%s%s_res3.125_pyres.nc.gz' % (currentyr,currentmn,currentdy)
    filenameout = 'Arc_AMSR2_SIC.nc'
    urllib.urlretrieve(url+filename, filename)
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
  
### Mask missing data and values less than 15% SIC    
ice[np.where(ice <= 0.15)] = np.nan
ice[np.where((ice >= 0.999) & (ice <= 1))] = 0.999
ice[np.where(ice > 1)] = np.nan
ice = ice*100.

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

### Pick region from following list
region = 'pacific'

if region == 'kara':
    # Kara Sea
    latmin = 67
    latmax = 87
    lonmin = 20
    lonmax = 90
    
elif region == 'beaufort':
    # Beaufort Sea
    latmin = 64
    latmax = 87
    lonmin = 180
    lonmax = 240

elif region == 'bering':
    # Bering/Chukchi Sea/Okhotsk 
    latmin = 45
    latmax = 83
    lonmin = 135
    lonmax = 210

elif region == 'greenland':
    # Greenland
    latmin = 55
    latmax = 89.5
    lonmin = 280
    lonmax = 395
    
elif region == 'pacific':
    # Central Arctic
    latmin = 69
    latmax = 89.99
    lonmin = 160
    lonmax = 250    

else:
    ValueError('Wrong region listed!')

### Region specific NPSTERE map
def polar_stere(lon_w, lon_e, lat_s, lat_n, **kwargs):
    '''Returns a Basemap object (NPS/SPS) focused in a region.
    
    lon_w, lon_e, lat_s, lat_n -- Graphic limits in geographical coordinates.
                                  W and S directions are negative.
    **kwargs -- Aditional arguments for Basemap object.
    
    '''
    lon_0 = lon_w + (lon_e - lon_w) / 2.
    ref = lat_s if abs(lat_s) > abs(lat_n) else lat_n
    lat_0 = math.copysign(90., ref)
    proj = 'npstere' if lat_0 > 0 else 'spstere'
    prj = Basemap(projection=proj, lon_0=lon_0, lat_0=lat_0,
                          boundinglat=0, resolution='l')
    #prj = pyproj.Proj(proj='stere', lon_0=lon_0, lat_0=lat_0)
    lons = [lon_w, lon_e, lon_w, lon_e, lon_0, lon_0]
    lats = [lat_s, lat_s, lat_n, lat_n, lat_s, lat_n]
    x, y = prj(lons, lats)
    ll_lon, ll_lat = prj(min(x), min(y), inverse=True)
    ur_lon, ur_lat = prj(max(x), max(y), inverse=True)
    return Basemap(projection='stere', lat_0=lat_0, lon_0=lon_0,
                       llcrnrlon=ll_lon, llcrnrlat=ll_lat,
                       urcrnrlon=ur_lon, urcrnrlat=ur_lat, round=True,
                       resolution='l')

### Call function for map grid
m = polar_stere(lonmin,lonmax,latmin,latmax)

m.drawcoastlines(color = 'y',linewidth=1)
m.drawmapboundary(color='white')
m.drawlsmask(land_color='k',ocean_color='k')

cs = m.contourf(lon,lat,ice[:,:],np.arange(20,100.01,.1),extend='min',latlon=True)

cmap = ncm.cmap('MPL_YlGnBu')         
cs.set_cmap(cmap)

m.fillcontinents(color='k')

cbar = m.colorbar(cs,location='right',pad = 0.2)
cbar.outline.set_edgecolor('k')
barlim = np.arange(20,101,10)
cbar.set_ticks(barlim)
cbar.set_ticklabels(list(map(str,barlim))) 
cbar.set_label(r'\textbf{Concentration (\%)}',fontsize=13,
                         alpha=0.6)
cbar.ax.tick_params(axis='y', size=.01)

fig.suptitle(r'\textbf{ARCTIC SEA ICE -- %s}' % titletime,
             fontsize=22,color='white',alpha=0.6)
                         
plt.annotate(r'\textbf{DATA:} AMSR2 3.125 km (JAXA/Uni Hamburg-Processing)',
             xy=(250,100),xycoords='figure pixels',color='white',fontsize=6,
             alpha=0.7,rotation=0) 
plt.annotate(r'\textbf{SOURCE:} http://icdc.cen.uni-hamburg.de/daten/cryosphere.html',
             xy=(250,80),xycoords='figure pixels',color='white',fontsize=6,
             alpha=0.7,rotation=0) 
plt.annotate(r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',xy=(250,60),
             xycoords='figure pixels',color='white',fontsize=6,
             alpha=0.7,rotation=0)
            
fig.subplots_adjust(top=0.89)

print('Completed: Figure plotted!')

plt.savefig(directorys + 'seaiceconc_%s_%s.png' % (region,currenttime), dpi=300)

print('Completed: Script done!')