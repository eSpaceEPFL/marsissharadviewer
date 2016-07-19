# -*- coding: utf-8 -*-
# Copyright (C) 2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

from collections import OrderedDict

from qgis.core import QgsFeatureRequest, QgsCoordinateTransform

class Orbit(object):
    """
    """

    def __init__(self,
                 orbit_id,
                 prefs = None,
                 layer = None,
                 data_reader = None,
                 sim_reader = None,
                 instrument = None,
                 map_crs = None):

        self.id = orbit_id
        self.prefs = prefs
        self.layer = layer
        self.data_reader = data_reader
        self.sim_reader = sim_reader
        self.instrument = instrument
        self.map_crs = map_crs


#        self.xform = xform
        self.point_id_dict = OrderedDict()
        self.crs = self.layer.crs()
        self.xform = QgsCoordinateTransform(self.crs, map_crs)

        self.data = []
        self.sim = []
        self.v_scale = None

        self.range = None

        self.map_avail_feats = None
        self.map_avail_feats_d = None
        self.map_avail_ids = None

#    def set_id(self, value):
#        self.id= value
#
    def get_id(self):
        return self.id
#
#    def set_layer(self, value):
#        self.layer = value
#
    def get_layer(self):
        return self.layer
#
#    def set_data_reader(self, value):
#        self.data_reader = value
#
#    def get_data_reader(self):
#        return self.data_reader
#
#    def set_sim_reader(self, value):
#        self.sim_reader = value
#
    def get_sim_reader(self):
        return self.sim_reader
#
#    def set_instrument(self, value):
#        self.instrument = value
#
    def get_instrument(self):
        return self.instrument


    def add_feature_point(self, feature):
        point_id = feature.attribute('point_id')
        self.point_id_dict[point_id] = {}
        self.point_id_dict[point_id]['feat'] = feature
        point = feature.geometry().asPoint()
        self.point_id_dict[point_id]['lat'] = point[1]
        self.point_id_dict[point_id]['lon'] = point[0]
        (proj_x, proj_y) = self.xform.transform(point)
        self.point_id_dict[point_id]['proj_x'] = proj_x
        self.point_id_dict[point_id]['proj_y'] = proj_y


#    def add_lon(self, point_id, lon):
#        self.point_id_dict[point_id]['lon'] = lon

    def get_lon(self, point_id):
        return self.point_id_dict[point_id]['lon']

#    def add_lat(self, point_id, lat):
#        self.point_id_dict[point_id]['lat'] = lat

    def get_lat(self, point_id):
        return self.point_id_dict[point_id]['lat']

    def _dict_0(self, d_key):
        point_id = self.point_id_dict.keys()[0]
        return self.point_id_dict[point_id][d_key]

    def _dict_f(self, d_key):
        point_id = self.point_id_dict.keys()[-1]
        return self.point_id_dict[point_id][d_key]

    def lon_0(self):
        return self._dict_0('lon')

    def lon_f(self):
        return self._dict_f('lon')

    def lat_0(self):
        return self._dict_0('lat')

    def lat_f(self):
        return self._dict_f('lat')

#    def add_proj_x(self, point_id, proj_x):
#        self.point_id_dict[point_id]['proj_x'] = proj_x

    def get_proj_x(self, point_id):
        return self.point_id_dict[point_id]['proj_x']

#    def add_proj_y(self, point_id, proj_y):
#        self.point_id_dict[point_id]['proj_y'] = proj_y

    def get_proj_y(self, point_id):
        return self.point_id_dict[point_id]['proj_y']

    def _get_dict_as_list(self, d_key):
        l = []
        for point_id in self.point_id_dict.keys():
            l.append(self.point_id_dict[point_id][d_key])

        return l

    def get_lon_list(self):
        return self._get_dict_as_list('lon')

    def get_lat_list(self):
        return self._get_dict_as_list('lat')

    def get_proj_x_list(self):
        return self._get_dict_as_list('proj_x')

    def get_proj_y_list(self):
        return self._get_dict_as_list('proj_y')

    def sort_point_dict(self):
        """ TO BE CALLED AFTER DICT 'LOADING'
        """
        temp_d = OrderedDict()
        point_id_sorted = self.point_id_dict.keys()
        point_id_sorted.sort()
        for point_id in point_id_sorted:
            temp_d[point_id] = self.point_id_dict[point_id]

        self.point_id_dict = temp_d

    def read_data(self):
        self.data = self.data_reader.get_data(self.id)

    def read_sim(self):
        self.sim = self.sim_reader.get_data(self.id)

    def read_v_scale(self):
        self.v_scale = self.data_reader.get_v_scale(self.id)

    def get_v_scale(self):
        return self.v_scale

    def set_range(self):
        point_ids = self.point_id_dict.keys()
        self.range = [min(point_ids), max(point_ids)]

    def get_range(self):
        return self.range

    def get_map_avail_feats(self):
        if not self.map_avail_feats:
            self.__retrieve_map_avail_feats(self)

        return self.map_avail_feats

    def __retrieve_map_avail_feats(self):

        qstring = self.prefs.ORBIT['MARSIS']+' = '+  str(self.id)
        req=QgsFeatureRequest().setFilterExpression(qstring)
        req.setSubsetOfAttributes([self.layer.fieldNameIndex(self.prefs.ORBIT['MARSIS']), self.layer.fieldNameIndex('point_id')])

        fit=self.layer.getFeatures(req)
        feats=[ f for f in fit ]
        feats.sort(key=lambda x: x.attribute('point_id'), reverse=False)

        ii = 0

        self.map_avail_ids = []
        self.map_avail_feats = []
        self.map_avail_feats_d = {}
        for f in feats:
            self.map_avail_feats.append(f.id())
            self.map_avail_ids.append(f.attribute('point_id'))
            self.map_avail_feats_d[f.attribute('point_id')] = ii
            self.add_feature_point(f)
            ii = ii + 1

    def get_map_selected_feats(self, start, stop):
        if not self.map_avail_feats:
            self.__retrieve_map_avail_feats()

        selection_start = self.map_avail_feats_d[start]
        selection_stop = self.map_avail_feats_d[stop]

        return self.map_avail_feats[selection_start:selection_stop]

    def get_map_avail_ids(self):
        if not self.map_avail_ids:
            self.__retrieve_map_avail_feats()

        return self.map_avail_ids

    def get_feature(self, point_id):
        if not self.point_id_dict.has_key(point_id):
            self.__retrieve_map_avail_feats()

        if self.point_id_dict.has_key(point_id):
            return self.point_id_dict[point_id]['feat']

        return -1
