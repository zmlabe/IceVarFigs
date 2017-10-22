"""
Script calculates area of PIOMAS grid. 
 
Notes
-----
    Source : http://psc.apl.washington.edu/zhang/IDAO/data_piomas.html
    Author : Zachary Labe
    Date   : 12 September 2016
    
Usage
-----
    area = readPiomasArea(directory)
"""

def readPiomasArea(directory):
    """
    Function calculates area of PIOMAS grid cells 

    Parameters
    ----------
    directory : string
        working directory for stored PIOMAS files

    Returns
    -------
    area : 2d array [lat,lon]
        area of grid cell

    Usage
    -----
    lats,lons,var = readPiomas(directory,years,threshold)
    """
    
    print('\n>>> Using readPiomasArea function!')
    
    ### Import modules
    import numpy as np

    ### Read in grids
    grid = np.genfromtxt(directory + 'griddata.txt')
    grid = np.reshape(grid,(grid.size))  
    
    ### Define Lat/Lon (sea PIOMAS grid documentation, fortran)
    lon = grid[:43200]   
    lons = np.reshape(lon,(120,360))
    lat = grid[43200:43200*2]
    lats = np.reshape(lat,(120,360))
    
    htn = grid[43200*2:43200*3]
    htn = np.reshape(htn,(120,360))
    hte = grid[43200*3:43200*4]
    hte = np.reshape(hte,(120,360))
    
    hts = grid[43200*4:43200*5]
    hts = np.reshape(hts,(120,360))
    htw = grid[43200*5:43200*6]
    htw = np.reshape(htw,(120,360))
    
    ex = grid[43200*6:43200*7]
    ex = np.reshape(ex,(120,360))
    
    print('Calculating area of grid cell')
    area = htn*hte
    
    print('*Completed: Area of PIOMAS calculated!')
    return area