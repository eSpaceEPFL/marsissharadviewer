================
Available layers
================

Several layers are available for MARSIS and SHARAD tracks data.

*_points* layers contain, for each radar sampling point, geometric data and other metadata. For the list of the included data see :doc:`data`.

*_lines* layers are intended for a quick visualization of the orbits' footprint without providing further details included in the *_points* layers. They can be used to show the track number on the QGIS canvas and maps.

In the layers named with the **_180_ suffix**, the **longitude** is represented **between -180° and +180°**. In the other layers the longitude is represented **between 0° and 360°**. 

PostGIS DB
----------

For the PostGIS connection parameters refer to :doc:`connections`

MARSIS layers
~~~~~~~~~~~~~

* *marsis_orbit_points*: MARSIS sampling points (longitude between 0° and 360°. Features geometry type is *point*)
* *marsis_orbit_points_180*: MARSIS sampling points (longitude between -180° and 180°. Features geometry type is *point*)
* *marsis_orbit_lines*: MARSIS orbit tracks (longitude between 0° and 360°. Features geometry type is *line*)
* *marsis_orbit_lines_180*: MARSIS orbit tracks (longitude between -180° and 180°. Features geometry type is *line*)

SHARAD layers
~~~~~~~~~~~~~

* *sharad_orbit_points*: SHARAD sampling points (longitude between 0° and 360°. Features geometry type is *point*)
* *sharad_orbit_points_180*: SHARAD sampling points (longitude between -180° and 180°. Features geometry type is *point*)
* *sharad_orbit_lines*: SHARAD orbit tracks (longitude between 0° and 360°. Features geometry type is *line*)
* *sharad_orbit_lines_180*: SHARAD orbit tracks (longitude between -180° and 180°. Features geometry type is *line*)


SQLite files
------------

The aforementioned tracks layers are also available in *SQLite* format from https://drive.google.com/open?id=0B_iYniNmEIOVVXZFRmZoeWN5MnM.

*Google drive* account is required to download the files.

The files are *zipped*.

For both MARSIS and SHARAD, the tracks files are the following:

* *_N_Pole.sqlite*: North pole, latitude > 70°, longitude between 0° and 360°
* *_N_Pole_180.sqlite*: North pole, latitude > 70°, longitude between -180° and 180°
* *_S_Pole.sqlite*: North pole, latitude < -70°, longitude between 0° and 360°
* *_S_Pole_180.sqlite*: North pole, latitude < -70°, longitude between -180° and 180°
* *_0_60E*: Longitude between 0° and 60°, latitude between -70° and 70° 
* *_60_120E*: Longitude between 60° and 120°, latitude between -70° and 70° 
* *_120_180E*: Longitude between 120° and 180°, latitude between -70° and 70° 
* *_180_240E*: Longitude between 180° and 240°, latitude between -70° and 70° 
* *_240_300E*: Longitude between 240° and 300°, latitude between -70° and 70° 
* *_300_360E*: Longitude between 300° and 360°, latitude between -70° and 70° 
* *_0_60W_180*: Longitude between 0° and -60°, latitude between -70° and 70° 
* *_60_120W_180*: Longitude between -60° and -120°, latitude between -70° and 70° 
* *_120_180W_180*: Longitude between -120° and -180°, latitude between -70° and 70° 
* *_orbit_lines*: Longitude between 0° and 360°, latitude between -90° and 90°
* *_orbit_lines_180*: Longitude between -180° and 180°, latitude between -90° and 90°  


Further layers including MOLA raster map, USGS geologic map and Mars nomenclature are available here https://drive.google.com/open?id=0B_iYniNmEIOVMXZ6aTJ2MGtGdVE.



