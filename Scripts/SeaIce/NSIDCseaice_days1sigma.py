"""
Reads in current year's Arctic sea ice extent from Sea Ice Index 2 (NSIDC)

Website   : ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/daily/data/
Author    : Zachary M. Labe
Date      : 22 January 2018
"""

### Import modules
import numpy as np
import urllib.request
import urllib as UL
import datetime
import matplotlib.pyplot as plt

### Directory and time
directoryfigure = './Figures/'
directorydata = './Data/'
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday

### Load url
url = 'ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/daily/data/' \
    'N_seaice_extent_daily_v3.0.csv'

### Read file
raw_data = UL.request.urlopen(url)
dataset = np.genfromtxt(raw_data, skip_header=2,delimiter=',',
                        usecols=[0,1,2,3,4])
                        
print('\nCompleted: Read sea ice data!')                    

### Set missing data to nan
dataset[np.where(dataset==-9999)] = np.nan

### Variables
year = dataset[:,0]
month = dataset[:,1]
day = dataset[:,2]
ice = dataset[:,3]
missing = dataset[:,4]

yr2018 = np.where(year == 2018)[0]

ice18 = ice[yr2018]

### Ice Conversion
iceval = ice18 * 1e6
    
###########################################################################
###########################################################################
###########################################################################
### Reads in 1981-2010 means
### Load url
url2 = 'ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/daily/data/' \
       'N_seaice_extent_climatology_1981-2010_v3.0.csv'

### Read file
raw_data2 = UL.request.urlopen(url2)
dataset2 = np.genfromtxt(raw_data2, skip_header=2,delimiter=',',
                        usecols=[0,1,2,3,4,5,6,7])
                        
### Create variables
doy = dataset2[:,0]
meanice = dataset2[:,1] * 1e6
std = dataset2[:,2]

upper2std = (meanice[:365]/1e6)+(std[:365])
lower2std = (meanice[:365]/1e6)-(std[:365])

### Quartiles
quartile10 = dataset2[:,3]
quartile25 = dataset2[:,4]
quartile50 = dataset2[:,5]
quartile75 = dataset2[:,6]
quartile90 = dataset2[:,7]

### Anomalies
currentanom = iceval[-1]-meanice[currentdoy-2]

### Printing
print('Current anomaly = %s km^2 \n' % currentanom)

### Selecting years
yearsq = np.arange(1990,2018,1)
iceall = np.empty((28,365))
for i in range(yearsq.shape[0]):
    yrice = np.where(year == yearsq[i])[0]
    iceall[i,:] = ice[yrice][:365]
    
### Years below 2 sigma
minus = iceall - lower2std
minus[np.where(minus>=0)]=np.nan
minus[np.where(minus<0)]=1

minus18 = ice18 - lower2std[:len(ice18)]
minus18[np.where(minus18>=0)]=np.nan
minus18[np.where(minus18<0)]=1
minus18yr = np.count_nonzero(minus18 == 1)

minusall = []
for i in range(iceall.shape[0]):
    minusallq = np.count_nonzero(minus[i] == 1)
    minusall.append(minusallq)
    
minusallnew = minusall + [minus18yr]

###########################################################################
###########################################################################
###########################################################################
### Create plot
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='white')
plt.rc('xtick',color='white')
plt.rc('ytick',color='white')
plt.rc('axes',labelcolor='white')
plt.rc('axes',facecolor='black')

fig = plt.figure()
ax = plt.subplot(111)

xlabels = list(map(str,np.arange(1990,2021,5)))
plt.xticks(np.arange(0,36,5),xlabels,rotation=0)
ylabels = list(map(str,np.arange(0,391,30)))
plt.yticks(np.arange(0,391,30),ylabels)
plt.ylim([0,390])
plt.xlim([0,30])

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
        
ax.tick_params('both',length=5.5,width=2,which='major')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2) 

N = len(minusallnew)
ind = np.arange(N)
width = 0.9

ax.yaxis.grid(zorder=1,color='w',alpha=0.35)

rects = ax.bar(ind,minusallnew,width,color='dodgerblue',alpha=1,
               zorder=9,edgecolor='dodgerblue')
rects[-1].set_color('tomato')
rects[-1].set_edgecolor('tomato')

plt.ylabel(r'\textbf{Days below -1 std. dev.}',fontsize=15,
           color='darkgrey')
plt.title(r'\textbf{ARCTIC SEA ICE}',
                       fontsize=32,color='darkgrey') 

plt.text(-0.05,381.8,r'\textbf{DATA:} National Snow \& Ice Data Center, Boulder CO [\textbf{BASE:} 1981-2010]',
         fontsize=5.5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(-0.05,371.8,r'\textbf{SOURCE:} ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/',
         fontsize=5.5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(-0.05,361.8,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5.5,rotation='horizontal',ha='left',color='darkgrey')  

plt.text(28,36,r'$\star$',fontsize=18,color='tomato',ha='center',va='center')  
plt.text(-0.05,345,r'$\star$',fontsize=8,color='tomato',ha='left',va='center')  
plt.text(0.45,345,r'[as of 3/27/18]',fontsize=5.5,color='darkgrey',ha='left',va='center') 

plt.savefig(directoryfigure + 'nsidc_sie_days1sigma.png',dpi=300)      
    