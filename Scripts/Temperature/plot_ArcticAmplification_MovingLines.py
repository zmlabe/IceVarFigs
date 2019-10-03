"""
Plot change in sea ice extent (NSIDC) and temperature (BEST) for annual means
from 1979 to 2017.

Author    : Zachary M. Labe
Date      : 20 August 2018
"""

### Import modules
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math 

### Time
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday

### Add directories
directorydata = '/home/zlabe/Documents/Projects/IceVarFigs/Data/'
directoryfigure = '/home/zlabe/Documents/Projects/IceVarFigs/Figures/'

### Load data files for Extent (e) and Temperature anomalies (t)
filee = 'NSIDC_AnnualSIE_2018.txt'
filet = 'BEST_Arctic.txt'

### Years through 2018
years = np.arange(1979,2018+1,1)

### Read file
eq = np.genfromtxt(directorydata + filee,unpack=True)
tq = np.genfromtxt(directorydata + filet,delimiter=',',skip_header=1,
                   unpack=True,usecols=[1]) 
tq = tq[-40:]                   
                        
print('\nCompleted: Read AA data!')                        

############################################################################
############################################################################
############################################################################
### Create animation
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='darkgrey')
plt.rc('xtick',color='darkgrey')
plt.rc('ytick',color='darkgrey')
plt.rc('axes',labelcolor='darkgrey')
plt.rc('axes',facecolor='black')

fig = plt.figure()

### Subplot for Extent
ax = plt.subplot(122)  

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

plt.text(1979,10.03,r'\textbf{SEA-ICE EXTENT}',color='deepskyblue',alpha=0.5,ha='left',
        fontsize=15,rotation=0,va='center',zorder=1)
        
ax.tick_params('both',length=5.5,width=2,which='major')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2) 

ant, = plt.plot(years,eq,linestyle='-',linewidth=3,
         color='deepskyblue',zorder=2,clip_on=False)

plt.scatter(years[-1],eq[-1],s=30,color='gold',zorder=9,clip_on=False)

xlabels = map(str,np.arange(1979,2020,6))
plt.xticks(np.arange(1979,2020,6),xlabels,fontsize=9)
ylabels = map(str,np.arange(10,13,0.5))
plt.yticks(np.arange(10,13,0.5),ylabels,fontsize=9)
plt.ylim([10,12.5])
plt.xlim([1979,2018])

plt.text(2019.2,10.29,r'\textbf{2018}',fontsize=10,color='gold',ha='left')

plt.text(1979,9.5,r'\textbf{DATA:} NSIDC Sea Ice Index v3.0 (\textbf{ANNUAL}, Satellite)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,9.42,r'\textbf{SOURCE:} ftp://sidads.colorado.edu/DATASETS/NOAA/G02135',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,9.34,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
         
plt.text(1968,12.64,r'\textbf{[\textbf{$\times$10$^{6}$ km$^{2}$}]}',color='darkgrey',
                           fontsize=12,va='center',alpha=1)      
plt.text(1970,13.1,r'\textbf{ARCTIC CLIMATE}',fontsize=32,color='w',
         ha='center',va='center',alpha=1)

###########################################################################
###########################################################################
###########################################################################
### Subplot for Volume
ax = plt.subplot(121)  

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
        
ax.tick_params('both',length=5,width=2,which='major')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2) 

plt.text(1979,-2.95,r'\textbf{AIR TEMPERATURE}',color='crimson',alpha=0.5,ha='left',
        fontsize=15,rotation=0,va='center',zorder=1)

gre, = plt.plot(years,tq,linestyle='-',linewidth=3,
         color='crimson',zorder=2,clip_on=False)

plt.scatter(years[-1],tq[-1],s=30,color='gold',zorder=9,clip_on=False)

xlabels = map(str,np.arange(1979,2020,6))
plt.xticks(np.arange(1979,2020,6),xlabels,fontsize=9)
ylabels = map(str,np.arange(-6,7,1))
plt.yticks(np.arange(-6,7,1),ylabels,fontsize=9)
plt.ylim([-3,3.5])
plt.xlim([1979,2018])

plt.text(1979,-4.36,r'\textbf{DATA:} Berkeley Earth Data using NOAA/ESRL [WRIT Tool]',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,-4.54,r'\textbf{SOURCE:} https://www.esrl.noaa.gov/psd/cgi-bin/data/testdap/timeseries.pl',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,-4.72,r'\textbf{BASELINE:} Temperature \textbf{anomalies} computed from 1981-2010',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)

plt.text(2017.25,1.6,r'\textbf{2018}',fontsize=10,color='gold',ha='left')
plt.text(1974.2,3.9,r'\textbf{($\bf{^\circ}$C)}',color='darkgrey',
                           fontsize=12,va='center',alpha=1) 

fig.subplots_adjust(wspace=0.4)
fig.subplots_adjust(top=0.75)
fig.subplots_adjust(bottom=0.2)

### Create animation using matplotlib
def update(num,years,eq,tq,ant,gre,bar):
    ant.set_data(years[:num+1],eq[:num+1])
    ant.axes.axis([1979,2018,10,12.5])
    gre.set_data(years[:num+1],tq[:num+1])
    gre.axes.axis([1979,2018,-3,3.5])
    return bar,

ani = animation.FuncAnimation(fig,update,60,fargs=[years,
                              eq,tq,ant,gre,gre],interval=0.01,blit=True)

### Save figure
#plt.savefig(directoryfigure + 'ArcticAmplification_moving.png',dpi=300)
ani.save(directoryfigure + 'ArcticAmplification.gif',dpi=300,writer='imagemagick')

print('\nCompleted: Script done!')
                     