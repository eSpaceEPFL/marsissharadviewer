# -*- coding: utf-8 -*-
# Copyright (C) 2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

from qgis.core import QgsFeatureRequest, QgsCoordinateTransform
from orbit import *

class GetFeatureData():
    """Implement data retrieval

    *Methods*
    * __init__ - Inizialize the class
    * get_layers - Get MARSIS and SHARAD layers from QGIS interface
    * get_selected_features - Get selected orbit points andd related data from QGIS canvas
    * get_data - Get radargrams
    * gfd_reset - Remove reference to orbit data
    """

    def __init__(self, iface, prefs):
        """Inizialize the class

        iface: QGIS interface
        prefs: Instance of preference (prefs) class
        """

        self.iface = iface
        self.prefs = prefs

    def get_layers(self):
        """Get MARSIS and SHARAD layers from QGIS interface
        """

#        self.layers = [self.iface.activeLayer()]
        self.layers = [] #[self.iface.mapCanvas()]
        self.reader = []
        self.radar_reader = []
        self.sim_reader = []
        self.orbit_field_name = []
        self.instrument = []
        for layer in self.iface.mapCanvas().layers():
            if ((layer.name().find('MARSIS') > -1) or (layer.name().find('marsis') > -1)) and layer.fieldNameIndex('point_id') > -1 and layer.fieldNameIndex(self.prefs.ORBIT['MARSIS']) > -1:
                self.layers.append(layer)
                self.radar_reader.append(self.prefs.RADAR_READER['MARSIS'])
                self.sim_reader.append(self.prefs.SIM_READER['MARSIS'])
                self.orbit_field_name.append(self.prefs.ORBIT['MARSIS'])
                self.instrument.append('MARSIS')

            if ((layer.name().find('SHARAD') > -1) or (layer.name().find('sharad') > -1)) and layer.fieldNameIndex('point_id') > -1 and layer.fieldNameIndex(self.prefs.ORBIT['SHARAD']) > -1:
                self.layers.append(layer)
                self.radar_reader.append(self.prefs.RADAR_READER['SHARAD'])
                self.sim_reader.append(self.prefs.SIM_READER['SHARAD'])
                self.orbit_field_name.append(self.prefs.ORBIT['SHARAD'])
                self.instrument.append('SHARAD')

        if not self.layers:
            return 0

        self.orbits = {}

        return 1

    def get_selected_features(self):
        """Get selected orbit points andd related data from QGIS canvas
        """

        map_crs = self.iface.mapCanvas().mapRenderer().destinationCrs()

        features_ids = [layer.selectedFeaturesIds() for layer in self.layers]
        req = [QgsFeatureRequest().setFilterFids(layer_features_ids) for layer_features_ids in features_ids]
#        [lreq.setSubsetOfAttributes([0, 1]) for lreq in req]
        for ii in range(len(self.layers)):
            req[ii].setSubsetOfAttributes([self.layers[ii].fieldNameIndex(self.orbit_field_name[ii]),
                                           self.layers[ii].fieldNameIndex('point_id'),
                                           self.layers[ii].fieldNameIndex('wkb_geometry')])

        fit = [self.layers[ii].getFeatures(req[ii]) for ii in range(len(self.layers))]

#        for feature in self.layer.selectedFeaturesIterator():
        for ii in range(len(self.layers)):
            xform = QgsCoordinateTransform(self.layers[ii].crs(), map_crs)
            for feature in fit[ii]:
                key = str(feature.attribute(self.orbit_field_name[ii]))
                if self.orbits.has_key(key) == False:
                    self.orbits[key] = Orbit(key)

                    self.orbits[key].set_layer (self.layers[ii])

                    self.orbits[key].set_data_reader(self.radar_reader[ii])
                    self.orbits[key].set_sim_reader(self.sim_reader[ii])
#                self.orbits[key]['orbit'] = self.orbit_field_name[ii]
                    self.orbits[key].set_instrument(self.instrument[ii])
                    self.orbits[key].set_crs(self.layers[ii].crs())

                point_id = feature.attribute('point_id')
                self.orbits[key].add_point_id(point_id)
                point = feature.geometry().asPoint()
                self.orbits[key].add_lat(point_id, point[1]) #feature.geometry().asPoint()[1]
                self.orbits[key].add_lon(point_id, point[0]) #feature.geometry().asPoint()[0]
                (proj_x, proj_y) = xform.transform(point)
                self.orbits[key].add_proj_x(point_id, proj_x)
                self.orbits[key].add_proj_y(point_id, proj_y)

        if not (self.orbits):
            return 0

        return 1


    def get_data(self):
        """Get radargrams
        """
        removed = []
        for orbit in self.orbits.keys():
            self.orbits[orbit].sort_point_dict()
            self.orbits[orbit].read_data()
            self.orbits[orbit].read_sim()
            self.orbits[orbit].get_v_scale()

            self.orbits[orbit].set_range()

            #Remove orbit from dictionary if data is unavailable
            if (not self.orbits[orbit].data) and (not self.orbits[orbit].sim):
                 del self.orbits[orbit]
#                 self.orbits[orbit] = None
                 removed.append(orbit)

#            for point in orbits[orbit]['point_id']:
#
#                tree_item.addChild(QTreeWidgetItem([str(point)]))
#
#            self.data_tree.addTopLevelItem(tree_item)

        return removed

    def gfd_reset(self):
        """Remove reference to orbit data
        """

        self.orbits = None