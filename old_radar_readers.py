# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import os

from urllib import urlretrieve

import numpy as np
from PIL import Image as im

import prefs

class RadarReader(object):
    """
    """
    def __init__(self, base_dir, file_prefix, file_suffix):

        self.base_dir = base_dir
        self.file_prefix = file_prefix
        self.file_suffix = file_suffix

#        self.orbit_str = str(orbit)
#        if len(self.orbit_str) == 4:
#            self.orbit_str = "0"+self.orbit_str
#
#        self.orbit_dir = self.get_orbit_dir()
#
#        self.orbit_file = base_dir+orbit_dir+"/"+file_prefix+self.orbit_str+file_suffix
#        self.cached_file = [prefs.CHACHE_BASE_DIR+orbit_dir+"/", file_prefix+self.orbit_str+file_suffix]

        self.fetcher = url_fetch

    def get_data(self, orbit):
        """
        """
        orbit_str = str(orbit)
        if len(orbit_str) == 4:
            orbit_str = "0"+orbit_str

        orbit_dir = self.get_orbit_dir(orbit_str)

        self.orbit_file = self.base_dir+orbit_dir+"/"+self.file_prefix+orbit_str+self.file_suffix
        self.cached_file = [prefs.CHACHE_BASE_DIR+orbit_dir+"/", self.file_prefix+orbit_str+self.file_suffix]
        self.orbit_file = self.base_dir+orbit_dir+"/"+self.file_prefix+orbit_str+self.file_suffix
        self.cached_file = [prefs.CHACHE_BASE_DIR+orbit_dir+"/", self.file_prefix+orbit_str+self.file_suffix]



class PngReader(RadarReader):
    """
    """
    def get_data(self, orbit):
        """
        """
        super(PngReader, self).get_data(orbit)

        self.fh = self.fetcher(self.orbit_file, self.cached_file)
        data = np.hsplit(np.rot90(np.asarray(self.fh), k=3),6)
        data.reverse()
        data1=[]
        data1.append(data[0:3])
        data1.append(data[4:6])
        return data1

class RadarPngReader(PngReader):
    """
    """

    def get_orbit_dir(self, orbit_str):
        return L2_orbit_dir(orbit_str)


class SimPngReader(PngReader):
    """
    """

    def get_orbit_dir(self, orbit_str):
        return SIM_orbit_dir(orbit_str)


def disk_fetch(filename, chaced_file):
    return im.open(filename)

def url_fetch(url, cached_file):
    if not os.path.exists(cached_file[0]):
        os.makedirs(cached_file[0])
    (cached_file, headers) = urlretrieve(url, cached_file[0]+cached_file[1])
    return disk_fetch(cached_file, None)

def L2_orbit_dir(orbit_str):
    return "RDR"+orbit_str[0:-1]+"X"

def SIM_orbit_dir(orbit_str):
    return "SIM"
