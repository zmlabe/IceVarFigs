"""
Script reads PIOMAS binary files stored on remote server through 
present year. Second function calculates climatological average over 
a given period.
 
Notes
-----
    Source : http://psc.apl.washington.edu/zhang/IDAO/data_piomas.html
    Author : Zachary Labe
    Date   : 7 September 2016
    
Usage
-----
    readPIOMAS(directory,years,threshold)
    meanThick(yearmin,yearmax,years,sit)
"""

def readPiomas(directory,years,threshold):
    """
    Function reads PIOMAS binary and converts to standard numpy array.

    Parameters
    ----------
    directory : string
        working directory for stored PIOMAS files
    years : integers
        years for data files
    threshold : float
        mask sea ice thickness amounts < to this value

    Returns
    -------
    lats : 2d array
        latitudes
    lons : 2d array
        longitudes
    var : 4d array [year,month,lat,lon]
        sea ice thickness (m) 

    Usage
    -----
    lats,lons,var = readPiomas(directory,years,threshold)
    """
    
    print('\n>>> Using readPiomas function!\n')
    
    ### Import modules
    import numpy as np
    import datetime
    
    ### Current times
    now = datetime.datetime.now()
    mo = now.month
    yr = now.year
    dy = now.day
    
    ### Retrieve Grid
    grid = np.genfromtxt(directory + 'grid.txt')
    grid = np.reshape(grid,(grid.size))  
    
    ### Define Lat/Lon
    lon = grid[:grid.size//2]   
    lons = np.reshape(lon,(120,360))
    lat = grid[grid.size//2:]
    lats = np.reshape(lat,(120,360))
    
    ### Call variables from PIOMAS
    files = 'heff'
    directory = directory + 'Thickness/'
    
    ### Read data from binary into numpy arrays
    var = np.empty((len(years),12,120,360))
    
    print('Currently reading PIOMAS data!')
    for i in range(len(years)):
        data = np.fromfile(directory + files + '_%s.H' % (years[i]),
                           dtype = 'float32')

    ### Reshape into [year,month,lat,lon]
        months = data.shape[0]//(120*360)
        if months != 12:
            lastyearq = np.reshape(data,(months,120,360))
            emptymo = np.empty((12-months,120,360))
            emptymo[:,:,:] = np.nan
            lastyear = np.append(lastyearq,emptymo,axis=0)
            var[i,:,:,:] = lastyear
            
            month = datetime.date(yr, months, dy).strftime('%B')
            print('\nSIT data available through ---> "%s"' % month)
            print('SIT data available from ---> (%s - %s)' \
                    % (np.nanmin(years),np.nanmax(years)))
            
        elif months == 12:
            dataq = np.reshape(data,(12,120,360))        
            var[i,:,:,:] = dataq
        else:
            ValueError('Issue with reshaping SIT array from binary')
    
    ### Mask out threshold values
    var[np.where(var < threshold)] = np.nan
    print('\nMasking SIT data < %s m!' % threshold)

    print('\n*Completed: Read SIT data!')   
    
    return lats,lons,var
    
def meanThick(yearmin,yearmax,years,sit):
    """
    Function calculates climatological gridded average sea ice thickness

    Parameters
    ----------
    yearmin : integer
        min year for climatological mean
    yearmax : integer
        max year for climatological mean
    years : 1d array
        years used in prior sit array
    sit : 4d array [year,month,lat,lon]
        sea ice thickness

    Returns
    -------
    meansit : 3d array [month,lat,lon]
        average sit over set climatological bounds

    Usage
    -----
    meansit = meanThick(yearmin,yearmax,years,sit)
    """
    
    print('\n>>> Using climatology sit function!')
    
    ### Import modules
    import numpy as np
    
    ### Calculate average
    slicee = np.where((years >= yearmin) & (years <= yearmax))[0]
    print('\nClimatology calculated over (%s - %s)' \
            % (np.nanmin(years[slicee]),np.nanmax(years[slicee])))
            
    newsit = sit[slicee,:,:,:]
    meansit = np.nanmean(newsit,axis=0)
    
    print('\n*Completed: Climatology sit calculated!\n')
    return meansit