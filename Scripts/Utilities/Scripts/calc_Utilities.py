"""
Functions are useful utilities for test scripts in scicomm
 
Notes
-----
    Author : Zachary Labe
    Date   : 3 March 2018
    
Usage
-----
    [1] calcDecJanFeb(varx,lat,lon,level,levsq)
"""

def calcDecJanFeb(varx,lat,lon,level,levsq):
    """
    Function calculates average for December-January-February

    Parameters
    ----------
    varx : 4d array or 5d array
        [year,month,lat,lon] or [year,month,lev,lat,lon]
    lat : 1d numpy array
        latitudes
    lon : 1d numpy array
        longitudes
    level : string
        Height of variable (surface or profile)
    levsq : integer
        number of levels
        
    Returns
    -------
    varx_djf : 3d array or 4d array
        [year,lat,lon] or [year,lev,lat,lon]

    Usage
    -----
    varx_djf = calcDecJanFeb(varx,lat,lon,level,levsq)
    """
    print('\n>>> Using calcDecJan function!')
    
    ### Import modules
    import numpy as np
    
    ### Reshape for 3d variables
    if level == 'surface':    
        varxravel = np.reshape(varx.copy(),
                           (int(varx.shape[0]*12),
                            int(lat.shape[0]),int(lon.shape[0])))
                               
        varx_djf = np.empty((varx.shape[0]-1,lat.shape[0],lon.shape[0]))               
        for i in range(0,varxravel.shape[0]-12,12):
            counter = 0
            if i >= 12:
                counter = i//12
            djfappendh1 = np.append(varxravel[11+i,:,:],varxravel[12+i,:,:])
            djfappendh = np.append(djfappendh1,varxravel[13+i,:,:])
            varx_djf[counter,:,:] = np.nanmean(np.reshape(djfappendh,
                                    (3,int(lat.shape[0]),int(lon.shape[0]))),
                                    axis=0)                   
            
    ### Reshape for 4d variables
    elif level == 'profile':
        varxravel = np.reshape(varx.copy(),
                           (int(varx.shape[0]*12.),levsq,
                            int(lat.shape[0]),int(lon.shape[0])))
                               
        varx_djf = np.empty((int(varx.shape[0]-1),levsq,
                            int(lat.shape[0]),int(lon.shape[0])))               
        for i in range(0,varxravel.shape[0]-12,12):
            counter = 0
            if i >= 12:
                counter = i//12
            djfappendh1 = np.append(varxravel[11+i,:,:,:],
                                  varxravel[12+i,:,:,:])
            djfappendh = np.append(djfappendh1,
                                  varxravel[13+i,:,:,:]) 
            varx_djf[counter,:,:] = np.nanmean(np.reshape(djfappendh,
                                    (3,levsq,int(lat.shape[0]),
                                     int(lon.shape[0]))),axis=0)                                                
    else:
        print(ValueError('Selected wrong height - (surface or profile!)!'))    
                                
    print('Completed: Organized data by months (DJF)!')

    print('*Completed: Finished calcDecJanFeb function!')
    return varx_djf