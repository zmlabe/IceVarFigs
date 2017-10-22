"""
Plots Arctic mean surface temperature (1948-2016) for Jan-month

Website   : http://www.esrl.noaa.gov/psd/cgi-bin/data/timeseries/timeseries1.pl
Author    : Zachary M. Labe
Date      : 15 May 2016
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as c
import scipy.stats as sts
import nclcmaps as ncm

### Directory and time
directoryfigure = '/home/zlabe/Documents/Projects/GlobalTemperature/Results/'
directorydata = '/home/zlabe/Documents/Projects/GlobalTemperature/Data/'           

### Insert month
month = 'Dec'

### Retrieve Data
data = np.genfromtxt(directorydata + 'Arctic_Tsurf_months_Jan%s.txt' % month,
                          unpack=True,usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12])
years = data[0,:]
temps = data[1:,-39:]
currentyear = int(years[-1])

temps = np.flipud(temps)

rank = np.empty(temps.shape)
for i in range(temps.shape[0]):
    rank[i,:] = abs(sts.rankdata(temps[i,:],method='min')-40)
    
    
### Call parameters
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='darkgrey')
plt.rc('xtick',color='white')
plt.rc('ytick',color='white')
plt.rc('axes',labelcolor='white')
plt.rc('axes',facecolor='black')

### Plot first meshgrid
fig = plt.figure()
ax = plt.subplot(111)

ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['left'].set_color('none')
ax.get_xaxis().set_tick_params(direction='out', width=2,length=3,
            color='darkgrey')

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='on',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='on')
plt.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    left='off',      # ticks along the bottom edge are off
    right='off',         # ticks along the top edge are off
    labelleft='on')

cs = plt.pcolormesh(rank,shading='faceted',edgecolor='k',
                    linewidth=0.3,vmin=1,vmax=37)

#cmap = ncm.cmap('MPL_RdGy')        
#cs.set_cmap(cmap)   
cs.set_cmap('RdBu')

ylabels = [r'\textbf{D}',r'\textbf{N}',r'\textbf{O}',r'\textbf{S}',
           r'\textbf{A}',r'\textbf{J}',r'\textbf{J}',r'\textbf{M}',
           r'\textbf{A}',r'\textbf{M}',r'\textbf{F}',r'\textbf{J}']
plt.yticks(np.arange(0.5,12.5,1),ylabels,ha='center',color='darkgrey')
yax = ax.get_yaxis()
yax.set_tick_params(pad=5)
plt.xticks(np.arange(0.5,39.5,3),map(str,np.arange(1979,2017,3)),
           color='darkgrey')
plt.xlim([0,39])

plt.text(-2,-3.3,r'Coldest',color='darkgrey')
plt.text(36.2,-3.3,r'Warmest',color='darkgrey')

for i in range(rank.shape[0]):
    for j in range(rank.shape[1]):
        plt.text(j+0.5,i+0.5,'%s' % int(rank[i,j]),fontsize=6,
                 color='k',va='center',ha='center')
                 
cbar = plt.colorbar(cs,orientation='horizontal',aspect=50,pad=0.12)
cbar.ax.invert_xaxis()
cbar.set_ticks([])
cbar.set_label(r'\textbf{AIR TEMPERATURE RANK BY MONTH}',
               color='darkgrey',labelpad=7,fontsize=13)

plt.text(9.8,-4.3,r'[ NCEP/NCAR Reanalysis : 925 hPa, \textbf{Arctic}, 70N+ ]',
         fontsize=7,color='darkgrey')
         
plt.text(0,12.39,r'\textbf{DATA:} NOAA/ESRL/PSD',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0,12.05,r'\textbf{SOURCE:} http://www.esrl.noaa.gov/psd/data/timeseries/',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(39.,12.05,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='right',color='darkgrey') 

plt.savefig(directoryfigure + '925T_70N_rank.png',dpi=400)