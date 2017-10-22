"""
Plots circle encompassing 80N

Author : Zachary Labe
Date : 24 August 2017
"""

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import datetime
import calendar as cal

### Directory and time
directoryfigure = '/home/zlabe/Documents/Projects/Tests/Utilities/Figures/'

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
    
titletime = currentmn + '/' + str(currentdy) + '/' + currentyr

### Create latitude and longitude
lat1 = np.arange(-90,90.1,0.5)
lon1 = np.arange(-180,180.1,0.5)
lon2,lat2 = np.meshgrid(lon1,lat1)


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
m = Basemap(projection='npstere',boundinglat=55.3,lon_0=270,resolution='l',
            round =True)
m.drawcoastlines(color = 'dodgerblue',linewidth=0.5)
m.drawmapboundary(color='white')
m.drawlsmask(land_color='k',ocean_color='k')

parallels = np.arange(50,91,5)
meridians = np.arange(-180,180,30)
m.drawparallels(parallels,labels=[False,False,False,False],
                linewidth=0.2,color='w')
par=m.drawmeridians(meridians,labels=[True,True,False,False],
                    linewidth=0.2,fontsize=6,color='w')
setcolor(par,'white')

cs = m.contourf(lon2,lat2,lat2,np.arange(80,100,10),latlon=True,
                colors='r')

m.fillcontinents(color='dimgrey')
                         
plt.annotate(r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',xy=(0.4,0.03),
             xycoords='figure fraction',color='darkgrey',fontsize=6)
plt.annotate(r'\textbf{80$^\circ$N+ REGION}',xy=(0.31,0.916),
             xycoords='figure fraction',color='darkgrey',fontsize=24)
            
fig.subplots_adjust(top=0.86)

print('Completed: Figure plotted!')

plt.savefig(directoryfigure + 'N80_degrees.png',dpi=700)

print('Completed: Script done!')