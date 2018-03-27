"""
Scripts calculates mean monthly SIT from PIOMAS
 
Notes
-----
    Source : http://psc.apl.washington.edu/zhang/IDAO/data_piomas.html
    Author : Zachary Labe
    Date   : 9 September 2016
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import datetime
import read_SeaIceThick_PIOMAS as CT
import calc_PiomasArea as CA

### Directory and time
directoryfigure = '/home/zlabe/Documents/Projects/IceVarFigs/Figures/' 
directorydata = '/home/zlabe/Documents/Projects/IceVarFigs/Data/'  

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

### Call functions to read data
lats,lons,sit = CT.readPiomas(directorydata,years,0.15)
area = CA.readPiomasArea(directorydata)

###########################################################################
###########################################################################
###########################################################################
### Calculating temporal sit
def weightThick(var,area):
    """
    Area weights sit array 4d [year,month,lat,lon] into [year,month] using 
    original PIOMAS GOCC grid, which area-weights
    """
    sityr = np.empty((var.shape[0],var.shape[1]))
    for i in range(var.shape[0]):
        for j in range(var.shape[1]):
            varq = var[i,j,:,:]
            mask = np.isfinite(varq) & np.isfinite(area)
            varmask = varq[mask]
            areamask = area[mask]
            sityr[i,j] = np.nansum(varmask*areamask)/np.sum(areamask)
     
    print('\nCompleted: Yearly weighted SIT average!') 
    return sityr
     
sitave = weightThick(sit,area)

###############################################################################
###############################################################################
###############################################################################
### Plot figure
matplotlib.rc('savefig', facecolor='black')
matplotlib.rc('axes', edgecolor='white')
matplotlib.rc('xtick', color='white')
matplotlib.rc('ytick', color='white')
matplotlib.rc('axes', labelcolor='white')
matplotlib.rc('axes', facecolor='black')
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']})

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

fig = plt.figure()
ax = plt.subplot(111) 

adjust_spines(ax, ['left', 'bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.tick_params('both',length=5.5,width=2,which='major',direction='out')

color=iter(plt.cm.viridis(np.linspace(0,1,len(sitave))))
for i in range(sitave.shape[0]):
    cma=next(color)
    ll = 0.9
    aa = 1
    if years[i] == 2017:
        cma = 'r'
        ll = 2.5
        aa = 1
        plt.scatter(8,sitave[i,8],color='r',s=20,zorder=11)
    plt.plot(sitave[i,:],color=cma,alpha=aa,linewidth=ll)
    
    ccc = 'white'
    if years[i] == 2017:
        ccc = 'r'
    t = plt.annotate(r'\textbf{%s}' % years[i],xy=(1,1),xytext=(7.5,2.5),color=ccc,
                     fontsize=50)       
    if years[i] == 2017:
        tt = plt.annotate(r'\textbf{%s}' % years[i],xy=(1,1),xytext=(7.8,sitave[i,8]-0.15),color=cma,
                     fontsize=7)    
    else:
        tt = plt.annotate(r'\textbf{%s}' % years[i],xy=(1,1),xytext=(11.3,sitave[i,-1]-0.03),color=cma,
                 fontsize=7)
                          
    xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
              r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan'] 
    plt.xticks(np.arange(0,12,1),xlabels,rotation=0,fontsize=9)
    plt.yticks(np.arange(0,3.5,0.5),np.arange(0,3.5,0.5),rotation=0,fontsize=9)
    plt.xlim([0,11])
    plt.ylim([0.5,3])
    
    plt.ylabel(r'\textbf{Sea Ice Thickness (m)}',color='darkgrey')
    
    plt.text(0.01,0.64,r'\textbf{DATA:} PIOMAS v2.1 [Zhang and Rothrock, 2003]',
             fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
    plt.text(0.01,0.57,r'\textbf{SOURCE:} http://psc.apl.washington.edu/zhang/IDAO/',
             fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
    plt.text(0.01,0.5,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
             fontsize=5,rotation='horizontal',ha='left',color='darkgrey')
    
    ### Use ImageMagick to make GIF from each .png file
    if i <= 9:
        plt.savefig(directoryfigure + 'meansit_0%s.png' % i,dpi=300)
    else:
        plt.savefig(directoryfigure + 'meansit_%s.png' % i,dpi=300)
        if i == 38:
            plt.savefig(directoryfigure + 'meansit_38.png',dpi=300)
            plt.savefig(directoryfigure + 'meansit_39.png',dpi=300)
            plt.savefig(directoryfigure + 'meansit_40.png',dpi=300)
            plt.savefig(directoryfigure + 'meansit_41.png',dpi=300)
            plt.savefig(directoryfigure + 'meansit_42.png',dpi=300)
            plt.savefig(directoryfigure + 'meansit_43.png',dpi=300)
            plt.savefig(directoryfigure + 'meansit_44.png',dpi=300)
            plt.savefig(directoryfigure + 'meansit_45.png',dpi=300)
            plt.savefig(directoryfigure + 'meansit_46.png',dpi=300)
            plt.savefig(directoryfigure + 'meansit_47.png',dpi=300)
            plt.savefig(directoryfigure + 'meansit_48.png',dpi=300)
            plt.savefig(directoryfigure + 'meansit_49.png',dpi=300)
            plt.savefig(directoryfigure + 'meansit_50.png',dpi=300)
            plt.savefig(directoryfigure + 'meansit_51.png',dpi=300)
       
    t.remove()
    tt.remove()