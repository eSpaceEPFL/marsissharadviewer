===========================================
Getting layers subsets using GDAL's ogr2ogr
===========================================

"GDAL (http://www.gdal.org/) is a translator library for raster and vector geospatial data formats that is released under an X/MIT style Open Source license by the Open Source Geospatial Foundation (http://www.osgeo.org/)."

Using the proper GDAL utility it is possible to **download subsets of data from MARSIS and SHARAD layers and saving it in one of the format managed by GDAL**. This can be useful to work without a network connection, download only the data of interest and can also lead to QGIS performance improvement.

Download GDAL
-------------

Information about GDAL download and installation for GNU/Linux, OSX and Windows operating systems can be found here: (https://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries)

GDAL sources can be downloaded from here (http://download.osgeo.org/gdal/)

Getting layers subsets
----------------------

The GDAL utility to fetch layers subsets is *ogr2ogr* (http://www.gdal.org/ogr2ogr.html). It is included in the GDAL installation.

The generic syntax of *ogr2ogr* command is the following:

::

    ogr2ogr -f "driver" filename PG:"host=redmine-espace.epfl.ch user=dbuser 
        dbname=dbname password=password" layer_name -spat min_lon min_lat 
        max_lon max_lat -where "restricted_where" -select "field1, field2 [,...]"


* *driver*: name of the GDAL driver to use to write data
* *filename*: name of the output file
* *dbuser*: database username. Please refer to :doc:`connections`
* *dbmane*: name of the database to fetch data from. Please refer to :doc:`connections`
* *password*: password provided to the users
* *layer_name*: name of the layer to fetch data from. Please refer to :doc:`layers`
* *min_lon* *min_lat* *max_lon* *max_lat*: longitude and latitude extent
* *restricted_where*: list of attribute to include in the output. Please refer to :doc:`data`

examples:
^^^^^^^^^
::

    ogr2ogr -f "GML" file.gml PG:"host=redmine-espace.epfl.ch user=dbuser dbname=dbname
         password=password" marsis_orbit_points_180 -spat -10 -30 10 30 

Fetches data of MARSIS sampling points from table *marsis_orbit_points_180* with **longitude between 10°W and 10°E and latitude between 30°S and 30°N** and save it in *file.gml* using GML format.

::

    ogr2ogr -f "SQLite" file.sqlite PG:"host=redmine-espace.epfl.ch user=dbuser 
        dbname=dbname password=password" marsis_orbit_points_180 
        -where "orbit>=8000 and orbit<=8999"


Fetches data of MARSIS sampling points from table *marsis_orbit_points_180* with **orbit number between 8000 and 8999** and save it in *file.sqlite* using SQLite format.

::

    ogr2ogr -f "SQLite" file.sqlite PG:"host=redmine-espace.epfl.ch user=dbuser 
        dbname=dbname password=password" marsis_orbit_points_180
         -select "orbit, point_id,sunzenith"

Fetches data of MARSIS sampling points from table *marsis_orbit_points_180* **restricted to orbit number, orbit point id and solar zenith angle** and save it in *file.sqlite* using SQLite format.


* For a detaild description* of *ogr2ogr* syntax please refer to http://download.osgeo.org/gdal/ or the documentation of your GDAL installation.






