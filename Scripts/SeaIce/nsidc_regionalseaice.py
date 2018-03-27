"""
Reads in current year's regional Arctic sea ice extent from Sea Ice Index 3 
(NSIDC)

Website   : ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/seaice_analysis/
Author    : Zachary M. Labe
Date      : 21 October 2017
"""

### Import modules
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd

### Directory and time
directoryfigure = '/home/zlabe/Documents/Projects/IceVarFigs/Figures/'
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday
doy = np.arange(0,365,1)
lastday = now.timetuple().tm_yday -2
years = np.arange(1979,2018+1,1)

### Turn on to read in the data (slow!)
datareader=True

### Load url
url = 'ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/seaice_analysis/' \
        'Sea_Ice_Index_Regional_Daily_Data_G02135_v3.0.xlsx'

### Read files from NSIDC (not very efficient - lol)
### There are more regional seas that can easily be added!
if datareader == True:       
    df_barents = pd.read_excel(url,sheetname='Barents-Extent-km^2',header=1,
                               parse_cols=range(3,43,1))
    barents = df_barents.as_matrix()
    ##################
    ##################
    ##################
    df_beaufort = pd.read_excel(url,sheetname='Beaufort-Extent-km^2',header=1,
                                parse_cols=range(3,43,1))
    beaufort = df_beaufort.as_matrix()
    ##################
    ##################
    ##################
    df_bering = pd.read_excel(url,sheetname='Bering-Extent-km^2',header=1,
                                parse_cols=range(3,43,1))
    bering = df_bering.as_matrix()
    ##################
    ##################
    ##################
    df_can = pd.read_excel(url,sheetname='CanadianArchipelago-Extent-km^2',header=1,
                                parse_cols=range(3,43,1))
    can = df_can.as_matrix()
    ##################
    ##################
    ##################
    df_chukchi = pd.read_excel(url,sheetname='Chukchi-Extent-km^2',header=1,
                                parse_cols=range(3,43,1))
    chukchi = df_chukchi.as_matrix()
    ##################
    ##################
    ##################
    df_ess = pd.read_excel(url,sheetname='East-Siberian-Extent-km^2',header=1,
                                parse_cols=range(3,43,1))
    ess = df_ess.as_matrix()
    ##################
    ##################
    ##################
    df_green = pd.read_excel(url,sheetname='Greenland-Extent-km^2',header=1,
                                parse_cols=range(3,43,1))
    green = df_green.as_matrix()
    ##################
    ##################
    ##################
    df_hudson = pd.read_excel(url,sheetname='Hudson-Extent-km^2',header=1,
                                parse_cols=range(3,43,1))
    hudson = df_hudson.as_matrix()
    ##################
    ##################
    ##################
    df_kara = pd.read_excel(url,sheetname='Kara-Extent-km^2',header=1,
                                parse_cols=range(3,43,1))
    kara = df_kara.as_matrix()
    ##################
    ##################
    ##################
    df_lap = pd.read_excel(url,sheetname='Laptev-Extent-km^2',header=1,
                                parse_cols=range(3,43,1))
    lap = df_lap.as_matrix()
    
    ### Read data in list then array
    sie = [barents,beaufort,bering,can,chukchi,ess,green,hudson,kara,lap]
    sie = np.asarray(sie)/1e6
                            
    print('\nCompleted: Read sea ice data!')                        

### Find statistics
yearsq = np.where((years>=1981) & (years<=2010))[0]   
sieq = sie[:,:,yearsq]  
    
mean = np.empty((sie.shape[0],sie.shape[1]))
std = np.empty((sie.shape[0],sie.shape[1]))
for i in range(sie.shape[0]):
    for j in range(sie.shape[1]):
        mean[i,j] = np.nanmean(sieq[i,j,:],axis=0)
        std[i,j] = np.nanstd(sieq[i,j,:],axis=0)

### +-2 standard deviation
maxe = mean + (2.*std)
mine = mean - (2.*std)

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

### Labels for months and regional seas        
xlabels = [r'Jan',r'Apr',r'Jul',r'Oct',r'Jan']
sienames = [r'\textbf{BARENTS SEA}',r'\textbf{BEAUFORT SEA}',
            r'\textbf{BERING SEA}',
            r'\textbf{CANADIAN ARCHIPELAGO}',r'\textbf{CHUKCHI SEA}',
            r'\textbf{EAST SIBERIAN SEA}',r'\textbf{GREENLAND SEA}',
            r'\textbf{HUDSON BAY}',r'\textbf{KARA SEA}',
            r'\textbf{LAPTEV SEA}']

### Loop through each regional sea 
fig = plt.figure()
for i in range(sie.shape[0]):
    ax = plt.subplot(5,2,i+1)
    
    ### if statement for adjusting plot axes between bottom and others
    if i >= 8:           
        ax.tick_params('both',length=3.5,width=2,which='major') 
        adjust_spines(ax, ['left','bottom'])            
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')  
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['left'].set_linewidth(2)
        ax.tick_params(color='darkgrey')
    else:          
        ax.tick_params('both',length=3.5,width=2,which='major') 
        adjust_spines(ax, ['left','bottom'])            
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none') 
        ax.spines['bottom'].set_color('none')
        ax.spines['left'].set_linewidth(2)
        ax.tick_params(labelbottom='off', labelright='off',bottom='off',
                       color='darkgrey')
    
    ### PLOT
    plt.plot(sie[i,:,-1],color='aqua',zorder=2)
    ax.fill_between(doy, mine[i], maxe[i], facecolor='magenta', alpha=0.4)
    
    plt.yticks(np.arange(0,1.6,0.5),list(map(str,np.arange(0,1.6,0.5))),
               fontsize=6)
    
    plt.axvline(lastday,color='dimgrey',linestyle='--',linewidth=2,zorder=1)
    plt.scatter(lastday,sie[i,lastday,-1],color='aqua',s=15,zorder=3)
    
    plt.ylim([0,1.5])
    
    ### if statement for adjusting plot axes between bottom and others
    if i >= 8:
        plt.xticks(np.arange(0,366,90.4),xlabels,rotation=0,fontsize=7)
        
    plt.xlim([0,361.5])
    
    ### Label each sea
    plt.text(0,1.45,sienames[i],color='w',fontsize=9,ha='left',
             va='center')     

### Add text to plot
fig.suptitle(r'\textbf{REGIONAL SEA ICE}',
                   fontsize=24,color='darkgrey') 
plt.text(-436,-1.1,r'\textbf{DATA:} National Snow \& Ice Data Center, Boulder CO',
         fontsize=5.5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(-436,-1.35,r'\textbf{SOURCE:} ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/seaiceanalysis/',
         fontsize=5.5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(365,-1.1,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5.5,rotation='horizontal',ha='right',color='darkgrey')
plt.text(-520,6.6,r'\textbf{Extent [$\bf{\times 10^{6}}$\ \textbf{km}$\bf{^2}$]}',
           fontsize=13,alpha=1,color='darkgrey',rotation=90) 
plt.text(365,9.4,r'$\bf{\pm}$2\ \textbf{std. dev.}',fontsize=10,
         color='magenta',alpha=0.7,ha='right') 

### Adjust size of plot  
fig.subplots_adjust(hspace=0.3)

### Save figure       
plt.savefig(directoryfigure + 'nsidc_sie_regionals.png',dpi=300)  

print('Completed: Script done!')                          