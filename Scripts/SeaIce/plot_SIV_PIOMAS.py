"""
Plots PIOMAS daily Sea Ice Volume for 1979-2016

Website   : http://psc.apl.uw.edu/research/projects/arctic-sea-ice-volume-
            anomaly/data/
Author    : Zachary M. Labe
Date      : 15 July 2016
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as c
import datetime

### Directory and time
directoryfigure = '/home/zlabe/Documents/Projects/IceVarFigs/Figures/' 

year,day,volume = np.loadtxt(
                          'PIOMAS.vol.daily.1979.2017.Current.v2.1.dat.gz',
                          skiprows=1,unpack=True)

### Current time
day = map(int,day)
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
years = np.arange(1979,2018,1)

currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday

month = datetime.date(int(currentyr), int(currentmn)-1, int(currentdy)).strftime('%B')

### Reshape sea ice volumes arrays
currentyear = volume.copy()[-day[-1]:]
volumen = volume[:-day[-1]]

volumen = np.reshape(volumen,(volumen.shape[0]/365,365))

### Calculate mean volume
mean = np.nanmean(volumen,axis=0)

### x-coordinates
doy = np.arange(0,np.nanmax(day))

### Calculate minimum
minsiv = np.nanmin(volumen[:,day[-1]])
minyear = np.where(volumen[:,day[-1]] == minsiv)[0]
timeyr = years[minyear][0]

### Make plot
plt.rc('savefig', facecolor='black')
plt.rc('axes', edgecolor='white')
plt.rc('xtick', color='white')
plt.rc('ytick', color='white')
plt.rc('axes', labelcolor='white')
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
plt.plot(doy,mean,color='white',linewidth=4,label='Average Volume',
         zorder=3,linestyle='-')

color=iter(plt.cm.magma(np.linspace(0,1,volumen.shape[0])))
for i in xrange(volumen.shape[0]):
    if i == 33:
        c = 'r'
        l = 2
        plt.plot(doy,volumen[i,:],c=c,zorder=2,linewidth=l,label='Year 2012')
    elif i == 37:
        c = 'gold'
        l = 2
        plt.plot(doy,volumen[i,:],c=c,zorder=2,linewidth=l,label='Year 2016')
    else:
        c=next(color)
        l = 0.6
        plt.plot(doy,volumen[i,:],c=c,zorder=1,linewidth=l)

plt.plot(doy[:day[-1]],currentyear,color='aqua',linewidth=2,
         label='Year 2017',zorder=6)
plt.scatter(day[-1]-1,currentyear[-1],
            s=6,color='aqua',zorder=4,marker='o')
                       
le = plt.legend(shadow=False,fontsize=8,loc='upper right',fancybox=True,
                frameon=False)
for text in le.get_texts():
    text.set_color('w')
                       
ax.tick_params('both',length=5.5,width=2,which='major')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)

plt.ylabel(r'\textbf{Volume [$\times$1000 km$^{3}$]}',fontsize=13,
           color='darkgrey')

xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan']

plt.xticks(np.arange(0,361,30),xlabels,rotation=0)

plt.yticks(np.arange(0,int(np.nanmax(volume)+2),2),
           map(str,np.arange(0,
                             int(np.nanmax(volume)+2),2)),fontsize=12)

plt.xlim([0,360])
plt.ylim([0,int(np.nanmax(volume)+1)])
plt.subplots_adjust(bottom=0.15)  

plt.text(0.3,2.1,r'\textbf{DATA:} PIOMAS v2.1 (Zhang and Rothrock, 2003)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0.3,1.1,r'\textbf{CSV:} http://psc.apl.washington.edu/zhang/IDAO/',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(0.3,0.1,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
plt.text(day[-1]+4,currentyear[-1]-2,r'\textbf{2017}',fontsize=8,color='aqua')

#plt.text(60,12,r'\textbf{%s %s}' % (month,currentyr),
#         color='aqua',fontsize=11,ha='left')
#plt.text(60,10,r'\textbf{%s [$\times$1000 km$^{3}$]}' % (currentyear[-1]),
#         color='aqua',fontsize=11,ha='left')
#plt.text(60,8,r'\textbf{*New Record Low*}',
#         color='aqua',fontsize=11,ha='left')         

fig.suptitle(r'\textbf{ARCTIC SEA ICE VOLUME (1979-%s)}' % currentyr,
                       fontsize=18,color='darkgrey') 

plt.savefig(directoryfigure + 'SIV_PIOMAS_September.png',dpi=900)

print '\n' '\n' 'Completed: Figure plotted!'
