"""
Reads in current year's Arctic sea ice extent from Sea Ice Index 2 (NSIDC)

Website   : ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/daily/data/
Author    : Zachary M. Labe
Date      : 5 September 2016
"""

### Import modules
import numpy as np
import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
from netCDF4 import Dataset
import cmocean

### Directory and time
directorydata = '/surtsey/zlabe/seaice_obs/PIOMAS/' 
directoryfigure = '/home/zlabe/Documents/Projects/Tests/Utilities/Figures/'
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday

### Time
years = np.arange(1979,2010+1,1)

directorydata = '/surtsey/zlabe/seaice_obs/seaice_reconstruct/'
directoryfigure = '/home/zlabe/Documents/Projects/Tests/Utilities/Figures/'
now = datetime.datetime.now()
month = now.month

years = np.arange(1914,2013+1,1)

data = Dataset(directorydata + 'G10010_SIBT1850_v1.1.nc')
lats = data.variables['latitude'][:]
lons = data.variables['longitude'][:]
sic = data.variables['seaice_conc'][768:,:,:]
data.close()

lon2,lat2 = np.meshgrid(lons,lats)

### Reshape concentration
sic = np.reshape(sic,(sic.shape[0]//12,12,lats.shape[0],lons.shape[0]))

### Slice month
sicmo = sic[:,2,:,:]
sicmo[np.where(sicmo < 0.01)] = np.nan
sicmo = sicmo/100.

#### Calculate 1981-2010 average
yearq = np.where((years>=1981) & (years<=2010))[0]
mean = np.nanmean(sicmo[yearq,:,:],axis=0)*100.

###############################################################################
###############################################################################
###############################################################################
### Plot Figure
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
m = Basemap(projection='npstere',boundinglat=43,lon_0=270,resolution='l',round =True)
m.drawcoastlines(color = 'k',linewidth=0.5)
m.drawmapboundary(color='k')
m.drawlsmask(land_color='k',ocean_color='k')

#parallels = np.arange(50,91,5)
#meridians = np.arange(-180,180,30)
#m.drawparallels(parallels,labels=[False,False,False,False],
#                linewidth=0.2,color='w')
#par=m.drawmeridians(meridians,labels=[True,True,False,False],
#                    linewidth=0.2,fontsize=6,color='w')
#setcolor(par,'white')

cs = m.contourf(lon2,lat2,mean,50,latlon=True)
cs1 = m.contour(lon2,lat2,lat2,np.arange(80,100,10),latlon=True,colors='r',
                linestyles='--',dashes=(1,0.2))
cs2 = m.contour(lon2,lat2,lat2,np.arange(67,77,10),latlon=True,colors='r',
                linestyles='-',linewidths=2.5)
cs2 = m.contour(lon2,lat2,lat2,np.arange(50,60,10),latlon=True,colors='r',
                linestyles='--',dashes=(1,0.2))
cs3 = m.plot(0,90,'ro',markersize=3.5,latlon=True)
cs.set_cmap(cmocean.cm.ice)

plt

m.fillcontinents(color='k')
                        
plt.annotate(r'\textbf{80$^\circ$N}',xy=(0.51,0.55),
             xycoords='figure fraction',color='r',fontsize=8.5,
             ha='center',va='center')
plt.annotate(r'\textbf{67$^\circ$N}',xy=(0.51,0.65),
             xycoords='figure fraction',color='r',fontsize=8.5,
             ha='center',va='center')
plt.annotate(r'\textbf{50$^\circ$N}',xy=(0.51,0.79),
             xycoords='figure fraction',color='r',fontsize=8.5,
             ha='center',va='center')

 
plt.annotate(r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',xy=(0.51,0.1),
             xycoords='figure fraction',color='darkgrey',fontsize=6,
             ha='center',va='center')
plt.annotate(r'\textbf{DATA:} March (1981-2010) SSMIS DMSP (NSIDC)',xy=(0.51,0.08),
             xycoords='figure fraction',color='darkgrey',fontsize=6,
             ha='center',va='center')
plt.annotate(r'\textbf{ARCTIC SEA ICE ANNUAL \underline{MAX}}',xy=(0.51,0.88),
             xycoords='figure fraction',color='darkgrey',fontsize=24,
             ha='center',va='center')

print('Completed: Figure plotted!')

plt.savefig(directoryfigure + 'seaiceMAX_climo.png',dpi=300)

print('Completed: Script done!')