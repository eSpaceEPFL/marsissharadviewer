# -*- coding: utf-8 -*-
# Copyright (C) 2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import os

class OgrToOgr(object):
    """
    """
    def __init__(self):
        """
        """
        self.spat = None
        self.orbit_ranges = None

    def set_in(self, drv_str, source_str):
        self.drv_in = drv_str
        self.source_in = source_str

    def set_out(self, drv_str, source_str):
        self.drv_out = drv_str
        self.source_out = source_str

    def set_orbit_ranges(self, ranges):
        self.orbit_ranges = ranges

    def set_spat(self, spat):
        self.spat = spat

    def _set_in_str(self):
        return ' '+self.drv_in+':'+self.source_in

    def _set_out_str(self):
        return ' -f "'+self.drv_out+'" '+self.source_out+' '

    def _set_orbit_str(self):
        if  self.orbit_ranges:
            where_str = ' -where "'
            for orbit_range in self.orbit_ranges:
                where_str = where_str+' (orbit>'+str(orbit_range[0])+' and orbit <'+str(orbit_range[1])+') or'

            return where_str[:-3]+'"'
        else:
            return ''

    def _set_spat_str(self):
        if self.spat:
            return '-spat '+str(self.spat)[1:-1]
        else:
            return ''

    def run(self):
        command = "ogr2ogr"+self._set_out_str()+self._set_spat_str()+self._set_orbit_str()+self._set_in_str()
        os.system(command)

