# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import os

from urllib import urlretrieve

import numpy as np
from PIL import Image as im


###############################################################################
class DataManager(object):
    """Convert raw radargrams to internal format

    *Methods*
    * run - Execute the conversion
    """

    def run(self, raw_data):
        """Execute the conversion

        raw_data: raw radargram
        """

        pass

class ImgManager(DataManager):
    """Convert image radargrams to internal format

    *Methods*
    * run - Execute the conversion
    """

    def run(self, raw_data):
        """Execute the conversion

        raw_data: image radargram
        """

        pass

class MarsisImgManager(ImgManager):
    """Convert Marsis image radargrams to internal format

    *Methods*
    * run - Execute the conversion
    """

    def run(self, raw_data):
        """Execute the conversion

        raw_data: image radargram
        """

        data = np.hsplit(np.rot90(np.asarray(raw_data), k=3),6)
        data.reverse()
        data1=[]
        data1.append(np.array(data[0:3]))
        data1.append(np.array(data[3:6]))
        return data1

class SharadImgManager(ImgManager):
    """Convert Sharad image radargrams to internal format

    *Methods*
    * run - Execute the conversion
    """

    def run(self, raw_data):
        """Execute the conversion

        raw_data: image radargram
        """

        d = np.rot90(np.asarray(raw_data), k=3)
        return [d[np.newaxis,:,:]]

###############################################################################
class DataFetcher(object):
    """Implement data feching from local or remote location

    *Methods*
    *fetch - Fetch the radargram data
    """

    def fetch(self, location, cache, filename):
        """Fetch the radargram data

        location: location of the radargram file
        cache: location to cache the radargram file to
        filename: name of the radargram file
        """

        pass

class DiskFetcher(DataFetcher):
    """Implement data feching from disk

    *Methods*
    *fetch - Fetch the radargram data
    """

    def fetch(self, location, cache, filename):
        """Fetch the radargram data

        location: directory of the radargram file
        cache: directory to cache the radargram file to
        filename: name of the radargram file
        """

        return im.open(os.path.join(location,filename))

class HttpFetcher(DiskFetcher):
    """Implement http data feching

    *Methods*
    *fetch - Fetch the radargram data
    """

    def fetch(self, location, cache, filename):
        """Fetch the radargram data

        location: base url of the radargram file
        cache: directory to cache the radargram file to
        filename: name of the radargram file
        """

        if not os.path.exists(cache):
            os.makedirs(cache)

        cache_location = os.path.join(cache,filename)
        if location[0:4]=='http':
            url = location+'/'+filename
        else:
            url = os.path.join(location,filename)

        if os.path.exists(cache_location) == False:
            try:
                (chaced, headers) = urlretrieve(url, cache_location)
            except IOError:
              pass

        return super(HttpFetcher, self).fetch(cache, cache, filename)

###############################################################################
class DataLocator(object):
    """
    """
    def __init__(self, base_dir, cache_dir, file_prefix, file_suffix, fetcher = None):
        """
        """
        self.base_dir = base_dir
        self.cache_dir = cache_dir
        self.file_prefix = file_prefix
        self.file_suffix = file_suffix

        self.fetcher = fetcher

    def set_fetcher(self, fetcher):
        """
        """
        self.fetcher = fetcher

    def get_raw_data(self, orbit):
        """
        """
        orbit_str = self.get_orbit_str(orbit)
        orbit_dir = self.get_orbit_dir(orbit_str)

        return self.fetcher.fetch(os.path.join(self.base_dir,orbit_dir),
                                  os.path.join(self.cache_dir,orbit_dir),
                                  self.file_prefix+orbit_str+self.file_suffix)

    def get_orbit_str(self, orbit):
        pass

    def get_orbit_dir(self, orbit):
        pass

class MarsisLocator(DataLocator):
    """
    """
    def get_orbit_str(self, orbit):
        """
        """
        orbit_str = str(orbit)
        if len(orbit_str) == 4:
            orbit_str = "0"+orbit_str

        return orbit_str

class MarsisRadarLocator(MarsisLocator):
    """
    """
    def get_orbit_dir(self, orbit):
        return "RDR"+str(orbit)[0:-1]+"X"

class MarsisSimLocator(MarsisLocator):
    """
    """
    def get_orbit_dir(self, orbit):
        return "SIM"


class SharadRadarLocator(DataLocator):
    """
    """
    def get_orbit_str(self, orbit):
        orbit_str = str(orbit)
        if len(orbit_str) == 6:
            orbit_str = "00"+orbit_str

        if len(orbit_str) == 7:
            orbit_str = "0"+orbit_str

        return orbit_str


    def get_orbit_dir(self, orbit):
        return "s_"+str(orbit)[0:-4]+"xx"



###############################################################################
class DataReader(object):
    """
    """
    def __init__(self, base_dir, cache_dir, file_prefix, file_suffix):
        """
        """
        self.base_dir = base_dir
        self.cache_dir = cache_dir
        self.file_prefix = file_prefix
        self.file_suffix = file_suffix

    def get_data(self, orbit):
        try:
            return self.data_man.run(self.locator.get_raw_data(orbit))
        except IOError:
            return None

    def get_v_scale(self, orbit):
        pass

class MarsisReader(DataReader):
    """
    """
    def __init__(self, base_dir, cache_dir, file_prefix, file_suffix):
        """
        """
        super(MarsisReader, self).__init__(base_dir, cache_dir, file_prefix, file_suffix)

        self.fetcher = HttpFetcher()
        self.data_man = MarsisImgManager()


class MarsisRadarReader(MarsisReader):
    """
    """
    def __init__(self, base_dir, cache_dir, file_prefix, file_suffix):
        """
        """
        super(MarsisRadarReader, self).__init__(base_dir, cache_dir, file_prefix, file_suffix)

        self.locator = MarsisRadarLocator(self.base_dir,
                                          self.cache_dir,
                                          self.file_prefix,
                                          self.file_suffix,
                                          fetcher = self.fetcher)

    def get_v_scale(self, orbit):
        return 350

class MarsisSimReader(MarsisReader):
    """
    """
    def __init__(self, base_dir, cache_dir, file_prefix, file_suffix):
        """
        """
        super(MarsisSimReader, self).__init__(base_dir, cache_dir, file_prefix, file_suffix)

        self.locator = MarsisSimLocator(self.base_dir,
                                        self.cache_dir,
                                        self.file_prefix,
                                        self.file_suffix,
                                        fetcher = self.fetcher)



class SharadRadarReader(DataReader):
    """
    """
    def __init__(self, base_dir, cache_dir, file_prefix, file_suffix):
        """
        """
        super(SharadRadarReader, self).__init__(base_dir, cache_dir, file_prefix, file_suffix)

        self.fetcher = HttpFetcher()
        self.data_man = SharadImgManager()

        self.locator = SharadRadarLocator(self.base_dir,
                                          self.cache_dir,
                                          self.file_prefix,
                                          self.file_suffix,
                                          fetcher = self.fetcher)

    def get_v_scale(self, orbit):
        return 135

class SharadSimReader(SharadRadarReader):
    def get_data(self, orbit):
        return None