=============
Included data
=============

For each radar sampling point, the _points_ layers provide the follwing data:

MARSIS layers:
--------------

* *point_id*: id of the corresponding radargram column 
* *scetw*: SCET timeof the frame (whole)   
* *scetf*: SCET timeof the frame (frac)   
* *ephemt*: Ephemeris time (number of seconds since Jan 1 2000 - 12:00 UTC)  
* *geoep*: Ephemeris time in UTC format
* *sunlon*: Mars solar longitude  
* *sundist*: Mars to Sun distance 
* *orbit*: Orbit number of the related dataproduct  
* *target*: Celestial body observed  
* *tarscx*: Target posistion (X component)  
* *tarscy*: Target posistion (Y component)  
* *tarscz*: Target posistion (Z component)  
* *scalt*: Distance from the Mars Express spacecraft to the reference surface   
* *scelon*: Longitude of the footprint location    
* *sclat*: Latitude of the footprint location   
* *tarscvx*: Mars Express spacecraft velocity vector in the reference frame of the target body (X component) 
* *tarscvy*: Mars Express spacecraft velocity vector in the reference frame of the target body (Y component) 
* *tarscvz*: Mars Express spacecraft velocity vector in the reference frame of the target body (Z component) 
* *tarscradv*: Radial component of the Mars Express spacecraft velocity vector in the reference frame of the target body
* *tarsctanv*: Tangential component of the Mars Express spacecraft velocity vector in the reference frame of the target body
* *locsunt*: Local true solar time  
* *sunzenith*: Solar zenith angle     
* *dipx*: Unit vector directed along MARSIS dipole Antenna in the reference frame of the target body (X component)     
* *dipy*: Unit vector directed along MARSIS dipole Antenna in the reference frame of the target body (Y component)     
* *dipz*: Unit vector directed along MARSIS dipole Antenna in the reference frame of the target body (Z component)     
* *monox*: Unit vector directed along MARSIS monopole Antenna in the reference frame of the target body (X component)
* *monoy*: Unit vector directed along MARSIS monopole Antenna in the reference frame of the target body (Y component)    
* *monoz*: Unit vector directed along MARSIS monopole Antenna in the reference frame of the target body (Z component)    
* *f1*: Values in Hz of the first radar frequency
* *f2*: Values in Hz of the second radar frequency
* *snr_f1_m1*: [[Signal to noise ratio]] of the first frequency, filter -1 
* *snr_f1__0*: [[Signal to noise ratio]] of the first frequency, filter 0 
* *snr_f1_p1*: [[Signal to noise ratio]] of the first frequency, filter 1 
* *snr_f2_m1*: [[Signal to noise ratio]] of the second frequency, filter -1 
* *snr_f2__0*: [[Signal to noise ratio]] of the second frequency, filter 0  
* *snr_f2_p1*: [[Signal to noise ratio]] of the second frequency, filter 1 

SHARAD layers:
--------------

The data provided in the SHARAD layers are those included in the SHARAD geometric data files (_http://pds-geosciences.wustl.edu/mro/mro-m-sharad-5-radargram-v1/mrosh_2001/data/geom/_)

* *point_id*: id of the corresponding radargram column 
* *epoch*: UT date and time of observation   
* *lat*: Latitude of the footprint location
* *lon*: Longitude of the footprint location  
* *mars_r*: Radius of Mars at the footprint time
* *sc_r*: Distance from center of mass to MRO    
* *rad_v*: MRO radial velocity
* *tan_v*: MRO tangential velocity   
* *sza*: Solar zenith angle     
* *phase*: Signal phase distortion   
* *orbit*: Orbit number of the related dataproduct

