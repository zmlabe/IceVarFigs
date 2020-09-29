"""
Plot change in sea ice extent (NSIDC) and volume (PIOMAS) for annual means
from 1979 to 2018.

Author    : Zachary M. Labe
Date      : 14 August 2018
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
directorydata = './Data/'
directoryfigure = './Figures/'

### Load data files for Extent (e) and Antarctica (v)
filee = 'NSIDC_AnnualSIE_2019_MeanMonth.txt'
filev = 'PIOMAS_AnnualSIV_2019.txt'

### Years through 2017
years = np.arange(1979,2019+1,1)

### Read file
eq = np.genfromtxt(directorydata + filee,unpack=True)
vq = np.genfromtxt(directorydata + filev,unpack=True)                        
                        
print('\nCompleted: Read land ice data!')                        

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

plt.text(1979,10.07,r'\textbf{EXTENT}',color='deepskyblue',alpha=0.5,ha='left',
        fontsize=22,rotation=0,va='center',zorder=1)
        
ax.tick_params('both',length=5.5,width=2,which='major')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2) 

ant, = plt.plot(years,eq,linestyle='-',linewidth=3.5,
         color='deepskyblue',zorder=2,clip_on=False)

plt.scatter(years[-1],eq[-1],s=30,color='crimson',zorder=9,clip_on=False)

xlabels = map(str,np.arange(1979,2019,6))
plt.xticks(np.arange(1979,2019,6),xlabels,fontsize=7)
ylabels = map(str,np.arange(10,13,0.5))
plt.yticks(np.arange(10,13,0.5),ylabels,fontsize=7)
plt.ylim([10,12.5])
plt.xlim([1979,2019])

plt.text(2020.5,10.2,r'\textbf{2019}',fontsize=10,color='crimson',ha='left')

plt.text(1979,9.5,r'\textbf{DATA:} NSIDC Sea Ice Index v3.0 (\textbf{ANNUAL}, Satellite)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,9.42,r'\textbf{SOURCE:} ftp://sidads.colorado.edu/DATASETS/NOAA/G02135',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,9.34,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
         
plt.text(1968,12.64,r'\textbf{[\textbf{$\times$10$^{6}$ km$^{2}$}]}',color='darkgrey',
                           fontsize=12,va='center',alpha=1)      
plt.text(2024,13.1,r'\textbf{ARCTIC SEA ICE}',fontsize=32,color='w',
         ha='center',va='center',alpha=1)

###########################################################################
###########################################################################
###########################################################################
### Subplot for Volume
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
        
ax.tick_params('both',length=5,width=2,which='major')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2) 

plt.text(1979,12.4,r'\textbf{VOLUME}',color='deepskyblue',alpha=0.5,ha='left',
        fontsize=22,rotation=0,va='center',zorder=1)

gre, = plt.plot(years,vq,linestyle='-',linewidth=3.5,
         color='deepskyblue',zorder=2,clip_on=False)

plt.scatter(years[-1],vq[-1],s=30,color='crimson',zorder=9,clip_on=False)

xlabels = map(str,np.arange(1979,2019,6))
plt.xticks(np.arange(1979,2019,6),xlabels,fontsize=7)
ylabels = map(str,np.arange(12,27,2))
plt.yticks(np.arange(12,27,2),ylabels,fontsize=7)
plt.ylim([12,26])
plt.xlim([1979,2019])

plt.text(1979,9.25,r'\textbf{DATA:} PIOMAS v2.1 (\textbf{ANNUAL}, Simulated)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,8.75,r'\textbf{SOURCE:} http://psc.apl.uw.edu/research/projects/',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,8.29,r'\textbf{REFERENCE:} Zhang and Rothrock [2003]',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)

plt.text(2020.5,13.5,r'\textbf{2019}',fontsize=10,color='crimson',ha='left')
plt.text(1966.7,26.8,r'\textbf{[\textbf{$\times$1000 km$^{3}$}]}',color='darkgrey',
                           fontsize=12,va='center',alpha=1) 

fig.subplots_adjust(wspace=0.4)
fig.subplots_adjust(top=0.75)
fig.subplots_adjust(bottom=0.2)

### Create animation using matplotlib
def update(num,years,eq,vq,ant,gre,bar):
    ant.set_data(years[:num+1],eq[:num+1])
    ant.axes.axis([1979,2019,10,12.5])
    gre.set_data(years[:num+1],vq[:num+1])
    gre.axes.axis([1979,2019,12,26])
    return bar,

ani = animation.FuncAnimation(fig,update,60,fargs=[years,
                              eq,vq,ant,gre,gre],interval=0.01,blit=True)

### Save figure
#plt.savefig(directoryfigure + 'SeaIce_moving.png',dpi=300)
ani.save(directoryfigure + 'SeaIce_moving.gif',dpi=300,writer='imagemagick')

print('\nCompleted: Script done!')
                     