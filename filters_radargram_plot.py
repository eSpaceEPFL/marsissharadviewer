# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from PyQt4.QtCore import QRectF
import qgis.core


import numpy as np

class FiltersRadargramPlot(pg.GraphicsLayoutWidget):

    def __init__(self, parent = None):
#############################################################
        arr = np.zeros((1024, 512), dtype=float)
#############################################################
        super(FiltersRadargramPlot, self).__init__(parent)

        self.text = ['F1 -1',
                'F1 0',
                'F1 +1',
                'F2 -1',
                'F2 0',
                'F2 +1']

        self.w = []
        self.label = []
        self.v = []
        self.g = []
        self.img = []
        self.vLine = []
        self.hLine = []
        self.region = []
        self.orbit_number = ""
        self.active_layer = None
        self.region_changed_flag = 0

        for ii in range(6):
            self.label.append(None)
            self.v.append(None)
            self.g.append(None)
            self.img.append(None)
            self.vLine.append(None)
            self.hLine.append(None)
            self.region.append(None)

        self.pos_label = pg.LabelItem(justify="left")
        self.addItem(self.pos_label)
        self.pos_label.setPos(0,0)


        self.w.append(self.addLayout(row=0, col=0))
        self.w.append(self.addLayout(row=1, col=0))
        self.w.append(self.addLayout(row=2, col=0))
        self.w.append(self.addLayout(row=0, col=1))
        self.w.append(self.addLayout(row=1, col=1))
        self.w.append(self.addLayout(row=2, col=1))


        for ii in range(6):
            self.label[ii] = self.w[ii].addLabel(self.text[ii], row=0, col=0)
            self.v[ii] = self.w[ii].addViewBox(row=1, col=0, lockAspect=True)
            self.g[ii] = pg.GridItem()
            self.v[ii].addItem(self.g[ii])
            self.img[ii] = pg.ImageItem(arr)
            self.v[ii].addItem(self.img[ii])
            self.img[ii].setRect(QRectF(0,-512, arr.shape[0], arr.shape[1]))
            self.region[ii] = pg.LinearRegionItem(movable=False)
            self.v[ii].addItem(self.region[ii])

            self.vLine[ii] = pg.InfiniteLine(angle=90, movable=True)
            self.hLine[ii] = pg.InfiniteLine(angle=0, movable=True)
            self.v[ii].addItem(self.vLine[ii], ignoreBounds=True)
            self.v[ii].addItem(self.hLine[ii], ignoreBounds=True)

            self.vLine[ii].sigPositionChanged.connect(self.v_line_moved)
            self.hLine[ii].sigPositionChanged.connect(self.h_line_moved)

            self.region[ii].sigRegionChanged.connect(self.region_changed)

        self.region[0].sigRegionChangeFinished.connect(self.upd_gis_selection)

        for ii in range(6):
            for jj in range(ii+1,6):
                self.v[ii].setXLink(self.v[jj])
                self.v[ii].setYLink(self.v[jj])

        self.upd_pos_label()
        self.set_orbit_num("")


    def v_line_moved(self,a):
        for ii in range(6):
            self.vLine[ii].setValue(a.value())
            self.upd_pos_label()

    def h_line_moved(self,a):
        for ii in range(6):
            self.hLine[ii].setValue(a.value())
            self.upd_pos_label()

    def upd_pos_label(self):
        self.pos_label.setText("Orbit: %s (x=%0.1f y=%0.1f)" % (str(self.orbit_number), self.vLine[0].value(), self.hLine[0].value()))


    def set_data(self, data):
        for ii in range(6):
            self.img[ii].setImage(data[ii])
            self.set_region(100,400)

    def set_region(self, start, stop):

        for ii in range(6):
            self.region[ii].sigRegionChanged.disconnect(self.region_changed)

        self.region[0].sigRegionChangeFinished.disconnect(self.upd_gis_selection)

        for ii in range(6):
            self.region[ii].setRegion([start, stop])

        for ii in range(6):
            self.region[ii].sigRegionChanged.connect(self.region_changed)

        self.region[0].sigRegionChangeFinished.connect(self.upd_gis_selection)

    def set_orbit_num(self, on):
        self.orbit_number = on
        self.upd_pos_label()

    def region_changed(self, a):
        for ii in range(6):
            self.region[ii].setRegion(a.getRegion())

    def upd_gis_selection(self, a):
        qstring = u'"orbitnumber" = '+  str(self.orbit_number) #+ ' AND "point_id" > ' + str(a.getRegion()[0]) + ' AND "point_id" < '+ str(a.getRegion()[1])
        req0=qgis.core.QgsFeatureRequest().setFilterExpression(qstring)

        qstring = qstring + ' AND "point_id" > ' + str(a.getRegion()[0]) + ' AND "point_id" < '+ str(a.getRegion()[1])
#        req=qgis.core.QgsFeatureRequest().setFilterExpression(qstring)
#
#        fit=self.active_layer.getFeatures(req0)
#        self.active_layer.deselect([ f.id() for f in fit ])
#
#        fit=self.active_layer.getFeatures(req)
#        self.active_layer.select([ f.id() for f in fit ])
#        print self.active_layer
#        print a.getRegion()[0]

    def set_active_layer(self, layer):
        self.active_layer = layer

