"""
Reads in current year's Antarctic sea ice extent from Sea Ice Index 3 (NSIDC)

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
ice = dataset[:,3]
missing = dataset[:,4]

yr2018 = np.where(year == 2018)[0]

sie18 = ice[yr2018]

### Ice Conversion
iceval = sie18 * 1e6

### Printing
print('\n----- NSIDC Antarctic Sea Ice -----')
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
url2 = 'ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/south/daily/data/' \
       'S_seaice_extent_climatology_1981-2010_v3.0.csv'

### Read file
raw_data2 = UL.request.urlopen(url2)
dataset2 = np.genfromtxt(raw_data2, skip_header=2,delimiter=',',
                        usecols=[0,1,2,3,4,5,6,7])
                        
### Create variables
doy = dataset2[:,0]
meanice = dataset2[:,1] * 1e6
std = dataset2[:,2]

### Anomalies
currentanom = iceval[-1]-meanice[currentdoy-2]

### Quartiles
quartile10 = dataset2[:,3]
quartile25 = dataset2[:,4]
quartile50 = dataset2[:,5]
quartile75 = dataset2[:,6]
quartile90 = dataset2[:,7]

yr2007 = np.where(year == 2007)[0]
yr2012 = np.where(year == 2012)[0]
yr2016 = np.where(year == 2016)[0]

sie7 = ice[yr2007]
sie12 = ice[yr2012]
sie16 = ice[yr2016]

### Printing
print('Current anomaly = %s km^2 \n' % currentanom)   

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
plt.xticks(np.arange(0,361,30.4),xlabels,rotation=0)
ylabels = map(str,np.arange(0,24,2))
plt.yticks(np.arange(0,24,2),ylabels)
plt.ylim([0,22])
plt.xlim([0,360])

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

upper2std = (meanice/1e6)+(std*2)
lower2std = (meanice/1e6)-(std*2)

ax.grid(zorder=1,color='w',alpha=0.25)

plt.plot(sie18,linewidth=1.8,color='aqua',zorder=9,label=r'Current Year (2018)') 
plt.plot(doy,upper2std,color='white',alpha=0.7,zorder=3,linewidth=0.01)
plt.plot(doy,lower2std,color='white',alpha=0.7,zorder=4,linewidth=0.01)
plt.plot(doy,quartile10,color='m',alpha=0.7,zorder=3,linewidth=0.01)
plt.plot(doy,quartile25,color='cornflowerblue',alpha=0.7,zorder=4,linewidth=0.01)
plt.plot(doy,quartile75,color='cornflowerblue',alpha=0.7,zorder=4,linewidth=0.01)
plt.plot(doy,quartile90,color='m',alpha=0.7,zorder=3,linewidth=0.01)

ax.fill_between(doy, lower2std, upper2std, facecolor='white', alpha=0.35,
                label=r'$\pm$2 standard deviations',zorder=2)
plt.plot(doy,quartile50,color='gold',alpha=1,zorder=3,linewidth=1.5,
         label=r'Median (1981-2010)')    
            
ax.fill_between(doy, quartile90, quartile75, facecolor='m', alpha=0.55,
                label=r'10-90th percentiles',zorder=2)
ax.fill_between(doy, quartile10, quartile25, facecolor='m', alpha=0.55,
                zorder=2)  
ax.fill_between(doy, quartile25, quartile50, facecolor='cornflowerblue', alpha=0.6,
                zorder=2)  
ax.fill_between(doy, quartile50, quartile75, facecolor='cornflowerblue', alpha=0.6,
                label=r'25-75th percentiles',zorder=2)              
   
plt.scatter(doy[currentdoy-2],ice[-1],s=10,color='aqua',zorder=9)

### Add text to the plot
plt.ylabel(r'\textbf{Extent} [$\times$10$^{6}$ km$^2$]',fontsize=15,
           color='darkgrey')
le = plt.legend(shadow=False,fontsize=6,loc='upper left',
           bbox_to_anchor=(0, 1.011),fancybox=True,ncol=2)
for text in le.get_texts():
    text.set_color('w')   
plt.title(r'\textbf{ANTARCTIC SEA ICE}',
                       fontsize=21,color='darkgrey')         

plt.text(doy[currentdoy+10],ice[-1]-1.5,r'\textbf{2018}',
         fontsize=13.5,rotation='horizontal',ha='left',color='aqua')
plt.text(360,0.8,r'\textbf{DATA:} National Snow \& Ice Data Center, Boulder CO',
         fontsize=5,rotation='horizontal',ha='right',color='darkgrey')
plt.text(360,1.3,r'\textbf{SOURCE:} ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/south/',
         fontsize=5,rotation='horizontal',ha='right',color='darkgrey')
plt.text(360,0.3,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='right',color='darkgrey')    
fig.subplots_adjust(top=0.91)

### Save figure        
plt.savefig(directoryfigure + 'nsidc_sie_ant_quartiles_currentyear.png',dpi=300)        
                  
                        