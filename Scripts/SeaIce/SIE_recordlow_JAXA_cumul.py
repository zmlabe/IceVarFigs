"""
Calculates current year percentage of record daily low SIE 2002-present 
using JAXA metadata

Website   : https://ads.nipr.ac.jp/vishop/vishop-extent.html
Author    : Zachary M. Labe
Date      : 23 March 2018
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as c
import urllib as UL
import datetime
import cmocean

### Directory and time
directoryfigure = '/home/zlabe/Documents/Projects/IceVarFigs/Figures/' 
directorydata = '/home/zlabe/Documents/Projects/IceVarFigs/Data/'   
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

### Time
yearq = np.arange(2002,2018+1,1)
yearqq = np.arange(2007,2018+1,1)

### Calculate record low SIE
recordlow = np.empty((12,years.shape[0]))
recordlow.fill(np.nan)
for j in range(12):
    for i in range(365):
        if years[i,5+j] == np.nanmin(years[i,:6+j]):
            recordlow[j,i] = 1.
        else: 
            recordlow[j,i] = 0.
            
recordlowq = np.cumsum(recordlow,axis=1)

###########################################################################
###########################################################################
###########################################################################
### Create plot
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='darkgrey')
plt.rc('xtick',color='white')
plt.rc('ytick',color='white')
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
        
xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan']

fig = plt.figure()
ax = plt.subplot(111)

ax.tick_params('both',length=5.5,width=2,which='major',color='darkgrey')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2) 

plt.vlines(lastday-1,linewidth=2,color='darkgrey',alpha=1,ymin=0,
            ymax=184,zorder=1)

color=cmocean.cm.haline(np.linspace(0.1,1,recordlowq.shape[0]))
for i,c in zip(range(recordlowq.shape[0]),color):
    if i == (recordlowq.shape[0]-1):
        c = 'red'
        l = 2.9
        aaa = 1
        line='--'
        plt.plot(recordlowq[i,:lastday],c=c,linewidth=l,zorder=3,alpha=aaa,
                 dashes=(1, 0.2),linestyle=line)
#    elif i == (recordlowq.shape[0]-2):
#        c = 'darkorange'
#        l = 2.9
#        aaa = 1
    else:
        l = 1.5 
        aaa = 1
        plt.plot(recordlowq[i,:],c=c,linewidth=l,zorder=2,alpha=aaa)
    if yearqq[i] == 2008:
        plt.text(387,np.nanmax(recordlowq[i,:])-3,
             r'\textbf{%s}' % yearqq[i],fontsize=9,color=c)
    elif yearqq[i] == 2009:
        plt.text(364.5,np.nanmax(recordlowq[i,:])+1.5,
             r'\textbf{%s}' % yearqq[i],fontsize=9,color=c)
    elif yearqq[i] == 2010:
        plt.text(364.5,np.nanmax(recordlowq[i,:])-5.3,
             r'\textbf{%s}' % yearqq[i],fontsize=9,color=c)
    elif yearqq[i] == 2017:
        plt.text(387,np.nanmax(recordlowq[i,:])-3,
             r'\textbf{%s}' % yearqq[i],fontsize=9,color=c)
    elif yearqq[i] == 2018:
        plt.text(lastday+2.8,np.nanmax(recordlowq[i,:]+3.6),
             r'\textbf{%s}' % yearqq[i],fontsize=11,color=c)
    else:
        plt.text(364.5,np.nanmax(recordlowq[i,:])-3,
             r'\textbf{%s}' % yearqq[i],fontsize=9,color=c)
    
plt.scatter(lastday-1,recordlowq[-1,lastday],color='r',s=25,zorder=3)
    
xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan']
plt.xticks(np.arange(0,361,30.4),xlabels,rotation=0)
ylabels = list(map(str,np.arange(0,201,50)))
plt.yticks(np.arange(0,201,50),ylabels)
plt.ylim([0,200])
plt.xlim([0,365])

plt.title(r'\textbf{RECORD LOW ARCTIC SEA ICE}',
                       fontsize=24,color='darkgrey')    

plt.text(0,196,r'\textbf{DATA:} JAXA AMSR2 (Arctic Data archive System, NIPR, 2002-2018)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0,191,r'\textbf{SOURCE:} https://ads.nipr.ac.jp/vishop/vishop-extent.html',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0,186,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')  

plt.ylabel(r'\textbf{Number of Days}',
           fontsize=18,alpha=1,color='darkgrey',rotation=90) 
       
plt.savefig(directoryfigure + 'SIE_record_cumul_JAXA.png',dpi=300)  

print('Completed: Script done!')    