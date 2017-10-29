"""
Plots Arctic daily sea ice extent from June 2002-present using JAXA metadata

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

currentyear[10] = currentyear[9]
currentyear[59] = currentyear[58]

### Changes in the last day and week
weekchange = currentice - currentyear[lastday-7]
daychange = currentice - currentyear[lastday-1]

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

oldaverage = currentyear.copy()
oldaverage[lastday:] = currentyear[lastday]

### 2000s average
average2000s = mean2000.copy()
average2000s[lastday:] = mean2000[lastday]
average2000s = average2000s/1e6
oldmin = np.where(mean2000 == np.min(mean2000))[0]

### 1990s average
average1990s = mean1990.copy()
average1990s[lastday:] = mean1990[lastday]
average1990s = average1990s/1e6

### 1980s average
average1980s = mean1980.copy()
average1980s[lastday:] = mean1980[lastday]
average1980s = average1980s/1e6

difference = (oldmin - lastday)[0]

### Are we below decadal climatological min?
if (currentyear[lastday]*1e6) < np.nanmin(mean1980):
    print( True, '1980')
if (currentyear[lastday]*1e6) < np.nanmin(mean1990):
    print(True, '1990')
if (currentyear[lastday]*1e6) < np.nanmin(mean2000):
    print(True, '2000')
    
### Calculate record low SIE
recordlow = np.empty((years.shape[0]))
for i in range(years.shape[0]):
    if years[i,-1] == np.nanmin(years[i,:]):
        recordlow[i] = 1.
    else: 
        recordlow[i] = 0.

### Begin plot
plt.plot(doy,years[:,:],color='w',linewidth=0.15,
         linestyle='-',alpha=0.7)

bar = ax.plot(doy,currentyear,linewidth=2.9,zorder=3,
              color='darkorange',)
                  
plt.scatter(doy[lastday],currentyear[lastday],
            s=20,color='darkorange',zorder=4)
plt.scatter(doy[lastday],mean2000[lastday]/1e6,
            s=20,color='dodgerblue',zorder=11)   
plt.scatter(doy[lastday],mean1990[lastday]/1e6,
            s=20,color='c',zorder=11)  
plt.scatter(doy[lastday],mean1980[lastday]/1e6,
            s=20,color='darkmagenta',zorder=11)             
            
plt.plot(doy,mean1980/1e6,linewidth=1.8,linestyle='-',
         color='darkmagenta',label=r'1980s Mean')
plt.plot(doy,mean1990/1e6,linewidth=1.8,linestyle='-',
         color='c',label=r'1990s Mean')
plt.plot(doy,mean2000/1e6,linewidth=1.8,linestyle='-',
         color='dodgerblue',label=r'2000s Mean')  

plt.plot(oldaverage,color='darkorange',linestyle=':',linewidth=2.8,zorder=5)
plt.plot(average2000s,color='dodgerblue',linestyle=':',linewidth=1.8,zorder=11)
plt.plot(average1990s,color='c',linestyle=':',linewidth=1.8,zorder=11)
plt.plot(average1980s,color='darkmagenta',linestyle=':',linewidth=1.8,zorder=11)

### Define date
xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan'] 

strmonth = xlabels[int(currentmn)-1]
asof = strmonth + ' ' + currentdy + ', ' + currentyr

### Add additional information to the plot
xcord = 109
ycord = 9.4
if recordlow[lastday] == 1.0:
    plt.text(xcord + 2,ycord,r'\textbf{[*Record Low*]}',fontsize=11,
             rotation='horizontal',ha='left',color='aqua')

xcord = lastday - 5.5
ycord = round(currentice)-0.8
plt.text(183.4,1.80,r'\textbf{DATA:} JAXA 2002-2017 (Arctic Data archive System, NIPR)',
         fontsize=5,rotation='horizontal',ha='left',color='w',alpha=0.6)
plt.text(183.4,1.50,r'\textbf{SOURCE:} https://ads.nipr.ac.jp/vishop/vishop-extent.html',
         fontsize=5,rotation='horizontal',ha='left',color='w',alpha=0.6)
plt.text(183.4,1.20,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='left',color='w',alpha=0.6)

plt.text(doy[lastday]+5,currentyear[lastday]-0.8,r'\textbf{$\bf{\longrightarrow}$}',
             fontsize=18,rotation=65,ha='right',color='darkorange')
plt.text(334.6,currentyear[lastday]-0.2,r'\textbf{CURRENT}',
             fontsize=9.5,rotation='horizontal',ha='left',
             color='darkorange',alpha=1) 
plt.text(334.6,mean2000[lastday]/1e6-0.2,r'2000s',
             fontsize=10,rotation='horizontal',ha='left',
             color='dodgerblue') 
plt.text(334.6,mean1990[lastday]/1e6-0.2,r'1990s',
             fontsize=10,rotation='horizontal',ha='left',
             color='c')  
plt.text(334.6,mean1980[lastday]/1e6-0.2,r'1980s',
             fontsize=10,rotation='horizontal',ha='left',
             color='darkmagenta')              
           
adjust_spines(ax, ['left', 'bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.tick_params(axis='both', direction='out',length=5.5,width=2,
               which='major',pad=7)

plt.ylabel(r'\textbf{Extent [$\bf{\times 10^{6}}$\ \textbf{km}$\bf{^2}$]}',
           fontsize=15,alpha=0.6)
l = plt.legend(shadow=False,fontsize=8.5,loc='lower left',
           bbox_to_anchor=(0.768, -0.025),fancybox=True,ncol=1,
            frameon=False)
for text in l.get_texts():
    text.set_color('w') 
    text.set_alpha(0.6)         

plt.xticks(np.arange(0,366,30.4),xlabels,rotation=0,fontsize=11)
ylabels = map(str,np.arange(1,18,1))
plt.yticks(np.arange(1,18,1),ylabels,fontsize=13)
plt.ylim([1,13])
plt.xlim([182.35,334.4])
fig.suptitle(r'\textbf{ARCTIC SEA ICE}',fontsize=28,color='w',alpha=0.6) 

plt.savefig(directoryfigure + 'JAXA_seaice_means_xe5.png',dpi=900)

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