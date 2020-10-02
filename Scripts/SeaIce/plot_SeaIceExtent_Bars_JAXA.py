"""
Plots Arctic sea ice extent from June 2002-present using JAXA metadata
Website   : https://ads.nipr.ac.jp/vishop/vishop-extent.html
Author    : Zachary M. Labe
Date      : 9 August 2016
"""

### Import modules
import numpy as np
import urllib.request
import urllib as UL
import datetime
import matplotlib.pyplot as plt

### Directory and time
directoryfigure = './Figures/'
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
years     = dataset[1:,6:]
doy       = np.arange(0,len(day),1)

### Change units to million km^2
years = years/1e6

### Recent day of current year
currentyear = years[:,-1]
#lastday = np.where(np.isnan(currentyear[1:]))[0][0]
lastday = now.timetuple().tm_yday - 1
currentice = currentyear[lastday]

currentyear[10] = currentyear[9]
currentyear[59] = currentyear[58]

### Changes in sea ice
weekchange = currentice - currentyear[lastday-7]
daychange = currentice - currentyear[lastday-1]

print('--- JAXA Arctic Sea Ice Extent Min Years ---')
print('\nCurrent Date =', now.strftime("%Y-%m-%d %H:%M"))
print('Current SIE = %s km^2 \n' % (currentice*1e6))

### Calculate minimums
mins = years[lastday,:]
    
### Add current year
currentline = [currentice]*years.shape[1]
mean1980line = [mean1980[lastday]/1e6] * years.shape[1]
mean1990line = [mean1990[lastday]/1e6] * years.shape[1]
mean2000line = [mean2000[lastday]/1e6] * years.shape[1]

### Define parameters (dark)
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='white')
plt.rc('xtick',color='white')
plt.rc('ytick',color='white')
plt.rc('axes',labelcolor='white')
plt.rc('axes',facecolor='black')

### Plot sea ice extent
fig = plt.figure()
ax = plt.subplot(111)

N = len(mins)
ind = np.arange(N)
width = 0.9

### Adjust axes in time series plots 
def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', -7))
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
ax.spines['bottom'].set_color('none')
ax.tick_params('both',length=5.5,width=2,which='major')
ax.spines['left'].set_linewidth(2)
ax.tick_params(labelbottom='off')
plt.setp(ax.get_xticklines()[0:-1],visible=False)

rects = ax.bar(ind,mins,width,color='tomato',alpha=1,
               zorder=1)
line = ax.plot(currentline,linestyle='--',color='yellowgreen',
               linewidth=2,zorder=3)
line80 = ax.plot(mean1980line,linestyle='--',color='w',
               linewidth=2,zorder=3)
line90 = ax.plot(mean1990line,linestyle='--',color='w',
               linewidth=2,zorder=3)
line00 = ax.plot(mean2000line,linestyle='--',color='w',
               linewidth=2,zorder=3)

### Check mins
belowyr = np.where(mins >= currentice)[0]

### Set color
for i in range(len(belowyr)):
    rects[belowyr[i]].set_color('dodgerblue')
    rects[belowyr[i]].set_edgecolor('black')
rects[-1].set_color('yellowgreen')

### Set y-axis labels
plt.yticks(np.arange(0,17,1),map(str,np.arange(0,17,1)))
plt.ylabel(r'\textbf{Extent} ($\times$10$^6$ km$^2)$',fontsize=16,
           color='w',alpha=0.6)

plt.ylim([int(np.nanmin(years[lastday,:]))-3,int(np.nanmin(years[lastday,:]))+3])

### Set font styles
labely = int(np.nanmin(years[lastday,:]))-3.34
labely2 = int(np.nanmin(years[lastday,:]))-3.55
labely3 = int(np.nanmin(years[lastday,:]))-3.7
labely4 = int(np.nanmin(years[lastday,:]))+3.25

plt.text(-0.3,labely,'03',color='w',fontsize=13)
plt.text(0.68,labely,'04',color='w',fontsize=13)
plt.text(1.66,labely,'05',color='w',fontsize=13)
plt.text(2.64,labely,'06',color='w',fontsize=13)
plt.text(3.62,labely,r'\textbf{07}',color='w',fontsize=13)
plt.text(4.64,labely,'08',color='w',fontsize=13)
plt.text(5.64,labely,'09',color='w',fontsize=13)
plt.text(6.66,labely,'10',color='w',fontsize=13)
plt.text(7.75,labely,'11',color='w',fontsize=13)
plt.text(8.75,labely,r'\textbf{12}',color='w',fontsize=13)
plt.text(9.75,labely,'13',color='w',fontsize=13)
plt.text(10.75,labely,'14',color='w',fontsize=13)
plt.text(11.75,labely,'15',color='w',fontsize=13)
plt.text(12.75,labely,r'\textbf{16}',color='w',fontsize=13)
plt.text(13.75,labely,r'\textbf{17}',color='w',fontsize=13)
plt.text(14.75,labely,r'\textbf{18}',color='yellowgreen',fontsize=13)
plt.text(-0.4,labely2,r'\textbf{DATA:} JAXA (Arctic Data archive System, NIPR)',
         fontsize=6,rotation='horizontal',ha='left',color='darkgrey')
plt.text(-0.4,labely3,r'\textbf{SOURCE:} https://ads.nipr.ac.jp/vishop/vishop-extent.html',
         fontsize=6,rotation='horizontal',ha='left',color='darkgrey')
plt.text(14.55,labely2,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=6,rotation='horizontal',ha='right',color='darkgrey') 
plt.text(14.1,currentice+0.3,r'Current',color='yellowgreen')
plt.text(2.5,labely4,r'\textbf{ARCTIC SEA ICE - %s/%s' % (currentmn,currentdy),
                       fontsize=20,color='w',alpha=0.6) 

plt.text(12.6,(mean1980[lastday]/1e6)+0.04,r'Mean 1980s',color='w')
plt.text(12.6,(mean1990[lastday]/1e6)+0.04,r'Mean 1990s',color='w')
plt.text(12.6,(mean2000[lastday]/1e6)+0.04,r'Mean 2000s',color='w')

### Save figure 
plt.savefig(directoryfigure + 'Bars_SIE_JAXA.png',dpi=500)              

print('Completed script!')    