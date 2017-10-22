"""
Plots Arctic sea ice extent from June 2002-present using JAXA metadata

Website   : https://ads.nipr.ac.jp/vishop/vishop-extent.html
Author    : Zachary M. Labe
Date      : 4 August 2016
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import datetime
import urllib as UL

### Directory and time
directory = '/home/zlabe/Documents/Projects/Tests/'
source = 'twitter'
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
#lastday = np.where(np.isnan(currentyear[1:]))[0][0]
lastday = now.timetuple().tm_yday -1
currentice = currentyear[lastday]
currentanom = currentice - (mean1980[lastday]/1e6)

currentyear[10] = currentyear[9]
currentyear[59] = currentyear[58]

### Changes 
weekchange = currentice - currentyear[lastday-7]
daychange = currentice - currentyear[lastday-1]

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
        
plt.plot(doy,mean1980/1e6,linewidth=1,linestyle='--',
         color='darkmagenta',label=r'1980s Mean',zorder=1)
plt.plot(doy,mean1990/1e6,linewidth=1,linestyle='--',
         color='c',label=r'1990s Mean',zorder=1)
plt.plot(doy,mean2000/1e6,linewidth=1,linestyle='--',
         color='dodgerblue',label=r'2000s Mean',zorder=1) 

bar4, = ax.plot(doy,years[:,-2],color='r',label=r'Year 2016',linewidth=1.8,
                alpha=1,zorder=3)        
bar2, = ax.plot(doy,years[:,-6],color='yellowgreen',label=r'Year 2012',linewidth=1.8,
                alpha=1,zorder=3)
bar3, = ax.plot(doy,years[:,5],color='white',label=r'Year 2007',linewidth=1.8,
                alpha=1,zorder=2)
bar, = ax.plot(doy,currentyear,linewidth=2.5,zorder=4,color='darkorange')

plt.scatter(doy[lastday],currentyear[lastday],
            s=25,color='darkorange',zorder=4)
            

xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan'] 
strmonth = xlabels[int(currentmn)-1]
asof = strmonth + ' ' + currentdy + ', ' + currentyr

plt.text(0.6,3.9,r'\textbf{DATA:} JAXA (Arctic Data archive System, NIPR)',
         fontsize=6,rotation='horizontal',ha='left',color='w',alpha=0.6)
plt.text(0.6,3.5,r'\textbf{SOURCE:} https://ads.nipr.ac.jp/vishop/vishop-extent.html',
         fontsize=6,rotation='horizontal',ha='left',color='w',alpha=0.6)
plt.text(0.6,3.1,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=6,rotation='horizontal',ha='left',color='w',alpha=0.6)  
         
### Insert sea ice text                        
if lastday <= 365:
    xcord = 120
    ycord = 10
    plt.text(xcord-4,ycord-0.65,r'\textbf{%s}' '\n' r'\textbf{%s} \textbf{km}$^2$' \
    % (asof,format(currentice*1e6,",f")[:-7]),fontsize=10,
        rotation='horizontal',ha='right',color='w',alpha=0.6)
    
if lastday <= 365:
    plt.text(xcord-4,ycord-2.5,r'\textbf{7--day change}'\
        '\n' r'\textbf{%s} \textbf{km}$^2$'\
        % (format(weekchange*1e6,",f")[:-7]),fontsize=10,
        rotation='horizontal',ha='right',color='w',alpha=0.6) 
    plt.text(xcord-4,ycord-4,r'\textbf{1--day change}' \
        '\n' r'\textbf{%s} \textbf{km}$^2$'\
        % (format((daychange*1e6),",f")[:-7]),fontsize=10,
        rotation='horizontal',ha='right',color='w',alpha=0.6) 
           
adjust_spines(ax, ['left', 'bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
plt.ylabel(r'\textbf{Extent [$\bf{\times}$10$^{6}$\ \textbf{km}$^2$]}',
           fontsize=15,alpha=0.6)
l = plt.legend(shadow=False,fontsize=6,loc='upper left',
           bbox_to_anchor=(0.655, 1.013),fancybox=True,ncol=2)
for text in l.get_texts():
    text.set_color('w')             

plt.xticks(np.arange(0,361,30),xlabels,rotation=0,fontsize=10)
ylabels = map(str,np.arange(2,18,1))
plt.yticks(np.arange(2,18,1),ylabels,fontsize=10)
plt.ylim([3,16])
plt.xlim([0,300])
ax.grid(zorder=1,color='w',alpha=0.2)
fig.suptitle(r'\textbf{ARCTIC SEA ICE}',
                       fontsize=25,color='w',alpha=0.6) 
ax.tick_params('both',length=5.5,width=2,which='major')

year2012 = years[:,-6]
year2007 = years[:,5]
year2016 = years[:,-2]
def update(num,doy,currentyear,year2016,year2012,year2007,bar,bar2,bar4):
    bar.set_data(doy[:num+1],currentyear[:num+1])
    bar.axes.axis([0,300,3,16])
    bar2.set_data(doy[:num+1],year2012[:num+1])
    bar2.axes.axis([0,300,3,16])
    bar3.set_data(doy[:num+1],year2007[:num+1])
    bar3.axes.axis([0,300,3,16])
    bar4.set_data(doy[:num+1],year2016[:num+1])
    bar4.axes.axis([0,300,3,16])
    return bar,

ani = animation.FuncAnimation(fig,update,310,fargs=[doy,currentyear,year2016,year2012,year2007,bar,bar2,bar4],
                              interval=.001,blit=True)

ani.save(directory + 'moving_SIE_JAXA.gif',dpi=150)

print('\n')
print('JAXA Sea Ice Loss Missing Days')
print('Day 5 Loss = %s km^2' % ((currentyear[lastday-4] - currentyear[lastday-5])*1e6))
print('Day 4 Loss = %s km^2' % ((currentyear[lastday-3] - currentyear[lastday-4])*1e6))
print('Day 3 Loss = %s km^2' % ((currentyear[lastday-2] - currentyear[lastday-3])*1e6))
print('Day 2 Loss = %s km^2' % ((currentyear[lastday-1] - currentyear[lastday-2])*1e6))
print('Day 1  Loss = %s km^2' % ((currentyear[lastday] - currentyear[lastday-1])*1e6))
print('\n' 'Total 5-day Loss = %s km^2' % ((currentyear[lastday]-currentyear[lastday-5])*1e6))
print('\n') 