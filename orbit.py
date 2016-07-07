# -*- coding: utf-8 -*-
# Copyright (C) 2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

from collections import OrderedDict

class Orbit(object):
    """
    """

    def __init__(self, orbit_id):
        self.id = orbit_id
        self.point_id_dict = OrderedDict()
#        self.point_id_dict['lon'] = {}
#        self.point_id_dict['lat'] = {}
#        self.point_id_dict['proj_x'] = {}
#        self.point_id_dict['proj_y'] = {}
        self.layer = None
        self.data = []
        self.sim = []
        self.v_scale = None
        self.crs = None
        self.data_reader = None
        self.instrument = None
        self.range = None
        self.sim_reader = None

#        self.lat_dict = {}
#        self.lon_dict = {}
#        self.point_id = []
#        self.proj_x_dict = {}
#        self.lon = []
#        self.proj_y_dict = {}
#        self.lat = []
#        self.proj_x = []
#        self.proj_y = []

    def set_id(self, value):
        self.id= value

    def get_id(self):
        return self.id

    def set_layer(self, value):
        self.layer = value

    def get_layer(self):
        return self.layer

    def set_data_reader(self, value):
        self.data_reader = value

    def get_data_reader(self):
        return self.data_reader

    def set_sim_reader(self, value):
        self.sim_reader = value

    def get_sim_reader(self):
        return self.sim_reader

    def set_instrument(self, value):
        self.instrument = value

    def get_instrument(self):
        return self.instrument

    def set_crs(self, value):
        self.crs= value

    def get_crs(self):
        return self.crs

    def add_point_id(self, point_id):
        self.point_id_dict[point_id] = {}

    def add_lon(self, point_id, lon):
        self.point_id_dict[point_id]['lon'] = lon

    def get_lon(self, point_id):
        return self.point_id_dict[point_id]['lon']

    def add_lat(self, point_id, lat):
        self.point_id_dict[point_id]['lat'] = lat

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

    def add_proj_x(self, point_id, proj_x):
        self.point_id_dict[point_id]['proj_x'] = proj_x

    def get_proj_x(self, point_id):
        return self.point_id_dict[point_id]['proj_x']

    def add_proj_y(self, point_id, proj_y):
        self.point_id_dict[point_id]['proj_y'] = proj_y

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

#    def add_point_id(self, value):
#        self.point_id.append(value)
#
#    def rem_point_id(self, value):
#        self.point_id.remove(value)
