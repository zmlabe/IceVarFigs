# Weather and Climate Variability Graphics [![DOI](https://zenodo.org/badge/107888830.svg)](https://zenodo.org/badge/latestdoi/107888830)


Repository contains all of the scripts used in making the figures within (http://sites.uci.edu/zlabe/arctic-sea-ice-figures/). Scripts are *not* intended to be the most efficient or simplest method of plotting and reading data. However, they work for their current purpose. Check back soon for new scripts and/or comments!

###### Under construction... ```[Python 3.6]```

## Contact
Zachary Labe - [Research Website](http://sites.uci.edu/zlabe/) - [@ZLabe](https://twitter.com/ZLabe)

## Description
+ ```Data/```: Additional data files not provided by Python URL functions
+ ```Examples/```: Arbitrary figures as examples from listed scripts
+ ```Figures/```: Output directory for figures produced by the scripts (intentionally empty)
+ ```Scripts/```: Main [Python](https://www.python.org/) scripts/functions used in data analysis and plotting. More details are provided in ```explainScripts.txt``` for each script and function.
+ ```requirements.txt```: List of environments and modules associated with the most recent version of this project. A Python [Anaconda3 Distribution](https://docs.continuum.io/anaconda/) was used for the analysis. Tools including [NCL 6.4.0](https://www.ncl.ucar.edu/), [CDO](https://code.mpimet.mpg.de/projects/cdo), and [NCO](http://nco.sourceforge.net/) were also used for initial data manipulation. [ImageMagick](https://www.imagemagick.org/script/index.php) is used for most of the animations (GIF). All code has been tested with Python ```3.6```.

## Data
###### Land Ice Data
+ GRACE JPL RL05M.1 Mascon Solution: Version 2 : [[DATA]](https://podaac.jpl.nasa.gov/dataset/TELLUS_GRACE_MASCON_CRI_GRID_RL05_V2)
    + Wiese, D. N., D.-N. Yuan, C. Boening, F. W. Landerer, and M. M. Watkins (2016) JPL GRACE Mascon Ocean, Ice, and Hydrology Equivalent HDR Water Height RL05M.1 CRI Filtered Version 2., Ver. 2., PO.DAAC, CA, USA.
    + Watkins, M. M., D. N. Wiese, D. -N. Yuan, C. Boening, and F. W. Landerer (2015), Improved methods for observing Earth's time variable mass distribution with GRACE using spherical cap mascons, J. Geophys. Res. Solid Earth, 120, 2648_2671, doi: 10.1002/2014JB011547. [[Publication]](http://onlinelibrary.wiley.com/doi/10.1002/2014JB011547/abstract)
###### Reanalysis Data 
+ ERA5 : [[DATA]](http://apps.ecmwf.int/data-catalogues/era5/?class=ea)
+ ERA-Interim (ERAi): [[DATA]](https://www.ecmwf.int/en/research/climate-reanalysis/era-interim)
    + Dee, D.P., and co-authors., 2011: The ERA-Interim reanalysis: configuration and performance of the data assimilation system. Quart. J. R. Meteorol. Soc., 137, 553-597, doi:10.1002/qj.828 [[Publication]](http://onlinelibrary.wiley.com/doi/10.1002/qj.828/abstract)
+ ERA-40 : [[DATA]](http://apps.ecmwf.int/datasets/data/era40-daily/levtype=sfc/)
    + Uppala, S. M., and co-authors., 2005: The ERA‐40 re‐analysis. Quarterly Journal of the royal meteorological society, 131(612), 2961-3012, doi:10.1256/qj.04.176 [[Publication]](http://onlinelibrary.wiley.com/doi/10.1256/qj.04.176/full)
+ ERA-20C : [[DATA]](http://apps.ecmwf.int/datasets/data/era20c-daily/levtype=sfc/type=an/)
    + Poli, P, and co-authors., 2016: ERA-20C: An Atmospheric Reanalysis of the Twentieth Century. J. Climate, 29, 4083–4097, doi: 10.1175/JCLI-D-15-0556.1. [[Publication]](http://journals.ametsoc.org/doi/10.1175/JCLI-D-15-0556.1)
+ NCEP-DOE Reanalysis 2 (R2): [[DATA]](https://www.esrl.noaa.gov/psd/data/gridded/data.ncep.reanalysis2.html)
    + M. Kanamitsu, and co-authors., 2002: NCEP-DOE AMIP-II Reanalysis (R-2). Bulletin of the American Meteorological Society, 1631-1643 [[Publication]](http://journals.ametsoc.org/doi/abs/10.1175/BAMS-83-11-1631)
+ NCEP/NCAR Reanalysis 1 (R1): [[DATA]](https://www.esrl.noaa.gov/psd/data/gridded/data.ncep.reanalysis.html)
    + Kalnay, E., and co-authors, 1996: The NCEP/NCAR 40-year reanalysis project. Bulletin of the American meteorological Society, 77(3), 437-471 [[Publication]](http://journals.ametsoc.org/doi/abs/10.1175/1520-0477(1996)077%3C0437:TNYRP%3E2.0.CO;2)
+ NOAA-CIRES Twentieth Century Reanalysis (20CRv2c) : [[DATA]](https://www.esrl.noaa.gov/psd/data/gridded/data.20thC_ReanV2.html)
    + Compo, G.P., and co-authors., 2011: The Twentieth Century Reanalysis Project. Quarterly J. Roy. Meteorol. Soc., 137, 1-28. DOI: 10.1002/qj.776. [[Publication]](http://onlinelibrary.wiley.com/doi/10.1002/qj.776/abstract)
+ NOAA-CIRES-DOE Twentieth Century Reanalysis (20CRv3) : [[DATA]](https://www.esrl.noaa.gov/psd/data/gridded/data.20thC_ReanV3.html)
    + Slivinski, L. C., Compo, G. P., Whitaker, J. S., Sardeshmukh, P. D., Giese, B. S., McColl, C., ... & Kennedy, J. (2019). Towards a more reliable historical reanalysis: Improvements for version 3 of the Twentieth Century Reanalysis system. Quarterly Journal of the Royal Meteorological Society. [[Publication]](https://rmets.onlinelibrary.wiley.com/doi/full/10.1002/qj.3598)
###### Sea Ice Concentration/Extent
+ AMSR2 (ASI 3.125 km, UAH-processed) : [[DATA]](http://icdc.cen.uni-hamburg.de/daten/cryosphere.html)
    + Beitsch, A.; Kaleschke, L.; Kern, S. Investigating High-Resolution AMSR2 Sea Ice Concentrations during the February 2013 Fracture Event in the Beaufort Sea, 2014: Remote Sens. 6, 3841-3856, doi:10.3390/rs6053841 [[Publication]](http://www.mdpi.com/2072-4292/6/5/3841)
+ AMSR2 (JAXA Arctic Data archive System, NIPR) : [[DATA]](https://ads.nipr.ac.jp/vishop/#/monitor)
+ Gridded Monthly Sea Ice Extent and Concentration, 1850 Onward, Version 1 : [[DATA]](http://nsidc.org/data/g10010)
    + Walsh, John E., Florence Fetterer, J. Scott Stewart, and William L. Chapman. 2016. A database for depicting Arctic sea ice variations back to 1850. Geographical Review. doi: 10.1111/j.1931-0846.2016.12195.x. [[Publication]](http://onlinelibrary.wiley.com/doi/10.1111/j.1931-0846.2016.12195.x/abstract)
+ Sea Ice Index, Version 3 : [[DATA]](https://nsidc.org/data/seaice_index/)
    + Fetterer, F., K. Knowles, W. Meier, M. Savoie, and A. K. Windnagel, 2017: updated daily. Sea Ice Index, Version 3. Boulder, Colorado USA. NSIDC: National Snow and Ice Data Center. doi:http: //dx.doi.org/10.7265/N5K072F8. [[Documentation]](http://nsidc.org/data/g02135)
+ SSMIS Sea Ice Concentration (EUMETSAT OSI SAF) : [[DATA]](http://osisaf.met.no/p/ice/#conc_details)
###### Sea Ice Thickness
+ Pan-Arctic Ice Ocean Modeling and Assimilation System (PIOMAS) : [[DATA]](http://psc.apl.uw.edu/research/projects/arctic-sea-ice-volume-anomaly/data/model_grid)
    + Zhang, J., and D. A. Rothrock, 2003: Modeling Global Sea Ice with a Thickness and Enthalpy Distribution Model in Generalized Curvilinear Coordinates. Monthly Weather Review, 131 (5), 845–861, doi:10.1175/1520-0493(2003)131<0845:MGSIWA>2.0.CO;2 [[Publication]](http://journals.ametsoc.org/doi/abs/10.1175/1520-0493%282003%29131%3C0845%3AMGSIWA%3E2.0.CO%3B2)
###### Sea Surface Temperatures
+ Extended Reconstructed Sea Surface Temperature (ERSST) v5 : [[DATA]](https://www1.ncdc.noaa.gov/pub/data/cmb/ersst/v5/netcdf/)
    + Huang, B., Peter W. Thorne, et. al, 2017: Extended Reconstructed Sea Surface Temperature version 5 (ERSSTv5), Upgrades, validations, and intercomparisons. J. Climate, doi: 10.1175/JCLI-D-16-0836.1 [[Publication]](http://journals.ametsoc.org/doi/10.1175/JCLI-D-16-0836.1)
+ NOAA Optimum Interpolation Sea Surface Temperature High Resolution (OISST) v2 : [[DATA]](https://www.esrl.noaa.gov/psd/data/gridded/data.noaa.oisst.v2.highres.html)
    + Reynolds, Richard W., Thomas M. Smith, Chunying Liu, Dudley B. Chelton, Kenneth S. Casey, Michael G. Schlax, 2007: Daily High-Resolution-Blended Analyses for Sea Surface Temperature. J. Climate, 20, 5473-5496. doi: 10.1175/2007JCLI1824.1 [[Publication]](https://journals.ametsoc.org/doi/abs/10.1175/2007JCLI1824.1)
