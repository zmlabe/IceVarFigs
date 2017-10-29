"""
Plots PIOMAS monthly Sea Ice Volume for 1979-2016

Website   : http://psc.apl.uw.edu/research/projects/arctic-sea-ice-volume-
            anomaly/data/
Author    : Zachary M. Labe
Date      : 21 September 2016
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import datetime

### Directory and time
directorydata = '/home/zlabe/Documents/Projects/Tests/SIV_animate/Data/'                   
directoryfigure = '/home/zlabe/Documents/Projects/Tests/SIV_animate/'                  

now = datetime.datetime.now()
currentmn = str(now.month-1)
currentdy = str(now.day)
currentyr = str(now.year)
years = np.arange(1979,2018,1)

print('\n' 'PIOMAS -- Sea Ice Volume --', \
        now.strftime("%Y-%m-%d %H:%M"), '\n') 

### Read data
years,aug = np.genfromtxt(directorydata + 'monthly_piomas.txt',
                           unpack=True,delimiter='',usecols=[0,9])

### Calculate average from 1981-2010 baseline
climyr = np.where((years >= 1981) & (years <= 2010))[0]  

clim = np.nanmean(aug[climyr])                         

print('Completed: Read data!')

###############################################################################
###############################################################################
###############################################################################
### Plot figure

### Select attributes
plt.rc('savefig', facecolor='black')
plt.rc('axes', edgecolor='white')
plt.rc('xtick', color='white')
plt.rc('ytick', color='white')
plt.rc('axes', labelcolor='white')
plt.rc('axes', facecolor='black')
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

### Plot horizontal bar graph
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

for i in range(aug.shape[0]):
    fig = plt.figure()
    ax = plt.subplot(111)
    
    adjust_spines(ax, ['left', 'bottom'])
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.tick_params('both',length=5.5,width=2,which='major',direction='out')
    
    N = 1
    ind = np.linspace(N,0.2,3)
    width = .33

    rects = plt.barh(ind,[0,aug[i],clim],width)
    
    plt.axvline(clim,color='dimgray',ymin=0.0509,ymax=0.627,linewidth=3,
                linestyle='-')
    
    ax.tick_params(labelleft='off')
    plt.setp(ax.get_yticklines()[0:-1],visible=False)
    
    if aug[i] >= clim:
        cc = 'cornflowerblue'
    elif aug[i] < clim:
        cc = 'indianred'
    
    rects[1].set_color(cc)
    rects[-1].set_color('dimgray')
    
    plt.xticks(np.arange(0,36,5),map(str,np.arange(0,36,5)))
    plt.xlabel(r'\textbf{Sea Ice Volume [$\times$1000 km$^{3}$]}',
               fontsize=14,color='darkgrey')
               
    plt.subplots_adjust(bottom=0.31)   

    plt.text(0.03,-0.4,r'\textbf{DATA:} PIOMAS v2.1 [Zhang and Rothrock, 2003] [\textbf{September}]',
         fontsize=6,rotation='horizontal',ha='left',color='darkgrey')
    plt.text(0.03,-0.45,r'\textbf{CSV:} http://psc.apl.washington.edu/zhang/IDAO/data.html',
             fontsize=6,rotation='horizontal',ha='left',color='darkgrey')
    plt.text(35.3,-0.4,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
             fontsize=6,rotation='horizontal',ha='right',color='darkgrey')  
    
    if i == 38:
        ccc = 'indianred'  
    else:
        ccc = 'white'
    plt.text(11.5,0.9,r'\textbf{%s}' % int(years[i]),fontsize=49,color=ccc)   
    plt.text(1.4,0.18,r'1981-2010 Average',rotation=0,color='w',
             fontsize=10)
    
    ### Save figure for GIF creation using ImageMagick
    if i < 10:        
        plt.savefig(directoryfigure + 'siv_0%s.png' % i,dpi=300)
    else:
        plt.savefig(directoryfigure + 'siv_%s.png' % i,dpi=300)
        if i == 38:
            plt.savefig(directoryfigure + 'siv_38.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_39.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_40.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_41.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_42.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_43.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_44.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_45.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_46.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_47.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_48.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_49.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_50.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_51.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_52.png',dpi=300)
            plt.savefig(directoryfigure + 'siv_53.png',dpi=300)