# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import numpy as np
from pyqtgraph import ColorMap as pg_ColorMap

class LUT(object):

    color = np.array([[0,0,0,255],[0,0,0,255]], dtype=np.ubyte)
    color_mode = pg_ColorMap.RGB

    def __init__(self, pos = np.array([0.0,255.0]), inst_color = None, inst_color_mode = None):

        if inst_color:
            self.inst_color = inst_color
        else:
            self.inst_color = self.color

        if inst_color_mode:
            self.inst_color_mode = inst_color_mode
        else:
            self.inst_color_mode = self.color_mode

        self.pos = pos

        self.lut = pg_ColorMap(self.pos, self.inst_color, self.inst_color_mode).getLookupTable(0.0, 255.0, 256, mode = 'byte')


    def get_lut(self):
        return self.lut


    @classmethod
    def get_implementations(cls):
        """Return the subclasses
        """
        implementations = cls.__subclasses__() + [g for s in cls.__subclasses__() for g in s.get_implementations()]
        impl = []
        for implementation in implementations:
            impl.append(implementation)

        return impl

class GrayAlphaLUT(LUT):

    color = np.array([[0,0,0,0],[255,255,255,255]], dtype=np.ubyte)
    color_mode = pg_ColorMap.RGB

class RedAlphaLUT(LUT):

    color = np.array([[0,0,0,0],[255,0,0,255]], dtype=np.ubyte)
    color_mode = pg_ColorMap.RGB

class GreenAlphaLUT(LUT):

    color = np.array([[0,0,0,0],[0,255,0,255]], dtype=np.ubyte)
    color_mode = pg_ColorMap.RGB

class BlueAlphaLUT(LUT):

    color = np.array([[0,0,0,0],[0,0,255,255]], dtype=np.ubyte)
    color_mode = pg_ColorMap.RGB

class GrayLUT(LUT):

    color = np.array([[0,0,0,255],[255,255,255,255]], dtype=np.ubyte)
    color_mode = pg_ColorMap.RGB

class RedLUT(LUT):

    color = np.array([[0,0,0,255],[255,0,0,255]], dtype=np.ubyte)
    color_mode = pg_ColorMap.RGB

class GreenLUT(LUT):

    color = np.array([[0,0,0,255],[0,255,0,255]], dtype=np.ubyte)
    color_mode = pg_ColorMap.RGB

class BlueUT(LUT):

    color = np.array([[0,0,0,255],[0,0,255,255]], dtype=np.ubyte)
    color_mode = pg_ColorMap.RGB
