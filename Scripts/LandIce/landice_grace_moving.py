"""
Plot change in land ice mass from GRACE satellite. Last update through
early 2017. GRACE-FO data will be released in the coming years.

Website   : https://climate.nasa.gov/vital-signs/land-ice/
Author    : Zachary M. Labe
Date      : 28 June 2017
"""

### Import modules
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math 

### Directory and time
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday

now = datetime.datetime.now()
currentmnq = now.month - 1
currentdy = now.day
currentyr = now.year
currentmn = datetime.date(currentyr,currentmnq, 1).strftime('%B')

### Load data files for Greenland (g) and Antarctica (a)
fileg = 'greenland_grace.txt'
filea = 'antarctic_grace.txt'

### Read file
yearg,gq,ung = np.genfromtxt(fileg,unpack=True,
                        usecols=[0,1,2])
yeara,aq,una = np.genfromtxt(filea,unpack=True,
                        usecols=[0,1,2])                        
                        
print('\nCompleted: Read land ice data!')                        

############################################################################
############################################################################
############################################################################
### Create animation
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='white')
plt.rc('xtick',color='white')
plt.rc('ytick',color='white')
plt.rc('axes',labelcolor='white')
plt.rc('axes',facecolor='black')

fig = plt.figure()

### Subplot for Antarctica 
ax = plt.subplot(121)  

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

plt.text(2002,-3850,r'\textbf{Antarctica}',color='dimgrey',alpha=1,ha='left',
        fontsize=22,rotation=0,va='center',zorder=1)
        
ax.tick_params('both',length=5.5,width=2,which='major')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2) 

ant, = plt.plot(yeara,aq,linestyle='-',linewidth=2,
         color='deepskyblue',zorder=2)

plt.scatter(yeara[-1],aq[-1],s=20,color='m',zorder=9)

plt.text(2016.1,-2260,r'\textbf{2017}',fontsize=8,color='m')
xlabels = map(str,np.arange(2002,2018,3))
plt.xticks(np.arange(2002,2018,3),xlabels)
ylabels = map(str,np.arange(-4000,1,1000))
plt.yticks(np.arange(-4000,1,1000),ylabels)
plt.ylim([-4000,150])
plt.xlim([2002,2018])

plt.text(2002,-4750,r'\textbf{DATA:} Gravity Recovery and Climate Experiment (GRACE)',
         fontsize=5,rotation='horizontal',ha='left',color='dimgrey',alpha=1)
plt.text(2002,-4900,r'\textbf{SOURCE:} https://climate.nasa.gov/vital-signs/land-ice/ (NASA)',
         fontsize=5,rotation='horizontal',ha='left',color='dimgrey',alpha=1)
plt.text(2002,-5050,r'\textbf{REFERENCE:} Wiese et al. [2015]',
         fontsize=5,rotation='horizontal',ha='left',color='dimgrey',alpha=1)
         
plt.text(1996.6,10,r'\textbf{[Gt]}',color='dimgrey',fontsize=15,va='center',
         alpha=1)         
plt.text(2021,600,r'\textbf{LAND ICE}',fontsize=40,color='w',
         ha='center',va='center',alpha=1)

###########################################################################
###########################################################################
###########################################################################
### Subplot for Greenland
ax = plt.subplot(122)  

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

plt.text(2002,-3850,r'\textbf{Greenland}',color='dimgrey',alpha=1,ha='left',
        fontsize=22,rotation=0,va='center',zorder=1)

gre, = plt.plot(yearg,gq,linestyle='-',linewidth=2,
         color='deepskyblue',zorder=2)

plt.scatter(yearg[-1],gq[-1],s=20,color='m',zorder=9)

xlabels = map(str,np.arange(2002,2018,3))
plt.xticks(np.arange(2002,2018,3),xlabels)
ylabels = map(str,np.arange(-4000,1,1000))
plt.yticks(np.arange(-4000,1,1000),ylabels)
plt.ylim([-4000,150])
plt.xlim([2002,2018])

plt.text(2017.9,-3844,r'\textbf{2017}',fontsize=8,color='m',ha='left')
plt.text(1996.6,10,r'\textbf{[Gt]}',color='dimgrey',fontsize=15,va='center',
         alpha=1) 

fig.subplots_adjust(wspace=0.4)
fig.subplots_adjust(top=0.83)
fig.subplots_adjust(bottom=0.2)

### Create animation using matplotlib
def update(num,yearg,aq,gq,ant,bar):
    ant.set_data(yearg[:num+1],gq[:num+1])
    ant.axes.axis([2002,2018,-4000,150])
    gre.set_data(yearg[:num+1],aq[:num+1])
    gre.axes.axis([2002,2018,-4000,150])
    return bar,

ani = animation.FuncAnimation(fig,update,190,fargs=[yearg,
                              gq,aq,ant,gre],interval=0.001,blit=True)

plt.text(2018.2,-4750,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='right',color='w',alpha=0.3)

### Save figure
#plt.savefig('landice.png',dpi=300)
ani.save('landice_moving.gif',dpi=300)

print('\nCompleted: Script done!')
                     