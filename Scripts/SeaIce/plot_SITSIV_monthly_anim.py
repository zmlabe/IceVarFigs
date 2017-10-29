"""
Scripts calculates monthly mean sea ice thickness and volume from PIOMAS
 
Notes
-----
    Source : http://psc.apl.washington.edu/zhang/IDAO/data_piomas.html
    Author : Zachary Labe
    Date   : 5 June 2017
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as c
import matplotlib
import datetime
import read_SeaIceThick_PIOMAS as CT
import calc_PiomasArea as CA

### Define directories
directorydata = '/home/zlabe/surt/seaice_obs/PIOMAS/'   
directoryfigure = '/home/zlabe/Documents/Projects/Tests/Piomas/Mean_SITSIV/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Plot Mean Sea Ice Thickness - %s----' % titletime) 

### Alott time series
yearmin = 1979
yearmax = 2017
years = np.arange(yearmin,yearmax+1,1)
months = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',r'Aug',
          r'Sep',r'Oct',r'Nov',r'Dec']

### Call functions
lats,lons,sit = CT.readPiomas(directorydata,years,0.15)
area = CA.readPiomasArea(directorydata)

### Directory and time
directorydatab = '/home/zlabe/Documents/Projects/Tests/SIV_animate/Data/'                                  

print('\n' 'PIOMAS -- Sea Ice Volume --', \
        now.strftime("%Y-%m-%d %H:%M"), '\n' '\n')

### Read data
years2,aug = np.genfromtxt(directorydatab + 'monthly_piomas.txt',
                           unpack=True,delimiter='',usecols=[0,9])

### Calculate climatology from 1981-2010 baseline
climyr = np.where((years2 >= 1981) & (years2 <= 2010))[0]  

clim = np.nanmean(aug[climyr])  

###########################################################################
###########################################################################
###########################################################################
### Calculating temporal sit
def weightThick(var,area):
    """
    Area weights sit array 4d [year,month,lat,lon] into [year,month] from
    original PIOMAS GOCC grid (area weighted)
    """
    sityr = np.empty((var.shape[0],var.shape[1]))
    for i in range(var.shape[0]):
        for j in range(var.shape[1]):
            varq = var[i,j,:,:]
            mask = np.isfinite(varq) & np.isfinite(area)
            varmask = varq[mask]#    plt.subplots_adjust(top=0.98)
            areamask = area[mask]
            sityr[i,j] = np.nansum(varmask*areamask)/np.sum(areamask)
     
    print('\nCompleted: Yearly weighted SIT average!')
    return sityr
     
sitave = weightThick(sit,area)

###############################################################################
###############################################################################
###############################################################################
### Plot plot of sea ice thickness
matplotlib.rc('savefig', facecolor='black')
matplotlib.rc('axes', edgecolor='white')
matplotlib.rc('xtick', color='white')
matplotlib.rc('ytick', color='white')
matplotlib.rc('axes', labelcolor='white')
matplotlib.rc('axes', facecolor='black')
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']})
        
fig = plt.figure()
color=iter(plt.cm.viridis(np.linspace(0,1,len(sitave))))
for i in range(sitave.shape[0]):
    ### Adjust axes in time series plots 
    def adjust_spines(ax, spines):
        for loc, spine in ax.spines.items():
            if loc in spines:
                spine.set_position(('outward', 0))
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
    
    ax = plt.subplot(211) 
    adjust_spines(ax, ['left', 'bottom'])            
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.tick_params('both',length=5,width=2,which='major',direction='out',
                   pad=3)
    cma=next(color)
    ll = 1.4
    aa = 1
    plt.axvline(8,linestyle='--',linewidth=1.3,color='dimgray',zorder=0)
    plt.plot(sitave[i,:],color=cma,alpha=aa,linewidth=ll,zorder=1)
    ttt = plt.scatter(8,sitave[i,8],color='w',s=20,zorder=2)
    if years[i] == 2017:
        cma = 'r'
        ll = 2.5
        aa = 1
        plt.scatter(8,sitave[i,8],color='r',s=20,zorder=3)
        plt.annotate(r'$\bf{\nwarrow}$',xy=(1,1),xytext=(8.1,sitave[i,8]-0.25),color='r',
                 fontsize=10)
    plt.plot(sitave[i,:],color=cma,alpha=aa,linewidth=ll,zorder=1)
    ccc = 'white'
    aaa = 0.6
    if years[i] == 2017:
        ccc = 'r'
        aaa = 1
    t = plt.annotate(r'\textbf{%s}' % years[i],xy=(1,1),xytext=(8.8,2.7),color=ccc,
                     fontsize=50,alpha=aaa)    

    xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
              r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan'] 
    plt.xticks(np.arange(0,12,1),xlabels,rotation=0,fontsize=6.5)
    plt.yticks(np.arange(0,3.5,0.5),np.arange(0,3.5,0.5),rotation=0,
               fontsize=6.5)
    ax.tick_params(pad=3)
    plt.xlim([0,11])
    plt.ylim([0.5,3])
    
    a = plt.text(-1.3,2.7,r'\textbf{THICKNESS}',fontsize=20,color='w',rotation=90,
             alpha=0.6)
    b = plt.text(-1.3,-1.15,r'\textbf{VOLUME}',fontsize=20,color='w',rotation=90,
             alpha=0.6)
    c = plt.text(0,3.25,r'\textbf{m}',fontsize=11,color='w',alpha=0.6,
             ha='center',va='center')

###########################################################################
###########################################################################
###########################################################################
### Begin plot of sea ice volume    
    
### Adjust axes in time series plots 
    def adjust_spines(ax, spines):
        for loc, spine in ax.spines.items():
            if loc in spines:
                spine.set_position(('outward', 6))
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

    ax = plt.subplot(212)
    
    adjust_spines(ax, ['left', 'bottom'])
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.tick_params('both',length=5,width=2,which='major',direction='out',
                   pad=3)
    
    N = 1
    ind = np.linspace(N,0.2,3)
    width = .33

    rects = plt.barh(ind,[0,aug[i],clim],width)
    
    plt.axvline(clim,color='dimgray',ymin=0.0567,ymax=0.622,linewidth=3,
                linestyle='-')
    
    ax.tick_params(labelleft='off')
    plt.setp(ax.get_yticklines()[0:-1],visible=False)
    
    if aug[i] >= clim:
        cc=cma
    elif aug[i] < clim:
        cc=cma
    elif years[i] == 2017:
        cc = 'r'
    
    rects[1].set_color(cc)
    rects[-1].set_color('dimgray')
    
    plt.xticks(np.arange(0,31,5),map(str,np.arange(0,31,5)),fontsize=6.5)
               
    plt.subplots_adjust(bottom=0.15) 

    d = plt.text(0.03,-0.39,r'\textbf{DATA:} PIOMAS v2.1 [Zhang and Rothrock, 2003]',
         fontsize=5,rotation='horizontal',ha='left',color='w',
         alpha=0.6)
    e = plt.text(0.03,-0.45,r'\textbf{SOURCE:} http://psc.apl.washington.edu/zhang/IDAO/data.html',
             fontsize=5,rotation='horizontal',ha='left',color='w',
             alpha=0.6)
    f = plt.text(30.3,-0.39,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
             fontsize=5,rotation='horizontal',ha='right',color='w',
             alpha=0.6)  

    j = plt.text(5,0.88,r'\textbf{ARCTIC SEA ICE}',fontsize=30,color='w',
                 alpha=0.6)
    plt.xlim([0,30])
    
    if i == 38:
        ccc = 'r'  
    else:
        ccc = 'white' 
    plt.text(2.4,0.17,r'1981-2010 Average',rotation=0,color='w',
             fontsize=9)
    g = plt.text(30.4,0.02,r'$\times$1000',fontsize=11,
                        color='w',alpha=0.6)
    h = plt.text(31.45,-0.136,r'\textbf{km$^{3}$}',fontsize=11,
                    color='w',alpha=0.6)
    
    ### Save figure to be used in ImageMagick for GIF
    if i < 10:        
        plt.savefig(directoryfigure + 'map_0%s.png' % i,dpi=300)
    else:
        plt.savefig(directoryfigure + 'map_%s.png' % i,dpi=300)
        if i == 38:
            plt.savefig(directoryfigure + 'map_38.png',dpi=300)
            plt.savefig(directoryfigure + 'map_39.png',dpi=300)
            plt.savefig(directoryfigure + 'map_40.png',dpi=300)
            plt.savefig(directoryfigure + 'map_41.png',dpi=300)
            plt.savefig(directoryfigure + 'map_42.png',dpi=300)
            plt.savefig(directoryfigure + 'map_43.png',dpi=300)
            plt.savefig(directoryfigure + 'map_44.png',dpi=300)
            plt.savefig(directoryfigure + 'map_45.png',dpi=300)
            plt.savefig(directoryfigure + 'map_46.png',dpi=300)
            plt.savefig(directoryfigure + 'map_47.png',dpi=300)
            plt.savefig(directoryfigure + 'map_48.png',dpi=300)
            plt.savefig(directoryfigure + 'map_49.png',dpi=300)
            plt.savefig(directoryfigure + 'map_50.png',dpi=300)
            plt.savefig(directoryfigure + 'map_51.png',dpi=300)
            plt.savefig(directoryfigure + 'map_52.png',dpi=300)
            plt.savefig(directoryfigure + 'map_53.png',dpi=300)
      
    ### Remove texts per each loop    
    t.remove()
    ttt.remove()
    rects.remove()
    a.remove()
    b.remove()
    c.remove()
    d.remove()
    e.remove()
    f.remove()
    g.remove()
    h.remove()
    j.remove()