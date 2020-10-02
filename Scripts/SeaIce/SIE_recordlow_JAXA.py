"""
Calculates current year percentage of record daily low SIE 2002-present 
using JAXA metadata

Website   : https://ads.nipr.ac.jp/vishop/vishop-extent.html
Author    : Zachary M. Labe
Date      : 18 October 2016
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as c
import matplotlib
import datetime
import urllib.request
import urllib as UL

### Directory and time
directoryfigure = './Figures/'
source = 'twitter'
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr

### Load url
url = 'https://ads.nipr.ac.jp/vishop.ver1/data/graph/plot_extent_n_v2.csv'

### Read file
raw_data = UL.request.urlopen(url)
dataset = np.genfromtxt(raw_data, skip_header=0,delimiter=",",)

### Set missing data to nan
dataset[np.where(dataset==-9999)] = np.nan

### Variables
month     = dataset[1:,0]        # 1-12, nan as month[0]
day       = dataset[1:,1]        # 1-31, nan as day[0]
mean1980  = dataset[1:,2]        # km^2, nan as mean1980[0]
mean1990  = dataset[1:,3]        # km^2, nan as mean1990[0]
mean2000  = dataset[1:,4]        # km^2, nan as mean2000[0]
years     = dataset[1:,5:]

doy       = np.arange(0,len(day),1)

### Change units to million km^2
years = years/1e6

### Recent day of current year
currentyear = years[:,-1]
lastday = now.timetuple().tm_yday -1
currentice = currentyear[lastday]
currentanom = currentice - (mean1980[lastday]/1e6)

currentyear[10] = currentyear[9]

### Changes 
weekchange = currentice - currentyear[lastday-7]
daychange = currentice - currentyear[lastday-1]

### Calculate record low SIE
recordlow = np.empty((years.shape[0]))
for i in range(years.shape[0]):
    if years[i,-1] == np.nanmin(years[i,:]):
        recordlow[i] = 1.
    else: 
        recordlow[i] = 0.

numberlow = np.count_nonzero(recordlow == 1.)
percentlow = float(numberlow)/(lastday) * 100.

print('\n')
print('[%s] of days so far at a record low SIE!' % (round(percentlow,2)))
print('\n')
print('Total new records [%s] out of [%s] for SIE! \n' % (numberlow,lastday))

means = np.nanmean(years[:lastday,:],axis=0)

values = np.arange(len(recordlow))

### Call parameters
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='darkgrey')
plt.rc('xtick',color='darkgrey')
plt.rc('ytick',color='darkgrey')
plt.rc('axes',labelcolor='darkgrey')
plt.rc('axes',facecolor='black')
plt.rcParams['xtick.direction'] = 'out'

fig = plt.figure()
ax = plt.subplot(111)

### Adjust axes in time series plots 
def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 0))
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
        
ax.tick_params('both',length=5.5,width=2,which='major',color='darkgrey')             
adjust_spines(ax, ['left', 'bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['left'].set_linewidth(0)       
ax.spines['bottom'].set_linewidth(2)  

barlist = plt.bar(np.arange(366),recordlow,color='indianred',
                  edgecolor='tomato')
                  
xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan']
plt.xticks(np.arange(0,390,30),xlabels,rotation=0)
plt.xlim([0,360])  

plt.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    left='off',      # ticks along the bottom edge are off
    right='off',         # ticks along the top edge are off
    labelleft='off') # labels along the bottom edge are off                

plt.title(r'\textbf{%s - \underline{NEW} DAILY RECORD LOW ARCTIC SEA ICE EXTENTS}' % currentyr,
                       fontsize=15,color='darkgrey') 

plt.text(-25,0.835,r'\textbf{$\leftarrow$ one record $\rightarrow$}',
                       fontsize=16,color='tomato',rotation=90) 

plt.text(185,0.41,r'\textbf{\underline{%s}' % numberlow,
         fontsize=55,rotation='horizontal',ha='left',color='tomato',
         alpha=1)
                       
plt.text(0,-0.18,r'\textbf{DATA:} JAXA (Arctic Data archive System, NIPR)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0,-0.22,r'\textbf{SOURCE:} https://ads.nipr.ac.jp/vishop/vishop-extent.html',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(360,-0.18,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='right',color='darkgrey')    
         
fig.subplots_adjust(bottom=0.2)   
fig.subplots_adjust(top=0.8)           

plt.savefig(directoryfigure + 'recordlow_bars_year.png',dpi=300)