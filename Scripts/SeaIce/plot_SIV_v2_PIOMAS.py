"""
Plots PIOMAS daily Sea Ice Volume for 1979-2019

Website   : http://psc.apl.uw.edu/research/projects/arctic-sea-ice-volume-
            anomaly/data/
Author    : Zachary M. Labe
Date      : 7 November 2019
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as c
import datetime
import cmocean

### Directory and time
directorydata = './Data/'
directoryfigure = './Figures/'

year,day,volume = np.loadtxt(directorydata +
                             'PIOMAS.vol.daily.1979.2018.Current.v2.1.dat.gz',
                             skiprows=1,unpack=True)

### Current time
day = list(map(int,day))
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
years = np.arange(1979,2020,1)

currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday

month = datetime.date(int(currentyr),int(currentmn)-1,int(currentdy)).strftime('%B')

### Reshape sea ice volumes arrays
currentyear = volume.copy()[-day[-1]:]
volumen = volume[:-day[-1]]

volumen = np.reshape(volumen,(volumen.shape[0]//365,365))

### Calculate mean volume
mean = np.nanmean(volumen,axis=0)

### x-coordinates
doy = np.arange(0,np.nanmax(day))

### Calculate minimum
minsiv = np.nanmin(volumen[:,day[-1]-1])
minyear = np.where(volumen[:,day[-1]-1] == minsiv)[0]
timeyr = years[minyear][0]

### Make plot
plt.rc('savefig', facecolor='black')
plt.rc('axes', edgecolor='darkgrey')
plt.rc('xtick', color='darkgrey')
plt.rc('ytick', color='darkgrey')
plt.rc('axes', labelcolor='darkgrey')
plt.rc('axes', facecolor='black')
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

### Return information
print('\n' 'PIOMAS -- Sea Ice Volume --', now.strftime("%Y-%m-%d %H:%M"), '\n' '\n')
print('Completed: Reading Data!')
print('Completed: Reshaping Data!' '\n' '\n')
print('Current Sea Ice Volume = %s [x1000 km^3]' % currentyear[-1])
print('Lowest previous record = %s --> %s [x1000 km^3]' % (timeyr,minsiv))

### Plot Arctic sea ice volume
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

ax.tick_params('both',length=5.5,width=2,which='major')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)

### Labeling (subject to change!)
color=iter(cmocean.cm.balance(np.linspace(0.05,0.95,volumen.shape[0])))
for i in range(volumen.shape[0]):
    if i == 333:
        c = 'm'
        l = 1.2
        plt.plot(doy,volumen[i,:],c=c,zorder=3,linewidth=l,label='Year 2012')
    elif i == 393:
        c = 'gold'
        l = 1.2
        plt.plot(doy,volumen[i,:],c=c,zorder=3,linewidth=l,label='Year 2018')
    else:
        c=next(color)
        l = 1.5
        plt.plot(doy,volumen[i,:],c=c,zorder=1,linewidth=l,alpha=1)   
    if any([i==1,i==11,i==21,i==31]):
        if i == 31:
            plt.text(376,np.nanmean(volumen[i:i+9,-1],axis=0),r'\textbf{%ss}*' % years[i],
                     color=c,fontsize=9,ha='center',va='center')
        else:
            plt.text(374,np.nanmean(volumen[i:i+10,-1],axis=0),r'\textbf{%ss}' % years[i],
                     color=c,fontsize=9,ha='center',va='center')

### Plot Figure
plt.plot(doy[:day[-1]],currentyear,color='gold',linewidth=1.6,
         label='Year 2019',zorder=6)
plt.scatter(day[-1]-1,currentyear[-1],
            s=24,color='gold',zorder=4,marker='o')
                      

### Organize axes
plt.ylabel(r'\textbf{Volume [$\times$1000 km$^{3}$]}',fontsize=16,
           color='darkgrey')

xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan']

plt.xticks(np.arange(0,361,30),xlabels,rotation=0,fontsize=9)
plt.xlim([0,360])

plt.yticks(np.arange(0,int(np.nanmax(volume)+2),3),
           map(str,np.arange(0,
                             int(np.nanmax(volume)+2),3)),fontsize=10)
plt.ylim([0,int(np.nanmax(volume))])

### Squeeze figure
plt.subplots_adjust(bottom=0.15)  

### Source data
plt.text(0.,1.7,r'\textbf{DATA:} PIOMAS v2.1 (Zhang and Rothrock, 2003)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0.,0.9,r'\textbf{SOURCE:} http://psc.apl.uw.edu/research/projects/arctic-sea-ice-volume-anomaly/',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0.,0.1,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(day[-1]-14,currentyear[-1]-3.5,r'\textbf{%s}' % currentyr,fontsize=12,color='gold')        

plt.title(r'\textbf{ARCTIC SEA ICE (1979-%s)}' % currentyr,
                       fontsize=25,color='w') 

### Save figure
plt.savefig(directoryfigure + 'SIV_PIOMAS_September_v2.png',dpi=900)


print('\n' '\n' 'Completed: Figure plotted!')
