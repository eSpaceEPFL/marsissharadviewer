# -*- coding: utf-8 -*-
# Copyright (C) 2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

from qgis.core import QgsFeatureRequest, QgsCoordinateTransform

import prefs

class GetFeatureData():

    def get_layers(self):


#        self.layers = [self.iface.activeLayer()]
        self.layers = [] #[self.iface.mapCanvas()]
        self.reader = []
        self.radar_reader = []
        self.sim_reader = []
        self.orbit_field_name = []
        self.instrument = []
        for layer in self.iface.mapCanvas().layers():
            if ((layer.name().find('MARSIS') > -1) or (layer.name().find('marsis') > -1)) and layer.fieldNameIndex('point_id') > -1 and layer.fieldNameIndex(prefs.ORBIT['MARSIS']) > -1:
                self.layers.append(layer)
                self.radar_reader.append(prefs.RADAR_READER['MARSIS'])
                self.sim_reader.append(prefs.SIM_READER['MARSIS'])
                self.orbit_field_name.append(prefs.ORBIT['MARSIS'])
                self.instrument.append('MARSIS')

            if ((layer.name().find('SHARAD') > -1) or (layer.name().find('sharad') > -1)) and layer.fieldNameIndex('point_id') > -1 and layer.fieldNameIndex(prefs.ORBIT['SHARAD']) > -1:
                self.layers.append(layer)
                self.radar_reader.append(prefs.RADAR_READER['SHARAD'])
                self.sim_reader.append(prefs.SIM_READER['SHARAD'])
                self.orbit_field_name.append(prefs.ORBIT['SHARAD'])
                self.instrument.append('SHARAD')

        self.orbits = {}

    def get_selected_features(self):
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
                    self.orbits[key] = {'point_id': [],
                                        'lat': [],
                                        'lat_dict': {},
                                        'lon': [],
                                        'lon_dict': {},
                                        'proj_x': [],
                                        'proj_x_dict': {},
                                        'proj_y': [],
                                        'proj_y_dict': {}}
                    self.orbits[key]['layer'] = self.layers[ii]

                    self.orbits[key]['data_reader'] = self.radar_reader[ii]
                    self.orbits[key]['sim_reader'] = self.sim_reader[ii]
#                self.orbits[key]['orbit'] = self.orbit_field_name[ii]
                    self.orbits[key]['instrument'] = self.instrument[ii]
                    self.orbits[key]['crs'] = self.layers[ii].crs()

                point_id = feature.attribute('point_id')
                self.orbits[key]['point_id'].append(point_id)
                point = feature.geometry().asPoint()
                self.orbits[key]['lat_dict'][point_id] =  point[1] #feature.geometry().asPoint()[1]
                self.orbits[key]['lon_dict'][point_id] =  point[0] #feature.geometry().asPoint()[0]
                (self.orbits[key]['proj_x_dict'][point_id], self.orbits[key]['proj_y_dict'][point_id]) = xform.transform(point)



    def get_data(self):

        for orbit in self.orbits.keys():
            self.orbits[orbit]['point_id'].sort()
            for point in self.orbits[orbit]['point_id']:

                self.orbits[orbit]['lat'].append(self.orbits[orbit]['lat_dict'][point])
                self.orbits[orbit]['lon'].append(self.orbits[orbit]['lon_dict'][point])

                self.orbits[orbit]['proj_x'].append(self.orbits[orbit]['proj_x_dict'][point])
                self.orbits[orbit]['proj_y'].append(self.orbits[orbit]['proj_y_dict'][point])

#            tree_item = QTreeWidgetItem([orbit])

#            r_read = rr.RadarPngReader(orbit, prefs.L2_DIR["MARSIS"], prefs.L2_PREFIX["MARSIS"], prefs.L2_SUFFIX["MARSIS"])
#            s_read = rr.SimPngReader(orbit, prefs.SIM_DIR["MARSIS"], prefs.SIM_PREFIX["MARSIS"], prefs.SIM_SUFFIX["MARSIS"])
#
#            self.orbits[orbit]['data'] = r_read.get_data()
#            self.orbits[orbit]['sim'] = s_read.get_data()
            self.orbits[orbit]['data'] = self.orbits[orbit]['data_reader'].get_data(orbit)
            self.orbits[orbit]['sim'] = self.orbits[orbit]['sim_reader'].get_data(orbit)

            self.orbits[orbit]['v_scale'] = self.orbits[orbit]['data_reader'].get_v_scale(orbit)

#            f1 = np.mean(np.array(orbits[orbit]['data'][0:3]),0)
#            f2 = np.mean(np.array(orbits[orbit]['data'][3:6]),0)
            self.orbits[orbit]['range'] = [min(self.orbits[orbit]['point_id']), max(self.orbits[orbit]['point_id'])]

            if (not self.orbits[orbit]['data']) and (not self.orbits[orbit]['sim']):
                 self.orbits[orbit] = None
                 print "orbit "+ orbit + " removed"

#            for point in orbits[orbit]['point_id']:
#
#                tree_item.addChild(QTreeWidgetItem([str(point)]))
#
#            self.data_tree.addTopLevelItem(tree_item)

    def gfd_reset(self):
        print "reset"
        self.orbits = None