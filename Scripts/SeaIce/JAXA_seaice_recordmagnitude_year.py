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
import matplotlib
import datetime
import urllib as UL

### Directory and time
directoryfigure = '/home/zlabe/Documents/Projects/IceVarFigs/Figures/' 
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day-1)
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
lastday = now.timetuple().tm_yday - 1
currentice = currentyear[lastday]
currentanom = currentice - (mean1980[lastday]/1e6)

### Fill in random missing days (does not affect!)
currentyear[10] = currentyear[9]

### Calculate magnitude of record
years2 = years[:,:-1]
mins = np.nanmin(years2[:,:],axis=1)

### Select month
octs = np.where(month == 10)[0]
recdiff = currentyear - mins

###############################################################################
###############################################################################
###############################################################################
### Plot figure
matplotlib.rc('savefig', facecolor='black')
matplotlib.rc('axes', edgecolor='white')
matplotlib.rc('xtick', color='white')
matplotlib.rc('ytick', color='white')
matplotlib.rc('axes', labelcolor='white')
matplotlib.rc('axes', facecolor='black')
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']})

fig = plt.figure()
ax = plt.subplot(111) 

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
        
adjust_spines(ax, ['left', 'bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)

recdiff_masked = np.ma.masked_less_equal(recdiff, 0)

zeroline = [0]*len(doy)
plt.plot(doy,zeroline,linewidth=2,color='w',linestyle='--',
         zorder=11)        
barlist = plt.bar(np.arange(366),recdiff,color='indianred',
                  edgecolor='indianred',zorder=10)         
barlist = plt.bar(np.arange(366),recdiff_masked.filled(np.nan),
                  color='cornflowerblue',edgecolor='dodgerblue',zorder=11)        

xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan'] 
plt.xticks(np.arange(0,366,30.4),xlabels,rotation=0,fontsize=11)
ylabels = [r'-1.5',r'-1.0',r'-0.5',r'\textbf{0.0}',r'0.5',r'1.0',r'1.5']
plt.yticks(np.arange(-1.5,1.6,0.5),ylabels,fontsize=11)

plt.text(0,-1.35,r'\textbf{DATA:} JAXA (Arctic Data archive System, NIPR)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0,-1.45,r'\textbf{SOURCE:} https://ads.nipr.ac.jp/vishop/vishop-extent.html',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0,-1.25,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey') 
         
plt.text(90,1.55,r'[ 2017 -- Previous Daily Record ]',color='darkgrey',ha='left',
         fontsize=11)
         
plt.xlim([0,365])
plt.ylim([-1.5,1.5])

plt.ylabel(r'\textbf{Extent [$\bf{\times 10^{6}}$\ \textbf{km}$\bf{^2}$]}',
           fontsize=15,color='darkgrey')

ax.yaxis.grid(zorder=1,color='w',alpha=0.35)
fig.suptitle(r'\textbf{ARCTIC SEA ICE EXTENT}',
                       fontsize=18,color='darkgrey') 
ax.tick_params('both',length=5.5,width=2,which='major')

### Save figure
plt.savefig(directoryfigure + 'JAXA_seaice_record_magnitude_year',dpi=900)

### Print additional information
print('\n')
print('----JAXA Sea Ice Change----')
print('Day 5 = %s km^2' % ((currentyear[lastday-4] - currentyear[lastday-5])*1e6))
print('Day 4 = %s km^2' % ((currentyear[lastday-3] - currentyear[lastday-4])*1e6))
print('Day 3 = %s km^2' % ((currentyear[lastday-2] - currentyear[lastday-3])*1e6))
print('Day 2 = %s km^2' % ((currentyear[lastday-1] - currentyear[lastday-2])*1e6))
print('Day 1 = %s km^2' % ((currentyear[lastday] - currentyear[lastday-1])*1e6))
print('\n' 'Total 5-day Change = %s km^2' % ((currentyear[lastday]-currentyear[lastday-5])*1e6))
print('\n')
print('2016-1980 = %s km^2' % ((currentyear[lastday]*1e6) - mean1980[lastday]))
print('2016-2012 = %s km^2' % ((currentyear[lastday] - years[lastday,-5])*1e6))
print('\n')