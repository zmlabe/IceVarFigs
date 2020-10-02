"""
Scripts plots temperatures from Berkeley Earth contrasting the Arctic and 
global temperature anomalies - "Arctic Amplification"
 
Notes
-----
    Source : https://www.esrl.noaa.gov/psd/cgi-bin/data/testdap/timeseries.pl
    Author : Zachary Labe
    Date   : 2 July 2018
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as c
import datetime
import cmocean
from mpl_toolkits.basemap import Basemap

### Define directories
directorydata = './Data/'
directoryfigure = './Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Arctic Amplification using BEST - %s----' % titletime) 

## Alott time series
yearmin = 1900
yearmax = 2017
years = np.arange(yearmin,yearmax+1,1)
months = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',r'Aug',
          r'Sep',r'Oct',r'Nov',r'Dec']
datasets = ['Arctic','Global']
datasetsq = ['Arctic [+67$^\circ$N]','Global']

### Read in data
datat = np.empty((len(datasets),len(years)))
for i in range(len(datasets)):
    datat[i] = np.genfromtxt(directorydata + 'BEST_%s.txt' % (datasets[i]),
                         delimiter=',',skip_header=1,unpack=True,usecols=[1])

### Look for missing data    
datat[np.where(datat == -9999.000)] = np.nan

###############################################################################
###############################################################################
###############################################################################                 
#### Plot Figure
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='darkgrey')
plt.rc('xtick',color='darkgrey')
plt.rc('ytick',color='darkgrey')
plt.rc('axes',labelcolor='darkgrey')
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
         linewidth=0.7,color='darkgrey',alpha=1,linestyle='--',
         dashes=(1,0.3))

color=iter(cmocean.cm.balance_r(np.linspace(0.15,0.8,len(datasets))))
for i in range(len(datasets)):
    c=next(color)
    plt.plot(years,datat[i],linewidth=3,color=c,alpha=1,
             label = r'\textbf{%s}' % datasetsq[i])
    
    plt.text(np.max(years)+6,datat[i][-1],r'\textbf{2017}',color=c,alpha=1,
             ha='center',va='center')

plt.xticks(np.arange(1900,2040,10),np.arange(1900,2040,10))
plt.yticks(np.arange(-10,11,1),map(str,np.arange(-10,11,1))) 
plt.xlim([1900,2018])
plt.ylim([-3,4])

plt.ylabel(r'\textbf{Air Temperature Anomalies ($\bf{^\circ}$C)}',fontsize=13,
                     color='darkgrey')
plt.title(r'\textbf{ARCTIC AMPLIFICATION',
                    color='darkgrey',fontsize=25)
plt.text(1983.4,-3.0,r'\textbf{BASELINE: 1981-2010}',
         fontsize=10.1,rotation='horizontal',ha='left',color='darkgrey')

l = plt.legend(shadow=False,fontsize=7,loc='upper center',
           bbox_to_anchor=(0.5, 1.02),fancybox=True,ncol=2,frameon=False)
for text in l.get_texts():
    text.set_color('w')   
    
plt.subplots_adjust(bottom=0.15)

plt.text(1900,-4.05,r'\textbf{DATA:} Berkeley Earth Data using NOAA/ESRL Physical Sciences Division [WRIT Tool]',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(1900,-4.23,r'\textbf{SOURCE:} https://www.esrl.noaa.gov/psd/cgi-bin/data/testdap/timeseries.pl',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(2017.6,-4.05,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='right',color='darkgrey',alpha=1)   

### Save figure           
plt.savefig(directoryfigure+'ArcticAmplification_BEST_%s.png' % yearmax,dpi=300)

