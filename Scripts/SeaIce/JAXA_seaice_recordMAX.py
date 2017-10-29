"""
Plots Arctic the climatological maximum sea ice extent from June 2002-present 
using JAXA metadata

Website   : https://ads.nipr.ac.jp/vishop/vishop-extent.html
Author    : Zachary M. Labe
Date      : 15 May 2016
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
lastday = now.timetuple().tm_yday -1
currentice = currentyear[lastday]
currentanom = currentice - (mean1980[lastday]/1e6)

### Fill in missing days
currentyear[10] = currentyear[9]
currentyear[59] = currentyear[58]

### Changes in the last week/day
weekchange = currentice - currentyear[lastday-7]
daychange = currentice - currentyear[lastday-1]

###############################################################################
###############################################################################
###############################################################################
### Make plot
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

oldaverage = currentyear.copy()
oldaverage[lastday:] = currentyear[lastday]

### Calculate 2000s average
average2000s = mean2000.copy()
average2000s[lastday:] = mean2000[lastday]
average2000s = average2000s/1e6
oldmin = np.where(mean2000 == np.min(mean2000))[0]

### Calculate 1990s average
average1990s = mean1990.copy()
average1990s[lastday:] = mean1990[lastday]
average1990s = average1990s/1e6

### Calculate 1980s average
average1980s = mean1980.copy()
average1980s[lastday:] = mean1980[lastday]
average1980s = average1980s/1e6

### Find max sea ice extents
maxyr = np.empty((years.shape[1]))
for i in range(years.shape[1]):
    maxyr[i] = np.nanmax(years[:,i])
    
maxwhere = np.empty((years.shape[1]))
for i in range(years.shape[1]):
    maxwhere[i] = np.where(years[:,i] == maxyr[i])[0]

plt.scatter(maxwhere[:],maxyr[:],c=maxyr[:],s=50,
            cmap='inferno',zorder=10)

pl = ax.plot(doy,currentyear,linewidth=2.9,zorder=3,
              color='r',)
                  
plt.scatter(maxwhere[-1],maxyr[-1],s=50,
            color='r',zorder=10)          
            
plt.plot(doy,mean1980/1e6,linewidth=3,linestyle='--',
         color='darkmagenta',label=r'1980s Mean',alpha=0.8)
plt.plot(doy,mean1990/1e6,linewidth=3,linestyle='--',
         color='c',label=r'1990s Mean',alpha=0.8)
plt.plot(doy,mean2000/1e6,linewidth=3,linestyle='--',
         color='dodgerblue',label=r'2000s Mean',alpha=0.8)

### Manual labeling to make plot look prettier
labels = list(map(str,np.arange(2002,2018,1)))

plt.text(maxwhere[1]+0.07,maxyr[1]+0.07,r'\textbf{%s}' % labels[1],color='w',fontsize=7)
plt.text(maxwhere[2]+1,maxyr[2]+0.05,r'\textbf{%s}' % labels[2],color='w',fontsize=7)
plt.text(maxwhere[3]+0.07,maxyr[3]+0.07,r'\textbf{%s}' % labels[3],color='w',fontsize=7)
plt.text(maxwhere[4]+0.07,maxyr[4]+0.07,r'\textbf{%s}' % labels[4],color='w',fontsize=7)
plt.text(maxwhere[5]+0.07,maxyr[5]+0.07,r'\textbf{%s}' % labels[5],color='w',fontsize=7)
plt.text(maxwhere[6]+0.07,maxyr[6]+0.07,r'\textbf{%s}' % labels[6],color='w',fontsize=7)
plt.text(maxwhere[7]-4,maxyr[7]+0.07,r'\textbf{%s}' % labels[7],color='w',fontsize=7)
plt.text(maxwhere[8]+0.07,maxyr[8]+0.07,r'\textbf{%s}' % labels[8],color='w',fontsize=7)
plt.text(maxwhere[9]+0.07,maxyr[9]+0.07,r'\textbf{%s}' % labels[9],color='w',fontsize=7)
plt.text(maxwhere[10]-4,maxyr[10]+0.07,r'\textbf{%s}' % labels[10],color='w',fontsize=7)
plt.text(maxwhere[11]+0.07,maxyr[11]+0.07,r'\textbf{%s}' % labels[11],color='w',fontsize=7)
plt.text(maxwhere[12]+0.07,maxyr[12]+0.07,r'\textbf{%s}' % labels[12],color='w',fontsize=7)
plt.text(maxwhere[13]+0.07,maxyr[13]+0.07,r'\textbf{%s}' % labels[13],color='w',fontsize=7)
plt.text(maxwhere[14]+0.07,maxyr[14]+0.07,r'\textbf{%s}' % labels[14],color='w',fontsize=7)
plt.text(maxwhere[15]+0.07,maxyr[15]+0.07,r'\textbf{%s}' % labels[15],color='r',fontsize=7)

plt.text(maxwhere[15]+5,maxyr[15]+0.08,r'$\longleftarrow$',color='r',fontsize=11)

### Define text
xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan'] 

strmonth = xlabels[int(currentmn)-1]
asof = strmonth + ' ' + currentdy + ', ' + currentyr

plt.text(30.8,15.91,r'\textbf{DATA:} JAXA (Arctic Data archive System, NIPR)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(30.8,15.84,r'\textbf{SOURCE:} https://ads.nipr.ac.jp/vishop/vishop-extent.html',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(30.8,15.77,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')                
           
adjust_spines(ax, ['left', 'bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
plt.ylabel(r'\textbf{Extent [$\bf{\times 10^{6}}$\ \textbf{km}$\bf{^2}$]}',
           fontsize=15,color='darkgrey')
l = plt.legend(shadow=False,fontsize=7.5,loc='upper left',
           bbox_to_anchor=(0.785, 1.02),fancybox=True,ncol=1,frameon=False)
for text in l.get_texts():
    text.set_color('darkgrey')           

plt.xticks(np.arange(0,366,30.4),xlabels,rotation=0,fontsize=11)
ylabels = map(str,np.arange(2,18,1))
plt.yticks(np.arange(2,18,1),ylabels,fontsize=13)
plt.ylim([13,16])
plt.xlim([30.4,121.6])
ax.grid(zorder=1,color='w',alpha=0.3)
fig.suptitle(r'\textbf{ARCTIC SEA ICE ANNUAL MAX}',
                       fontsize=22,color='darkgrey')
ax.tick_params('both',length=5.5,width=2,which='major')

### Save figure
plt.savefig(directoryfigure + 'JAXA_seaice_recordMAX.png',dpi=900)

### Print additional information
print('\n')
print('----JAXA Sea Ice Change----')
print('Day 5 = %s km^2' % ((currentyear[lastday-4] - currentyear[lastday-5])*1e6))
print('Day 4 = %s km^2' % ((currentyear[lastday-3] - currentyear[lastday-4])*1e6))
print('Day 3 = %s km^2' % ((currentyear[lastday-2] - currentyear[lastday-3])*1e6))
print('Day 2 = %s km^2' % ((currentyear[lastday-1] - currentyear[lastday-2])*1e6))
print('Day 1 = %s km^2' % ((currentyear[lastday] - currentyear[lastday-1])*1e6))
print('\n' 'Total 5-day Change = %s km^2 \n' % ((currentyear[lastday]-currentyear[lastday-5])*1e6))

print('2017-1980 = %s km^2' % ((currentyear[lastday]*1e6) - mean1980[lastday]))
print('2017-1990 = %s km^2' % ((currentyear[lastday]*1e6) - mean1990[lastday]))
print('2017-2000 = %s km^2' % ((currentyear[lastday]*1e6) - mean2000[lastday]))
print('\n')