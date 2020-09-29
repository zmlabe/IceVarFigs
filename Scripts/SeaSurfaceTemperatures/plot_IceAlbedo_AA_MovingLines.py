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
directorydata = './Data/'
directoryfigure = './Figures/'

### Load data files for Extent (e) and Temperature anomalies (t)
filee = 'NSIDC_AnnualSIE_2019_MeanMonth.txt'
filet = 'BEST_Arctic.txt'
files = 'SST_Arctic_67N_annual_1982-2019.txt'

### Years through 2019
years = np.arange(1979,2019+1,1)
yearsst = np.arange(1982,2019+1,1)

### Read file
eq = np.genfromtxt(directorydata + filee,unpack=True)
#####
tq = np.genfromtxt(directorydata + filet,delimiter=',',skip_header=1,
                   unpack=True,usecols=[1]) 
tq = tq[-41:]                   
#####
sq1 = np.genfromtxt(directorydata + files,unpack=True)
emptysst = np.array([np.nan]*(1982-1979))
sq = np.append(emptysst,sq1)
#####
                        
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

fig = plt.figure(figsize=(9,4))

### Subplot for Extent
ax = plt.subplot(132)  

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
        fontsize=11,rotation=0,va='center',zorder=1)
        
ax.tick_params('both',length=5.5,width=2,which='major')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2) 

ant, = plt.plot(years,eq,linestyle='-',linewidth=3,
         color='deepskyblue',zorder=2,clip_on=False)

plt.scatter(years[-1],eq[-1],s=30,color='gold',zorder=9,clip_on=False)

xlabels = map(str,np.arange(1979,2020,5))
plt.xticks(np.arange(1979,2020,5),xlabels,fontsize=6)
ylabels = map(str,np.arange(10,13,0.5))
plt.yticks(np.arange(10,13,0.5),ylabels,fontsize=6)
plt.ylim([10,12.5])
plt.xlim([1979,2019])

plt.text(2020.2,10.16,r'\textbf{2019}',fontsize=8,color='gold',ha='left')

plt.text(1979,9.5,r'\textbf{DATA:} NSIDC Sea Ice Index v3.0 (\textbf{ANNUAL}, Satellite)',
         fontsize=4.5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,9.42,r'\textbf{SOURCE:} ftp://sidads.colorado.edu/DATASETS/NOAA/G02135',
         fontsize=4.5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,9.34,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=4.5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
         
plt.text(1968,12.64,r'\textbf{[\textbf{$\times$10$^{6}$ km$^{2}$}]}',color='darkgrey',
                           fontsize=12,va='center',alpha=1)      
plt.text(2001,13.1,r'\textbf{ARCTIC AMPLIFICATION}',fontsize=32,color='w',
         ha='center',va='center',alpha=1)

###########################################################################
###########################################################################
###########################################################################
### Subplot for Volume
ax = plt.subplot(131)  

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
        fontsize=11,rotation=0,va='center',zorder=1)

gre, = plt.plot(years,tq,linestyle='-',linewidth=3,
         color='crimson',zorder=2,clip_on=False)

plt.scatter(years[-1],tq[-1],s=30,color='gold',zorder=9,clip_on=False)

xlabels = map(str,np.arange(1979,2020,5))
plt.xticks(np.arange(1979,2020,5),xlabels,fontsize=6)
ylabels = map(str,np.arange(-6,7,1))
plt.yticks(np.arange(-6,7,1),ylabels,fontsize=6)
plt.ylim([-3,3])
plt.xlim([1979,2019])

plt.text(1979,-4.22,r'\textbf{DATA:} Berkeley Earth Data using NOAA/ESRL [WRIT Tool; +67$\bf{^\circ}$N]',
         fontsize=4.5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,-4.40,r'\textbf{SOURCE:} https://www.esrl.noaa.gov/psd/cgi-bin/data/testdap/timeseries.pl',
         fontsize=4.5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,-4.58,r'\textbf{BASELINE:} Temperature \textbf{anomalies} computed from 1981-2010 (\textbf{ANNUAL})',
         fontsize=4.5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)

plt.text(2020.25,1.73,r'\textbf{2019}',fontsize=8,color='gold',ha='left')
plt.text(1974.2,3.35,r'\textbf{[$\bf{^\circ}$C]}',color='darkgrey',
                           fontsize=12,va='center',alpha=1) 

###########################################################################
###########################################################################
###########################################################################
### Subplot for SST
ax = plt.subplot(133)  

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

plt.text(1979,-0.484,r'\textbf{SEA SURFACE TEMPERATURE}',color='crimson',alpha=0.5,ha='left',
        fontsize=11,rotation=0,va='center',zorder=1)

sst, = plt.plot(years,sq,linestyle='-',linewidth=3,
         color='crimson',zorder=2,clip_on=False)

plt.scatter(years[-1],sq[-1],s=30,color='gold',zorder=9,clip_on=False)

xlabels = map(str,np.arange(1979,2020,5))
plt.xticks(np.arange(1979,2020,5),xlabels,fontsize=6)
ylabels = map(str,np.around(np.arange(-6,7,0.25),4))
plt.yticks(np.arange(-6,7,0.25),ylabels,fontsize=6)
plt.ylim([-0.5,0.75])
plt.xlim([1979,2019])

plt.text(1979,-0.75,r'\textbf{DATA:} NOAA Optimum Interpolation (OI) Sea Surface Temperature (SST) V2 [+67$\bf{^\circ}$N]',
         fontsize=4.5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,-0.785,r'\textbf{SOURCE:} https://www.esrl.noaa.gov/psd/data/gridded/data.noaa.oisst.v2.html',
         fontsize=4.5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1979,-0.82,r'\textbf{BASELINE:} SST \textbf{anomalies} computed from 1982-2010 (\textbf{ANNUAL})',
         fontsize=4.5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)

plt.text(2020.25,0.345,r'\textbf{2019}',fontsize=8,color='gold',ha='left')
plt.text(1974.2,0.825,r'\textbf{[$\bf{^\circ}$C]}',color='darkgrey',
                           fontsize=12,va='center',alpha=1)

fig.subplots_adjust(wspace=0.4)
fig.subplots_adjust(top=0.75)
fig.subplots_adjust(bottom=0.2)

#### Create animation using matplotlib
def update(num,years,eq,tq,sq,ant,gre,sst,bar):
    ant.set_data(years[:num+1],eq[:num+1])
    ant.axes.axis([1979,2019,10,12.5])
    gre.set_data(years[:num+1],tq[:num+1])
    gre.axes.axis([1979,2019,-3,3])
    sst.set_data(years[:num+1],sq[:num+1])
    sst.axes.axis([1979,2019,-0.5,0.75])
    return bar,

ani = animation.FuncAnimation(fig,update,70,fargs=[years,
                              eq,tq,sq,ant,gre,sst,sst],interval=0.01,blit=True)

### Save figure
#plt.savefig(directoryfigure + 'IceAlbedo_AA_moving.png',dpi=220)
ani.save(directoryfigure + 'IceAlbedo_AA_moving.gif',dpi=220,writer='imagemagick')

print('\nCompleted: Script done!')
                     