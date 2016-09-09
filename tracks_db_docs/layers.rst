================
Available layers
================

Several layers are available for MARSIS and SHARAD tracks data.

*_point* layers contain, for each radar sampling point, geometric data and other metadata. For the list of the included data see :doc:`data`.

*_lines* layers are intended for a quick visualization of the orbit footprint without providing further details included in the *_point* layers. They can be used to show the track number on the QGIS canvas and maps.

In the layers named with the **_180_ suffix**, the **longitude** is represented **between -180° and +180°**. In the other layers the longitude is represented **between 0° and 360°**. 

Using PostGIS DB connection
---------------------------

For the PostGIS connection parameters refer to :doc:`connections`

MARSIS layers
~~~~~~~~~~~~~

* *orbit_point*: MARSIS sampling points (longitude between 0° and 360°. Features geometry type is *point*)
* *marsis_orbit_points_180*: MARSIS sampling points (longitude between -180° and 180°. Features geometry type is *point*)
* *marsis_orbit_lines*: MARSIS orbit tracks (longitude between 0° and 360°. Features geometry type is *line*)
* *marsis_orbit_lines_180*: MARSIS orbit tracks (longitude between -180° and 180°. Features geometry type is *line*)

SHARAD layers
~~~~~~~~~~~~~

* *orbit_point*: SHARAD sampling points (longitude between 0° and 360°. Features geometry type is *point*)
* *sharad_orbit_points_180*: SHARAD sampling points (longitude between -180° and 180°. Features geometry type is *point*)
* *sharad_orbit_lines*: SHARAD orbit tracks (longitude between 0° and 360°. Features geometry type is *line*)
* *sharad_orbit_lines_180*: SHARAD orbit tracks (longitude between -180° and 180°. Features geometry type is *line*)


Tracks layers in SQLite format
------------------------------

The aforementioned tracks layers are also available in *SQLite* format from TBA.

Both for MARSIS and SHARAD, the DB is partitioned as follow:




