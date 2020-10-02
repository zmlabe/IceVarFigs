"""
Script plots sea ice thickness (SIT) data using Basemap module between
ortho or polar stereographic grids
 
Source : http://psc.apl.washington.edu/zhang/IDAO/data_piomas.html
Author : Zachary Labe
Date   : 7 September 2016
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as c
import datetime
import calc_SeaIceThick_PIOMAS as CP
import iris as ir
import iris.quickplot as qplt

### Define directories
### Directory and time
directoryfigure = './Figures/'
directorydata = './Data/'

yearmin = 1979
yearmax = 2017
years = np.arange(yearmin,yearmax+1,1)
       
### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr

print '\n' '----Plot Sea Ice Thickness - %s----' % titletime

### Use functions
lats,lons,sit = CP.readPiomas(directorydata,years,0.01)

###########################################################################
###########################################################################
### Define specs
style = 'polar'
plotyr1 = 2016
plotyr2 = 2017
plotmonth = 6
###########################################################################
###########################################################################

### Computer difference
def diffThick(sit,plotyr1,plotyr2,years,month):
    """
    Function calculates different between years for PIOMAS sea ice 
    thickness with optional parameter for month

    Parameters
    ----------
    sit : 4d array [year,month,lat,lon]
        sea ice thickness
    plotyr1 : integer
        first year of difference
    plotyr2 : integer
        final year of difference
    years : 1d array
        total available years (usually 1979-present)
    month : string on integer
        'None' or integer using Python indexing of month

    Returns
    -------
    diffsit : 3d or 4d array 
        difference between years of sea ice thickness

    Usage
    -----
    diffsit = diffThick(sit,plotyr1,plotyr2,years,month)
    """
    print '\n>>> Using difference in SIT function!'    
    
    yr1 = np.where(years == plotyr1)[0]
    yr2 = np.where(years == plotyr2)[0]
    
    if month == 'None':
        year1 = sit[yr1,:,:,:]
        year2 = sit[yr2,:,:,:]
        print 'No month included'
    elif month <= 11:
        year1 = sit[yr1,month,:,:]
        year2 = sit[yr2,month,:,:]
        print '%s month sliced' % month
    else:
        ValueError('Month is out of range!')
    
    year1[np.where(np.isnan(year1))] = 0.0
    year2[np.where(np.isnan(year2))] = 0.0    
    
    diffsit = year2 - year1
    diffsit = np.squeeze(diffsit)
    diffsit[np.where(diffsit == 0.0)] = np.nan
    
    print '*Completed: Calculated difference between %s and %s!\n' \
            % (plotyr1,plotyr2)    
    return diffsit

diffsit = diffThick(sit,plotyr1,plotyr2,years,plotmonth)

print 'Completed: Beginning plotting!'
### Create colormaps for sit
def setcolor(x, color):
     for m in x:
         for t in x[m][1]:
             t.set_color(color)

### Call parameters
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='white')
plt.rc('xtick',color='white')
plt.rc('ytick',color='white')
plt.rc('axes',labelcolor='white')
plt.rc('axes',facecolor='black')
plt.rcParams['axes.linewidth'] = 0.55

### Define figure
fig = plt.figure()
ax = plt.subplot(111)

if style == 'ortho':
    m = Basemap(projection='ortho',lon_0=-90,
                lat_0=70,resolution='l',round=True)
elif style == 'polar':
    m = Basemap(projection='npstere',boundinglat=66,lon_0=270,
                resolution='l',round =True)
    
m.drawmapboundary(fill_color='white')
m.drawcoastlines(color='k',linewidth=0.3)
parallels = np.arange(50,90,10)
meridians = np.arange(-180,180,30)
m.drawparallels(parallels,labels=[False,False,False,False],
                linewidth=0.5,color='k',fontsize=4)
mer = m.drawmeridians(meridians,labels=[True,True,False,False],
                linewidth=0.5,color='k',fontsize=4)
m.drawlsmask(land_color='darkgrey',ocean_color='w')
setcolor(mer,'white')

### Adjust maximum limits
values = np.arange(-2,2.1,.2)  

### Plot filled contours    
cs = m.contourf(lons[:,:],lats[:,:],np.squeeze(diffsit[:,:]),
                values,latlon=True,extend='both')
#cs1 = m.contour(lons[:,:],lats[:,:],np.squeeze(diffsit[:,:]),
#                values,linewidths=0.2,colors='darkgrey',
#                linestyles='-',latlon=True) 
                  
### Set colormap                              
cs.set_cmap(plt.cm.get_cmap('RdBu'))

### Set colorbar
cbar = m.colorbar(cs,drawedges=True,location='right',pad = 0.4)
cbar.set_ticks(np.arange(-2,3,1))
cbar.set_ticklabels(map(str,np.arange(-2,3,1)))    
cbar.set_label(r'\textbf{Difference (m)}')
cbar.ax.tick_params(axis='y', size=.2)
  
monthtitle = datetime.date(plotyr2, plotmonth, 1).strftime('%B')  
fig.subplots_adjust(top=0.89)

plt.annotate(r'\textbf{Sea Ice Thickness -- [July, %s-%s]}' \
            % (plotyr2,plotyr1),xy=(1,1),
             xytext=(0.54,1.06),textcoords='axes fraction',
             fontsize=15,color='w',ha='center')
#plt.annotate(r'%s' % (monthtitle),xy=(1,1),
#             xytext=(-0.1,1.018),textcoords='axes fraction',
#             fontsize=14,color='w',ha='center')
plt.annotate(r'\textbf{GRAPHIC}: Zachary Labe (@ZLabe)',
             textcoords='axes fraction',
             xy=(0,0), xytext=(-0.1,-0.11),
             fontsize=4.5,color='w')
plt.annotate(r'\textbf{SOURCE}: http://psc.apl.washington.edu/zhang/IDAO/data.html',
             textcoords='axes fraction',
             xy=(0,0), xytext=(-0.1,-0.08),
             fontsize=4.5,color='w')
plt.annotate(r'\textbf{DATA}: PIOMAS v2.1 (Zhang and Rothrock, 2003)',
             textcoords='axes fraction',
             xy=(0,0), xytext=(-0.1,-0.05),
             fontsize=4.5,color='w')
    
### Save figure
plt.savefig(directoryfigure +'sit_%s_%s.png' % (plotyr1,plotyr2),dpi=800)

print 'Completed: Script finished!'