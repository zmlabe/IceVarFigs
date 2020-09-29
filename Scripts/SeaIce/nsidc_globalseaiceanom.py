"""
Plot anomalies for Arctic and Antarctic sea ice extents of the current
year from Sea Ice Index 3 (NSIDC). Total anomaly (global) is also shown.

Website   : ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/daily/data/
Author    : Zachary M. Labe
Date      : 5 September 2016
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
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday

### Load url
url = 'ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/daily/data/' \
    'N_seaice_extent_daily_v3.0.csv'

### Read Arctic file
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
iceAR = dataset[:,3]
missing = dataset[:,4]

### Find current year
yr2018 = np.where(year == 2018)[0]
iceAR18 = iceAR[yr2018]

### Ice unit Conversion
icevalAR = iceAR18 * 1e6    

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
                        usecols=[0,1,2])
                        
### Create variables
doy = dataset2[:,0]
meaniceAR = dataset2[:,1] * 1e6
std = dataset2[:,2]

### Anomalies
currentanomAR = icevalAR-meaniceAR[:currentdoy-1]

###########################################################################
###########################################################################
###########################################################################
### Antarctic file

### Load url
url = 'ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/south/daily/data/' \
        'S_seaice_extent_daily_v3.0.csv'

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
iceAA = dataset[:,3]
missing = dataset[:,4]

### Find current year
yr2018 = np.where(year == 2018)[0]
iceAA18 = iceAA[yr2018]

### Ice Conversion
icevalAA = iceAA18 * 1e6
    
###########################################################################
###########################################################################
###########################################################################
### Reads in 1981-2010 means
### Load url
url2 = 'ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/south/daily/data/' \
       'S_seaice_extent_climatology_1981-2010_v3.0.csv'

### Read file
raw_data2 = UL.request.urlopen(url2)
dataset2 = np.genfromtxt(raw_data2, skip_header=2,delimiter=',',
                        usecols=[0,1,2])
                        
### Create variables
doy = dataset2[:,0]
meaniceAA = dataset2[:,1] * 1e6

### Anomalies
currentanomAA = icevalAA-meaniceAA[:currentdoy-1]

###########################################################################
###########################################################################
###########################################################################
### Total Anomaly
totalanom = (currentanomAR + currentanomAA) / 1e6
currentanomAR = currentanomAR/1e6
currentanomAA = currentanomAA/1e6

print('Completed script!')

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

xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan']
plt.xticks(np.arange(0,366,30.4),xlabels,rotation=0,fontsize=11)
ylabels = [r'-5',r'-4',r'-3',r'-2',r'-1',r'\textbf{0.0}',r'1',r'2',r'3',r'4',r'5']
plt.yticks(np.arange(-5,6,1),ylabels)
plt.ylim([-5,5])
plt.xlim([0,365])

strmonth = xlabels[int(currentmn)-1]
asof = strmonth + ' ' + currentdy + ', ' + currentyr

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

ax.yaxis.grid(zorder=1,color='w',alpha=0.35)

zeroline = [0]*len(doy)
plt.plot(doy,zeroline,linewidth=2,color='w',linestyle='--',
         zorder=1)

plt.plot(currentanomAR,linewidth=1.6,color='dodgerblue',
         label=r'Arctic',zorder=2)
plt.plot(currentanomAA,linewidth=1.6,color='m',
         label=r'Antarctic',zorder=3)

plt.plot(totalanom,linewidth=2.6,color='darkorange',zorder=8,
         label=r'Global') 
plt.scatter(doy[currentdoy-3],totalanom[-1],s=15,color='darkorange',zorder=9)
plt.scatter(doy[currentdoy-3],currentanomAR[-1],s=15,color='dodgerblue',zorder=9)
plt.scatter(doy[currentdoy-3],currentanomAA[-1],s=15,color='m',zorder=9)

plt.ylabel(r'\textbf{Extent Anomaly} [$\times$10$^{6}$ km$^2$]',fontsize=15,
           color='darkgrey')  
plt.title(r'\textbf{%s SEA ICE DEPARTURE}' % 2018,
                       fontsize=24,color='darkgrey')      
                       
le = plt.legend(shadow=False,fontsize=8,loc='upper left',
           bbox_to_anchor=(0.8084, 1.024),fancybox=True,frameon=False)
for text in le.get_texts():
    text.set_color('darkgrey')                          

plt.text(69,1.3,r'Global Anomaly $\approx$ %s km$^2$' % (format(totalanom[-1]*1e6,",f")[:-7]),
         fontsize=13,rotation='horizontal',ha='left',color='darkorange')
plt.text(0.5,-4.35,r'\textbf{DATA:} National Snow \& Ice Data Center, Boulder CO \textbf{[1981-2010 Baseline]}',
         fontsize=6,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0.5,-4.60,r'\textbf{SOURCE:} ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/',
         fontsize=6,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0.5,-4.85,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=6,rotation='horizontal',ha='left',color='darkgrey')    
fig.subplots_adjust(top=0.91)
 
### Save figure      
plt.savefig(directoryfigure + 'nsidc_sie_globalanom_year.png',dpi=300)                            