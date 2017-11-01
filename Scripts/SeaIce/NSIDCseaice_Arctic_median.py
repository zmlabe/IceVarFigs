"""
Reads in current year's Arctic sea ice extent from Sea Ice Index 3 (NSIDC) 
and calculates the anomaly from the 1981-2010 median

Website   : ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/daily/data/
Author    : Zachary M. Labe
Date      : 5 September 2016
"""

### Import modules
import numpy as np
import urllib as UL
import datetime
import matplotlib.pyplot as plt

### Directory and time
directoryfigure = '/home/zlabe/Documents/Projects/IceVarFigs/Figures/' 
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

### Find current year (2017)
yr2017 = np.where(year == 2017)[0]
sie17 = ice[yr2017]

### Ice Conversion
iceval = sie17 * 1e6

### Printing info
print('\n----- NSIDC Arctic Sea Ice -----')
print('Current Date =', now.strftime("%Y-%m-%d %H:%M"), '\n')

print('SIE Date    = %s/%s/%s' % (int(month[-1]),int(day[-1]),int(year[-1])))
print('Current SIE = %s km^2 \n' % (iceval[-1]))

print('1-day change SIE = %s km^2' % (iceval[-1]-iceval[-2]))
print('7-day change SIE = %s km^2 \n' % (iceval[-1]-iceval[-8]))
    
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

### Quartiles
quartile10 = dataset2[:,3]
quartile25 = dataset2[:,4]
quartile50 = dataset2[:,5]
quartile75 = dataset2[:,6]
quartile90 = dataset2[:,7]

### Anomalies
currentanom = iceval[-1]-meanice[currentdoy-2]

### Printing info
print('Current anomaly = %s km^2 \n' % currentanom)   

### Finding select years since 2012
yr2012 = np.where(year == 2012)[0]
yr2013 = np.where(year == 2013)[0]
yr2014 = np.where(year == 2014)[0]
yr2015 = np.where(year == 2015)[0]
yr2016 = np.where(year == 2016)[0]

### Calculate anomaly from their median
sie12 = ice[yr2012] - quartile50
sie13 = ice[yr2013] - quartile50[:-1]
sie14 = ice[yr2014] - quartile50[:-1]
sie15 = ice[yr2015] - quartile50[:-1]
sie16 = ice[yr2016] - quartile50
sie17 = sie17 - quartile50[:len(sie17)]

### Append years to extented list
extend5 = np.append(sie12,sie13,axis=0)
extend4 = np.append(extend5,sie14,axis=0)
extend3 = np.append(extend4,sie15,axis=0)
extend2 = np.append(extend3,sie16,axis=0)
extend1 = np.append(extend2,sie17,axis=0)

### Find median to plot
median = np.tile(quartile50,6)

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

xlabels = map(str,np.arange(2012,2019,1))
plt.xticks(np.arange(0,2555,365),xlabels,rotation=0)
ylabels = [r'-5',r'-4',r'-3',r'-2',r'-1',r'\textbf{0.0}',r'1',r'2',r'3',r'4',r'5']
plt.yticks(np.arange(-5,6,1),ylabels)
plt.ylim([-5,5])
plt.xlim([0,2190])

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
        
ax.tick_params('both',length=7.5,width=2,which='major')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')  
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)

upper2std = (meanice/1e6)+(std*2)
lower2std = (meanice/1e6)-(std*2)

ax.yaxis.grid(zorder=1,color='w',alpha=0.35)

zeroline = [0]*2191

recdiff_masked = np.ma.masked_less_equal(extend1, 0)

plt.bar(np.arange(len(extend1)),extend1,color='r',
        edgecolor='r',zorder=9) 
plt.bar(np.arange(len(extend1)),recdiff_masked.filled(np.nan),
        color='dodgerblue',edgecolor='dodgerblue',zorder=10) 

plt.ylabel(r'\textbf{Extent Anomalies} [$\times$10$^{6}$ km$^2$]',fontsize=13,
           color='darkgrey')

plt.title(r'\textbf{ARCTIC SEA ICE EXTENT ANOMALIES}',
                       fontsize=20,color='darkgray') 
                       
plt.text(1095,0.25,r'\textbf{1981-2010 Climatology}',fontsize=8,
         rotation=0,ha='center',color='darkgrey')                        
plt.text(155,0.8,r'$\bf{\rightarrow}$',fontsize=35,rotation=230,ha='center',
        color='dodgerblue')    
plt.text(len(extend1)+30,-0.27,r'\textbf{Today!}',fontsize=8,rotation=270,ha='center',
        color='r')                    

plt.text(0.5,-4.45,r'\textbf{DATA:} National Snow \& Ice Data Center, Boulder CO',
         fontsize=6,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0.5,-4.70,r'\textbf{CSV:} ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/',
         fontsize=6,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0.5,-4.95,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=6,rotation='horizontal',ha='left',color='darkgrey')    
fig.subplots_adjust(top=0.91)
        
plt.savefig(directoryfigure + 'nsidc_sie_median.png',dpi=300)     