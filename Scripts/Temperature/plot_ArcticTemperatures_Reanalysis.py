"""
Scripts plots reanalysis data of 2-m Arctic temperatures (67N+)
 
Notes
-----
    Source : https://www.esrl.noaa.gov/psd/cgi-bin/data/testdap/timeseries.pl
    Author : Zachary Labe
    Date   : 19 October 2017
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as c
import datetime
import cmocean
from mpl_toolkits.basemap import Basemap

### Define directories
directorydata = '/home/zlabe/Documents/Projects/IceVarFigs/Data/'
directoryfigure = '/home/zlabe/Documents/Projects/IceVarFigs/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Arctic Temperatures (Reanalysis Data) - %s----' % titletime) 

## Alott time series
yearmin = 1900
yearmax = 2017
years = np.arange(yearmin,yearmax+1,1)
months = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',r'Aug',
          r'Sep',r'Oct',r'Nov',r'Dec']
datasets = ['R1','R2','CFSR','MERRA2','JRA55','ERAi']

### Read in data
datat = np.empty((len(datasets),len(years)))
for i in range(len(datasets)):
    datat[i] = np.genfromtxt(directorydata + '%s_Arctic_%s.txt' % (datasets[i],
                             yearmax),delimiter=',',skip_header=1,
                             unpack=True,usecols=[1])

### Look for missing data    
datat[np.where(datat == -9999.000)] = np.nan

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
        
fig = plt.figure()
ax = plt.subplot(111)

adjust_spines(ax, ['left', 'bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.tick_params('both',length=5.5,width=2,which='major')

plt.plot(np.arange(yearmin,yearmax+2,1),([0]*(len(years)+1)),
         linewidth=2,color='darkgrey',alpha=1,linestyle='--')

color=iter(cmocean.cm.thermal(np.linspace(0.17,1,len(datasets))))
for i in range(len(datasets)):
    c=next(color)
    plt.plot(years,datat[i],linewidth=1.3,color=c,alpha=1,
             label = '%s' % datasets[i])

plt.xticks(np.arange(1900,2040,10),np.arange(1900,2040,10))
plt.yticks(np.arange(-2,4,1),map(str,np.arange(-2,4,1))) 
plt.xlim([1958,2017])
plt.ylim([-2.3,3])

plt.ylabel(r'\textbf{2-m Air Temperature Anomalies ($\bf{^\circ}$C)}',fontsize=13,
                     color='darkgrey')
plt.title(r'\textbf{ARCTIC TEMPERATURES',
                    color='darkgrey',fontsize=25)
plt.text(2000,-2.3,r'\textbf{BASELINE: 1981-2010}',
         fontsize=10.1,rotation='horizontal',ha='left',color='darkgrey')

l = plt.legend(shadow=False,fontsize=7,loc='upper right',
           bbox_to_anchor=(0.73, 1.02),fancybox=True,ncol=3,frameon=False)
for text in l.get_texts():
    text.set_color('w')   

plt.text(1958,-3.05,r'\textbf{DATA:} NOAA/ESRL Physical Sciences Division [WRIT Tool; +67$\bf{^\circ}$N]',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1958,-3.2,r'\textbf{SOURCE:} https://www.esrl.noaa.gov/psd/cgi-bin/data/testdap/timeseries.pl',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(2017,-3.05,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='right',color='darkgrey',alpha=1)

plt.subplots_adjust(bottom=0.15)        

###############################################################################
###############################################################################
###############################################################################
### Create subplot of region of averaging (67N+)

### Add axis for subplot
a = plt.axes([.65, .19, .29, .24], axisbg='w') 

def setcolor(x, color):
     for m in x:
         for t in x[m][1]:
             t.set_color(color)

lat1 = np.arange(-90,90.1,0.5)
lon1 = np.arange(-180,180.1,0.5)
lon2,lat2 = np.meshgrid(lon1,lat1)

m = Basemap(projection='npstere',boundinglat=55.3,lon_0=270,resolution='l',
            round =True,area_thresh=10000)
m.drawcoastlines(color = c,linewidth=0.3)
m.drawmapboundary(color='k')
m.drawlsmask(land_color='k',ocean_color='k')

parallels = np.arange(50,91,5)
meridians = np.arange(-180,180,30)
m.drawparallels(parallels,labels=[False,False,False,False],
                linewidth=0.2,color='w')
par=m.drawmeridians(meridians,labels=[False,False,False,False],
                    linewidth=0.2,fontsize=6,color='w')
setcolor(par,'white')

cs = m.contourf(lon2,lat2,lat2,np.arange(67,100,10),latlon=True,
                colors='darkgrey')
           
### Save figure
plt.savefig(directoryfigure+'Reanalysis_Arctic_T_%s.png' % yearmax,dpi=300)

