"""
Plot land ice from GRACE

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
directoryfigure = './Figures/'

now = datetime.datetime.now()
currentmnq = now.month - 1
currentdy = now.day
currentyr = now.year
currentmn = datetime.date(currentyr,currentmnq, 1).strftime('%B')
currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday

### Load url
fileg = './Data/greenland_grace.txt'
filea = './Data/antarctic_grace.txt'

### Read file
yearg,gq,ung = np.genfromtxt(fileg,unpack=True,
                        usecols=[0,1,2])
yeara,aq,una = np.genfromtxt(filea,unpack=True,
                        usecols=[0,1,2])        

missing = np.where((yearg >2017.6) & (yearg <= 2018.45))[0]    
gq[missing] = np.nan     
aq[missing] = np.nan
                        
print('\nCompleted: Read land ice data!')                        

############################################################################
############################################################################
############################################################################
### Create plot
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='white')
plt.rc('xtick',color='white')
plt.rc('ytick',color='white')
plt.rc('axes',labelcolor='white')
plt.rc('axes',facecolor='black')

miny = -5400

fig = plt.figure()
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

plt.text(2002.3,-5100,r'\textbf{Antarctica}',color='deepskyblue',alpha=1,ha='left',
        fontsize=22,rotation=0,va='center',zorder=1)
        
ax.tick_params('both',length=5.5,width=2,which='major')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2) 

aqfill = aq.copy()
locnanaq = np.where(np.isnan(aqfill))[0]
aqfill[locnanaq] = (aqfill[locnanaq-1] + aqfill[locnanaq+1])/2
ax.fill_between(yeara, miny-200, aqfill, facecolor='deepskyblue', alpha=0.2)

ant, = plt.plot(yeara,aq,linestyle='-',linewidth=2.4,
         color='deepskyblue',zorder=2,clip_on=False)

plt.scatter(yeara[-1],aq[-1],s=20,color='crimson',zorder=9,clip_on=False)

plt.text(2023.2,-2450,r'\textbf{2022}',fontsize=11,color='crimson')

xlabels = map(str,np.arange(2002,2030,3))
plt.xticks(np.arange(2002,2030,3),xlabels,size=7)
ylabels = map(str,np.arange(-8000,1,1000))
plt.yticks(np.arange(-8000,1,1000),ylabels,size=7)
plt.ylim([miny,150])
plt.xlim([2002,2023])

plt.text(2002,-6350,r'\textbf{DATA:} Gravity Recovery and Climate Experiment (GRACE/GRACE-FO)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(2002,-6500,r'\textbf{SOURCE:} https://climate.nasa.gov/vital-signs/land-ice/ (NASA JPL)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
plt.text(2002,-6650,r'\textbf{REFERENCE:} Wiese et al. [2015, 2019]',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey',alpha=1)
         
plt.text(1995.2,10,r'\textbf{[Gt]}',color='darkgrey',fontsize=15,va='center',
         alpha=1)                

plt.text(2025,840,r'\textbf{LOSS OF LAND ICE}',fontsize=35,color='w',
         ha='center',va='center',alpha=1)

###########################################################################
###########################################################################
###########################################################################
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

plt.text(2002.3,-5100,r'\textbf{Greenland}',color='deepskyblue',alpha=1,ha='left',
        fontsize=22,rotation=0,va='center',zorder=1)

gqfill = gq.copy()
locnangq = np.where(np.isnan(gqfill))[0]
gqfill[locnangq] = (gqfill[locnangq-1] + gqfill[locnangq+1])/2
ax.fill_between(yearg, miny-200, gqfill, facecolor='deepskyblue', alpha=0.2)

gre, = plt.plot(yearg,gq,linestyle='-',linewidth=2.4,
         color='deepskyblue',zorder=2,clip_on=False)
#plt.plot(aq,linestyle='--',linewidth=2,zorder=1,color='r')
plt.scatter(yearg[-1],gq[-1],s=20,color='crimson',zorder=9,clip_on=False)

xlabels = map(str,np.arange(2002,2030,3))
plt.xticks(np.arange(2002,2030,3),xlabels,size=7)
ylabels = map(str,np.arange(-8000,1,1000))
plt.yticks(np.arange(-8000,1,1000),ylabels,size=7)
plt.ylim([miny,150])
plt.xlim([2002,2023])

plt.text(2023.2,-5175,r'\textbf{2022}',fontsize=11,color='crimson',ha='left')
plt.text(1995.2,10,r'\textbf{[Gt]}',color='darkgrey',fontsize=15,va='center',
         alpha=1) 

fig.subplots_adjust(wspace=0.4)
fig.subplots_adjust(top=0.83)
fig.subplots_adjust(bottom=0.2)

plt.text(2023.1,-6350,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
          fontsize=5,rotation='horizontal',ha='right',color='darkgrey',alpha=1)

def update(num,yearg,aq,gq,ant,bar):
    ant.set_data(yearg[:num+1],gq[:num+1])
    ant.axes.axis([2002,2023,miny,150])
    gre.set_data(yearg[:num+1],aq[:num+1])
    gre.axes.axis([2002,2023,miny,150])
    return bar,

ani = animation.FuncAnimation(fig,update,230,fargs=[yearg,
                              gq,aq,ant,gre],interval=0.001,blit=True)

### Save figure
ani.save('landice_moving.gif',writer='imagemagick',dpi=285)
# plt.savefig('landice.png',dpi=300)

print('\nCompleted: Script done!')                  
