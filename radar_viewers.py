# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import os.path
from collections import OrderedDict
from time import sleep

from numpy import mean as np_mean
from numpy import zeros as np_zeros
#from numpy import array as np_array

import marsissharadviewer.pyqtgraphcore  as pg
from marsissharadviewer.pyqtgraphcore import opengl as gl
from OpenGL.GL import *

from marsissharadviewer.pyqtgraphcore.Qt import QtCore, QtGui
#QtGui.QApplication.setGraphicsSystem('raster')
from qgis.core import  QgsVectorLayer, QgsMapLayerRegistry, QgsField, QgsFeature, QgsVectorFileWriter
from qgis import utils
#from PyQt4.QtCore import QRectF
#from PyQt4.QtGui import QPushButton, QGridLayout
from PIL import Image as im

#import numpy as np

import look_up_tables as lut

#from filters_marsis_viewer_dialog import FiltersMarsisViewerDialog
from radar_plots import SinglePlot
from radar_plots import ThreeDPlot
from radar_plots import ThreeDImageRenderer

#import prefs

#import scipy.ndimage as ndi
import numpy as np

import time
class _RadarViewer(pg.LayoutWidget):

    def __init__(self, parent = None):
        super(_RadarViewer, self).__init__(parent)


        self.rad_gray_lut = lut.GrayLUT()

        self.rad_gray_alpha_lut = lut.GrayAlphaLUT()

        self.sim_gray_lut = lut.GrayLUT()

        self.rad_red_lut = lut.RedLUT()
        self.rad_red_alpha_lut = lut.RedAlphaLUT()

        self.sim_green_lut = lut.GreenLUT()
        self.sim_green_alpha_lut = lut.GreenAlphaLUT()

        self.sup_rad_gray_lut = lut.GrayAlphaLUT()
        self.sup_sim_gray_lut = lut.GrayAlphaLUT()

        self.sup_red_rad_gray_lut = lut.GrayAlphaLUT()
        self.sup_red_sim_red_lut = lut.RedLUT()

        self.glw = pg.GraphicsLayoutWidget()
        self.blw = pg.LayoutWidget()

        self.buttons = self.addWidget(self.blw, row=0, col=0)
        self.graphs = self.addWidget(self.glw, row=1, col=0)

        self.l2views = [self.show_radar_def, self.show_radar_def]
        self.add_buttons()

        self.plots = []
        self.reset()

    def set_prefs(self, prefs):
        self.prefs = prefs

    def add_buttons(self):
        self.buttons = {}
        self.buttons['radar'] = self._add_r_button("Rad", self.show_radar_def)
        self.buttons['radara'] = self._add_r_button("Rad (alpha)", self.show_radar_alpha_def)
        self.buttons['sim'] = self._add_r_button("Sim", self.show_sim_def)
        self.buttons['super'] = self._add_r_button("Rad+Sim", self.show_super_def)
        self.buttons['super_alpha'] = self._add_r_button("Rad+Sim (alpha)", self.show_super_alpha_def)
        self.buttons['super_diff'] = self._add_r_button("Rad+Sim (diff)", self.show_super_alpha_diff)
        self.buttons['super_red'] = self._add_r_button("Rad+Sim (gray/red)", self.show_super_gray_red)
        self.buttons['swap'] = self._add_button("Swap last two", self.swap_last_two)
#        self.buttons['lut'] = self._add_button("LUT", self.open_lut_widget)
        self.buttons['v_off'] = self._add_button("V offset", self.open_v_offset)

    def _add_button(self, label, cb):
        button = QtGui.QPushButton(label)
        button.clicked.connect(cb)
        self.blw.addWidget(button)

        return button

    def _add_r_button(self, label, cb):
        button = QtGui.QRadioButton(label)
        button.clicked.connect(cb)
        self.blw.addWidget(button)

        return button


    def addItem(self, item, row=None, col=None):
        self.glw.addItem(item, row=row, col=col)

    def reset(self):
        for plot in self.plots:
            plot.reset_images()

class RadarViewer(_RadarViewer):

    roi_movable = True
    lock_aspect = True

    def __init__(self, parent = None):
        super(RadarViewer, self).__init__(parent)
        self.name = 'Simple viewer'
        self.x_unit = ''
        self.y_unit = ''

        #self.glw = pg.GraphicsLayoutWidget()
    def set_plots(self, data_dict):
        self.upd_gis_selection = {}
        self.orbit_row = []
        self.orbit_idx = OrderedDict()
        ii = 0;
        for orbit in data_dict.keys():
            str_orbit = str(orbit)
            self.orbit_idx[str_orbit] = ii

            self.q_rect = self.get_q_rect(data_dict[orbit])

            ow = OrbitViewer(orbit,
                             data_dict[orbit],
                             q_rects = [self.q_rect, self.q_rect],
                             roi_movable = self.roi_movable,
                             lock_aspect = self.lock_aspect,
                             labels = 0,
                             x_unit = self.x_unit,
                             y_unit = self.y_unit,
                             prefs = self.prefs)

            self.orbit_row.append(ow)

            self.addItem(self.orbit_row[-1], row=ii, col=0)
            self.orbit_row[-1].set_roi(self.get_roi_range(data_dict[orbit]),
                                       self.get_roi_bounds(data_dict[orbit]))
            self.orbit_row[-1].set_full_link_int()

            self.upd_gis_selection[str_orbit] = UpdGisSelection(ow, str_orbit, data_dict[orbit].get_layer(), self.prefs)
            self.orbit_row[-1].plots[0].roi_connect(self.upd_gis_selection[str_orbit].run)

            self.buttons[self.prefs.DEF_LUT].click()

            ii = ii + 1

    def _show_single_image(self, image_idx, lut = lut.GrayAlphaLUT().get_lut(), comp_mode = QtGui.QPainter.CompositionMode_Plus):
        for orbit in self.orbit_row:
            orbit.show_single_image(image_idx, lut = lut, comp_mode = comp_mode)

    def show_superposed(self,
                        luts = [lut.RedLUT().get_lut(), lut.GreenLUT().get_lut()],
                        comp_modes = [QtGui.QPainter.CompositionMode_Plus, QtGui.QPainter.CompositionMode_Plus]):

        for orbit in self.orbit_row:
            orbit.show_superposed( luts = luts, comp_modes = comp_modes)

    def get_roi_bounds(self, orbit_dict):
        return None

    def get_roi_range(self, orbit_dict):
        return orbit_dict.get_range()

    def get_q_rect(self, orbit_dict):
    # If files are not available an exception is thrown here
    # Check if data is actually avaiable (probably higher in the hierarchy of call )
        return QtCore.QRectF(0, -orbit_dict.data[0].shape[2],orbit_dict.data[0].shape[1], orbit_dict.data[0].shape[2])

    def show_data(self, lut = lut.GrayLUT().get_lut(), comp_mode = QtGui.QPainter.CompositionMode_Plus):
        self._show_single_image(0, lut = lut, comp_mode = comp_mode)

    def show_sim(self, lut = lut.GrayLUT().get_lut(), comp_mode = QtGui.QPainter.CompositionMode_Plus):
        self._show_single_image(1, lut = lut, comp_mode = comp_mode)

    def show_radar_def(self):
        self.show_data(self.rad_gray_lut.get_lut())
        self.l2views_update(self.buttons['radar'].click)

    def show_radar_alpha_def(self):
        self.show_data(lut = self.rad_gray_alpha_lut.get_lut())
        self.l2views_update(self.buttons['radara'].click)

    def show_sim_def(self):
        self.show_sim(self.sim_gray_lut.get_lut())
        self.l2views_update(self.buttons['sim'].click)

    def show_super_def(self):
        self.show_superposed(luts = [self.rad_red_lut.get_lut(), self.sim_green_lut.get_lut()])
        self.l2views_update(self.buttons['super'].click)

    def show_super_alpha_def(self):
        self.show_superposed(luts = [self.rad_red_alpha_lut.get_lut(), self.sim_green_alpha_lut.get_lut()])
        self.l2views_update(self.buttons['super_alpha'].click)

    def show_super_alpha_diff(self):
        self.show_superposed(luts = [self.sup_rad_gray_lut.get_lut(), self.sup_sim_gray_lut.get_lut()],
                             comp_modes = [QtGui.QPainter.CompositionMode_Plus, QtGui.QPainter.CompositionMode_Difference])
        self.l2views_update(self.buttons['super_diff'].click)

    def show_super_gray_red(self):
        self.show_superposed(luts = [self.sup_red_rad_gray_lut.get_lut(), self.sup_red_sim_red_lut.get_lut()],
                             comp_modes = [QtGui.QPainter.CompositionMode_Plus, QtGui.QPainter.CompositionMode_Plus])
        self.l2views_update(self.buttons['super_red'].click)

    def swap_last_two(self):
        self.l2views[0]()

    def l2views_update(self, view):
        self.l2views.pop(0)
        self.l2views.append(view)

    def open_lut_widget(self):
        self.lut_ctl = RadarLutWidget(images = [self.plots[0].images[0], self.plots[1].images[0]])
        self.lut_ctl.show()

    def get_v_offset(self, orbit):
        pass

    def set_v_offset_data(self, orbit, offset):
        self.orbit_row[self.orbit_idx[orbit]].set_v_offset_data(offset)

    def set_v_offset_sim(self, orbit, offset):
        self.orbit_row[self.orbit_idx[orbit]].set_v_offset_sim(offset)

    def open_v_offset(self):
        self.v_offset_widg = VOffsetWidget(self)
        self.v_offset_widg.show()

    def set_roi_range(self, orbit):
        pass

    def revert_roi_range(self, orbit):
        pass

class SyncRadarViewer(RadarViewer):

    roi_movable = False
    lock_aspect = False

    def __init__(self, parent = None):
        super(SyncRadarViewer, self).__init__(parent)
        self.name = 'Sync viewer'
        self.x_unit = ' lat'
        self.y_unit = ' muSec'

    def set_plots(self, data_dict):
        super(SyncRadarViewer, self).set_plots(data_dict)

        for ii in range(1, len(self.orbit_row)):
            self.orbit_row[ii].set_full_link_ext(self.orbit_row[ii-1])
            self.orbit_row[ii].set_pos_label(-1)

    def get_roi_bounds(self, orbit_dict):
        return None

    def get_roi_range(self, orbit_dict):

        return (orbit_dict.lat_0(), orbit_dict.lat_f())

    def get_q_rect(self, orbit_dict):

        step = (orbit_dict.lat_f()-orbit_dict.lat_0())/(orbit_dict.get_range()[-1]-orbit_dict.get_range()[0])
        lat_0 = orbit_dict.lat_0() + step*(-orbit_dict.get_range()[0])
        lat_f = orbit_dict.lat_0() + step*(orbit_dict.data[0].shape[1]-orbit_dict.get_range()[0])

        return QtCore.QRectF(lat_0,-orbit_dict.get_v_scale(), lat_f-lat_0, orbit_dict.get_v_scale())

class CreateDepthLayer(object):

    def __init__(self, orbit, band, saving_dir):
        self.saving_dir = saving_dir
        self.orbit = orbit
        self.band = band

    def run(self, surf_sel, sub_sel, i_surf, i_sub, depths):
        warning_flag = 0

        # create layer
        layer_name = self.orbit.get_instrument()+'_'+self.orbit.get_id()+'_'+str(self.band)+'_depth'
        vl = QgsVectorLayer("Point", layer_name, "memory")
        pr = vl.dataProvider()

        # changes are only possible when editing the layer
        vl.startEditing()
        # add fields
        pr.addAttributes([QgsField("orbit", QtCore.QVariant.Int),
                          QgsField("point_id", QtCore.QVariant.Int),
                          QgsField("band", QtCore.QVariant.Int),
                          QgsField("surf_px", QtCore.QVariant.Double),
                          QgsField("surf_t", QtCore.QVariant.Double),
                          QgsField("surf_sel_x", QtCore.QVariant.Double),
                          QgsField("surf_sel_y", QtCore.QVariant.Double)
                        ])

        x_list = []
        i_surf_d = dict(zip(i_surf[0],i_surf[1]))
        i_sub_d = []
        depths_d = []
        for ii in range(len(depths)):
            i_sub_d.append(dict(zip(i_sub[ii][0],i_sub[ii][1])))
            depths_d.append(dict(zip(depths[ii][0],depths[ii][1])))
            pr.addAttributes([QgsField("sub_"+str(ii)+"_px", QtCore.QVariant.Double),
                              QgsField("sub_"+str(ii)+"_t", QtCore.QVariant.Double),
                              QgsField("sub_"+str(ii)+"_sel_x", QtCore.QVariant.Double),
                              QgsField("sub_"+str(ii)+"_sel_y", QtCore.QVariant.Double),
                              QgsField("depth_"+str(ii)+"_px", QtCore.QVariant.Double),
                              QgsField("depth_"+str(ii)+"_t", QtCore.QVariant.Double)])

#            x_list = x_list+depths[ii][0]

        x_list = i_surf[0]
        x_list = list(set(x_list))
        x_list.sort()

        for xx in x_list:
            surf, sub =  self._find_sel(xx, surf_sel, sub_sel)

            attr_list = [self.orbit.get_id(), xx, self.band, float(i_surf_d[xx]), self.orbit.px2t(float(i_surf_d[xx])), surf[0], surf[1]]
            feat = self.orbit.get_feature(xx)

            if not (feat == -1):
                for ii in range(len(depths)):
                    if i_sub_d[ii].has_key(xx):
                        attr_list = attr_list+[float(i_sub_d[ii][xx]),
                                               self.orbit.px2t(float(i_sub_d[ii][xx])),
                                               sub[ii][0],
                                               sub[ii][1],
                                               float(depths_d[ii][xx]),
                                               self.orbit.px2t(float(depths_d[ii][xx]))
                                               ]
                    else:
                        attr_list = attr_list+[None]*6

                new_feat = QgsFeature()
                new_feat.setGeometry(feat.geometry())
                new_feat.setAttributes(attr_list)

                pr.addFeatures([new_feat])

            else:
                warning_flag = 1

        if warning_flag:
            QtGui.QMessageBox.warning(None, "Warning", "Some surface point is outside the map available features")

        # commit to stop editing the layer
        vl.commitChanges()

        # update layer's extent when new features have been added
        # because change of extent in provider is not propagated to the layer
        vl.updateExtents()

        # add layer to the legend
        QgsMapLayerRegistry.instance().addMapLayer(vl)
        file_name = os.path.join(self.saving_dir, layer_name + '.sqlite')

        QgsVectorFileWriter.writeAsVectorFormat(vl, file_name, "utf-8", None, "SQLite")

#        pass

    def _find_sel(self, xx, surf_sel, sub_sel):

        surf = [None, None]
        sub = []
        for ii in range(len(sub_sel)):
            sub.append([None,None])

        # surface line
        for ii in range(len(surf_sel[0])):
            if int(surf_sel[0][ii]) == int(xx):
                surf[0] = surf_sel[0][ii]
                surf[1] = surf_sel[1][ii]

        #subsurface lines
        for jj in range(len(sub_sel)):
            for ii in range(len(sub_sel[jj][0])):
                if int(sub_sel[jj][0][ii]) == int(xx):
                    sub[jj][0] = sub_sel[jj][0][ii]
                    sub[jj][1] = sub_sel[jj][1][ii]

        return surf, sub


class UpdGisSelection():

    def __init__(self, orbit_viewer, orbit_number, layer, prefs):
        self.orbit_viewer = orbit_viewer
        self.orbit_number = orbit_number
        self.layer = layer
        self.features_ids = []
        self.features_ids_dict = {}
        self.fetch_feat_ids = 1
        self.prefs = prefs
#        self.run_filter = run_filter

    def run(self, a):

        point_ids = self.orbit_viewer.orbit_dict.get_map_avail_ids()
        self.orbit_viewer.set_roi_bounds([min( point_ids), max( point_ids)])
        feat_list = self.orbit_viewer.orbit_dict.get_map_selected_feats(int(round(a.getRegion()[0])),int(round(a.getRegion()[1])))
        self.layer.deselect(self.orbit_viewer.orbit_dict.get_map_avail_feats())
        self.layer.select(feat_list)

class RadarLutWidget(pg.LayoutWidget):

    def __init__(self, images = None, parent = None):
        super(RadarLutWidget, self).__init__(parent)

        self.glw = pg.GraphicsLayoutWidget()
        self.blw = pg.LayoutWidget()

        self.buttons = self.addWidget(self.blw, row=0, col=0)
        self.graphs = self.addWidget(self.glw, row=1, col=0)

        self.add_buttons()

        self.v = pg.HistogramLUTItem(images[0])
        self.w = pg.HistogramLUTItem(images[1])
        self.addItem(self.v, row = 1, col = 0)
        self.addItem(self.w, row = 1, col = 1)

    def add_buttons(self):
        self.buttons = {}
#        self.buttons['close'] = self._add_button("Close", self.close)

    def _add_button(self, label, cb):
        button = QtGui.QPushButton(label)
        button.clicked.connect(cb)
        self.blw.addWidget(button)

        return button

    def _add_r_button(self, label, cb):
        button = QtGui.QRadioButton(label)
        button.clicked.connect(cb)
        self.blw.addWidget(button)

        return button

    def addItem(self, item, row=None, col=None):
        self.glw.addItem(item, row=row, col=col)


class OrbitViewer(pg.GraphicsLayout):

    def __init__(self,
                 orbit,
                 orbit_dict,
                 q_rects = None,
                 roi_movable = False,
                 lock_aspect = True,
                 parent = None,
                 labels = 1,
                 x_label = 'x',
                 y_label = 'y',
                 x_unit = "",
                 y_unit = "",
                 v_offset = (0,0),
                 prefs = None):

        super(OrbitViewer, self).__init__(parent)

        self.plots = []
        data_f = []
        sim_f = []
        self.v_offset = v_offset
        self.v_offset_data = self.v_offset[0]
        self.v_offset_sim = self.v_offset[1]
        self.orbit_label = orbit_dict.get_instrument() + " - Orbit "+str(orbit)
        self.x_unit = x_unit
        self.y_unit = y_unit
        self.orbit_dict=orbit_dict
        self.prefs = prefs

        if orbit_dict.data:
            for band in orbit_dict.data:
                data_f.append(np_mean(band,0))

        else:
            for band in orbit_dict.sim:
                data_f.append(np_zeros(band.shape[1:]))


        if orbit_dict.sim:
            for band in orbit_dict.sim:
                sim_f.append(np_mean(band,0))

        else:
            for band in orbit_dict.data:
                sim_f.append(np_zeros(band.shape[1:]))

        ii = 0
        for band in orbit_dict.data:
            depth_cb = CreateDepthLayer(self.orbit_dict, ii, self.prefs.CHACHE_BASE_DIR)
            self.plots.append(SinglePlot(images = [data_f[ii], sim_f[ii]],
                                         images_label = ["data", "sim"],
                                         label_text = self.orbit_label+" Frequency band "+str(ii+1),
                                         q_rects = q_rects,
                                         roi_movable = roi_movable,
                                         lock_aspect = lock_aspect,
                                         x_label = x_label,
                                         y_label = y_label,
                                         x_unit = x_unit,
                                         y_unit = y_unit,
                                         depth_cb = depth_cb.run))

            self.addItem(self.plots[-1], row=0, col=(ii))

            ii = ii + 1

        self.set_pos_label(0)

    def set_roi(self, roi_range, roi_bounds = None):
        for plot in self.plots:
            plot.set_roi(roi_range, roi_bounds)


    def set_roi_bounds(self, roi_bounds):
        for plot in self.plots:
            plot.set_roi_bounds(roi_bounds)

    def _set_link_int(self, link_methods):
        n = len(link_methods) - 1
        for ii in range(n):
            link_methods[ii+1](self.plots[ii])

    def set_x_link_int(self):
        self._set_link_int([plot.set_x_link for plot in self.plots])

    def set_y_link_int(self):
        self._set_link_int([plot.set_y_link for plot in self.plots])

    def set_xy_link_int(self):
        self._set_link_int([plot.set_xy_link for plot in self.plots])
#        self.set_x_link_int()
#        self.set_y_link_int()

    def set_h_mark_link_int(self):
        self._set_link_int([plot.set_h_mark_link for plot in self.plots])

    def set_v_mark_link_int(self):
        self._set_link_int([plot.set_v_mark_link for plot in self.plots])

    def set_marks_link_int(self):
        self._set_link_int([plot.set_marks_link for plot in self.plots])

    def set_roi_link_int(self):
        self._set_link_int([plot.set_roi_link for plot in self.plots])

    def set_full_link_int(self):
        self._set_link_int([plot.set_full_link for plot in self.plots])

    def set_x_link_ext(self, to):
        self.plots[0].set_x_link(to.plots[0])

    def set_y_link_ext(self, to):
        self.plots[0].set_y_link(to.plots[0])

    def set_xy_link_ext(self, to):
        self.plots[0].set_xy_link(to.plots[0])

    def set_v_mark_link_ext(self, to):
        self.plots[0].set_v_mark_link(to.plots[0])

    def set_h_mark_link_ext(self, to):
        self.plots[0].set_h_mark_link(to.plots[0])

    def set_roi_link_ext(self, to):
        self.plots[0].set_roi_link(to.plots[0])

    def set_full_link_ext(self, to):
        self.plots[0].set_full_link(to.plots[0])

    def set_pos_label(self, lab_flag):
        if lab_flag != 1:
            for plot in self.plots[lab_flag + 1:]:
                plot.position_label.set_hidden()

    def show_single_image(self, image_idx, lut = lut.GrayAlphaLUT().get_lut(), comp_mode = QtGui.QPainter.CompositionMode_Plus):
        for plot in self.plots:
            plot.show_single_image(image_idx, lut = lut, comp_mode = comp_mode)


    def show_superposed(self, luts = [lut.RedLUT().get_lut(), lut.GreenLUT().get_lut()],
                              comp_modes = [QtGui.QPainter.CompositionMode_Plus, QtGui.QPainter.CompositionMode_Plus]):

        for plot in self.plots:
            plot.show_superposed([0, 1], luts = luts, comp_modes = comp_modes)

    def get_v_offset(self):
        return self.v_offset

#    def set_v_offset(self, offset):
#        self.v_offset = offset
#        for plot in self.plots:
#            plot.set_v_offset(offset)

    def set_v_offset_data(self, offset):
        self.v_offset_data = offset
        for plot in self.plots:
            plot.set_v_offset_data(offset)

    def set_v_offset_sim(self, offset):
        self.v_offset_sim = offset
        for plot in self.plots:
            plot.set_v_offset_sim(offset)

class VOffsetWidget(pg.LayoutWidget):

    def __init__(self, viewer, parent = None):
        super(VOffsetWidget, self).__init__(parent = parent)

        self.setWindowTitle(viewer.name)
        self.v_off_action_data = []
        self.v_off_action_sim = []
        ii = 0
        for orbit in viewer.orbit_idx:
            self.addWidget(QtGui.QLabel(viewer.orbit_row[viewer.orbit_idx[str(orbit)]].orbit_label), row = ii, col = 0)
            ii = ii+1

            self.addWidget(QtGui.QLabel("Data"), row = ii, col = 0)
            self.addWidget(QtGui.QLabel("Simulation"), row = ii, col = 1)
            ii = ii+1

            self.v_off_action_data.append(VOffsetActionData(viewer, str(orbit)))
            self.v_off_action_sim.append(VOffsetActionSim(viewer, str(orbit)))

            data_offset, sim_offset = viewer.orbit_row[viewer.orbit_idx[str(orbit)]].get_v_offset()

            spin = pg.SpinBox(value=data_offset,
                              step=1, bounds=[None, None],
                              suffix=viewer.orbit_row[viewer.orbit_idx[str(orbit)]].y_unit)
            spin.sigValueChanged.connect(self.v_off_action_data[-1].spin_changed)
            spin.sigValueChanging.connect(self.v_off_action_data[-1].spin_changing)
            self.addWidget(spin, row = ii, col = 0)

            spin_sim = pg.SpinBox(value=sim_offset,
                              step=1, bounds=[None, None],
                              suffix=viewer.orbit_row[viewer.orbit_idx[str(orbit)]].y_unit)
            spin_sim.sigValueChanged.connect(self.v_off_action_sim[-1].spin_changed)
            spin_sim.sigValueChanging.connect(self.v_off_action_sim[-1].spin_changing)
            self.addWidget(spin_sim, row = ii, col = 1)
            ii = ii+1

###############################################################################
class VOffsetAction():

    def __init__(self, viewer, orbit ):
        self.viewer = viewer
        self.orbit = orbit

    def run(self, offset):
        pass

    def spin_changed(self, sb):
        self.run(sb.value())

    def spin_changing(self, sb, value):
        self.run(sb.value())

class VOffsetActionData(VOffsetAction):

    def run(self, offset):
        self.viewer.set_v_offset_data(self.orbit, offset)

class VOffsetActionSim(VOffsetAction):

    def run(self, offset):
        self.viewer.set_v_offset_sim(self.orbit, offset)

###############################################################################

class ThreeDViewer(QtGui.QWidget):

    def __init__(self):
        super(ThreeDViewer, self).__init__()

        self.buttons_widg = pg.LayoutWidget()
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        self.plot = ThreeDPlot()

        self.layout.addWidget(self.plot, stretch = 1)
        self.layout.addWidget(self.buttons_widg, stretch = 0, alignment = QtCore.Qt.AlignRight)

        self.orbit_surf_dict = {}
        self.add_buttons()

    def set_prefs(self, prefs):
        self.prefs = prefs

    def add_buttons(self):
        self.buttons = {}
        self.buttons['ctrl'] = self._add_button("Open controller", self.open_controller)

    def _add_button(self, label, cb):
        button = QtGui.QPushButton(label)
        button.clicked.connect(cb)
        self.buttons_widg.addWidget(button)

        return button

    def open_controller(self):
        self.ctrl_widg = ThreeDCtrlWidget(self)
        self.ctrl_widg.show()

    def set_plots(self, data_dict):

#        self.controller = ThreeDController()
#        self.controller.show()
        self.data_dict = data_dict
        utils.iface.mapCanvas().saveAsImage(os.path.join(self.prefs.CHACHE_BASE_DIR,'canvas.png'))
        self.canvas = np.asarray(im.open(os.path.join(self.prefs.CHACHE_BASE_DIR,'canvas.png')))

        self.set_k(data_dict)

        xMax = utils.iface.mapCanvas().extent().xMaximum()
        xMin = utils.iface.mapCanvas().extent().xMinimum()
        yMax = utils.iface.mapCanvas().extent().yMaximum()
        yMin = utils.iface.mapCanvas().extent().yMinimum()

        ref_gl_obj = self.plot.add_reference_surface(xMin, xMax, yMin, yMax, self.canvas)
        self.reference_surf = ThreeDDataSurf(ref_gl_obj, self.plot, 0)

        self.xoff,self.yoff = self.get_xy_offs(data_dict)

        for orbit in data_dict.keys():
            self.orbit_surf_dict[orbit] = {}
            self.orbit_surf_dict[orbit]['data'] = []
            for band in data_dict[orbit].data:
                data = np_mean(band[:,data_dict[orbit].get_range()[0]:data_dict[orbit].get_range()[1]+1,:],0)
                y = np.array(data_dict[orbit].get_proj_y_list())
                x = np.array(data_dict[orbit].get_proj_x_list())
                z = np.linspace(0, data_dict[orbit].get_v_scale(), data.shape[1])
                gl_obj = self.plot.add_surface(x,y,z/10., data)
                self.orbit_surf_dict[orbit]['data'].append(ThreeDDataSurf(gl_obj, self.plot, 0))

#            if data_dict[orbit].has_key('sim'):
            if data_dict[orbit].sim:
                self.orbit_surf_dict[orbit]['sim'] = []
                for band in data_dict[orbit].sim:
                    data = np_mean(band[:,data_dict[orbit].get_range()[0]:data_dict[orbit].get_range()[1]+1,:],0)
                    y = np.array(data_dict[orbit].get_proj_y_list())
                    x = np.array(data_dict[orbit].get_proj_x_list())
                    z = np.linspace(0, data_dict[orbit].get_v_scale(), data.shape[1])
                    gl_obj = self.plot.add_surface(x,y,z/10., data)
                    self.orbit_surf_dict[orbit]['sim'].append(ThreeDDataSurf(gl_obj, self.plot, 0))


    def set_k(self, data_dict):
    # Here place check if something was selected - output an error
    # indicating that nothing reasonable was selected
    # Here plug in crashes if started from an empty project.
        if np.abs(data_dict[data_dict.keys()[0]].get_proj_y_list()[0])>1000:
            self.plot.set_k( kx=100000., ky=100000., kz=1.)
        else:
            self.plot.set_k( kx=1., ky=1., kz=1.)



    def get_xy_offs(self, data_dict):
        for orbit in data_dict.keys():
            xm = []
            ym = []

            ym.append(np.mean(data_dict[orbit].get_proj_y_list()))
            xm.append(np.mean(data_dict[orbit].get_proj_x_list()))

        return (np.mean(xm), np.mean(ym))


class GridItem(gl.GLGridItem):
    """
    **Bases:** :class:`GLGraphicsItem <pyqtgraph.opengl.GLGraphicsItem>`

    Displays a wire-grame grid.
    """

    def __init__(self, size=None, color=None, antialias=True, glOptions='translucent'):
        super(GridItem, self).__init__(size = size, color=color,antialias = antialias,glOptions=glOptions)

    def paint(self):
        self.setupGLState()

        if self.antialias:
            glEnable(GL_LINE_SMOOTH)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);

        glBegin( GL_LINES )

        x,y,z = self.size()
        glColor4f(1, 1, 0, 1)
        for x in range(-10, 11):
            glVertex3f(x, -10, 0)
            glVertex3f(x,  10, 0)
        for y in range(-10, 11):
            glVertex3f(-10, y, 0)
            glVertex3f( 10, y, 0)

        glEnd()


class ThreeDDataSurf(object):

    def __init__(self,
                 gl_obj = None,
                 plot = None,
                 zoff0 = None):

        self.gl_obj = gl_obj
        self.plot = plot
        self.zoff0 = zoff0

        self.zoff = zoff0

    def set_gl_obj(gl_obj):
        self.gl_obj = gl_obj

    def set_plot(plot):
        self.plot = plot

    def set_zoff0(zoff0):
        self.zoff0 = zoff0

    def set_zoff(self, zoff):
        self.plot.move_surface_z(self.gl_obj, zoff-self.zoff)
        self.zoff = zoff
    def get_zoff(self):
        return self.zoff

    def set_visible(self, visible):
        self.gl_obj.setVisible(visible)

    def is_visible(self):
        return self.gl_obj.visible()

class ThreeDCtrlWidget(pg.LayoutWidget):

    def __init__(self, viewer, parent = None):
        super(ThreeDCtrlWidget, self).__init__(parent = parent)

        self.setWindowTitle('3D view ctrl')

        self.tw = pg.TreeWidget()
        self.tw.setColumnCount(3)
        self.tw.setHeaderLabels(['','Visible','Offset'])

        map_it =  pg.TreeWidgetItem(['Map'])

        self.tw.addTopLevelItem(map_it)
        buttonm = QtGui.QCheckBox()
        buttonm.setChecked(viewer.reference_surf.is_visible())

        self.map_surf_actions = SurfActions(viewer.reference_surf)

        buttonm.stateChanged.connect(self.map_surf_actions.check_box_changed)
        self.tw.setItemWidget(map_it,1,buttonm)

        spinm = pg.SpinBox(value=viewer.reference_surf.get_zoff())
        spinm.sigValueChanged.connect(self.map_surf_actions.spin_changed)
        spinm.sigValueChanging.connect(self.map_surf_actions.spin_changing)

        self.tw.setItemWidget(map_it,2,spinm)

        orb_it = pg.TreeWidgetItem(['Orbits'])
        self.tw.addTopLevelItem(orb_it)
        buttono = QtGui.QCheckBox()
        self.tw.setItemWidget(orb_it,1,buttono)
        dialo = QtGui.QDial()
        dialo.setMaximumSize(31,31)
        dialo.setWrapping(1)
        dialo_spins_list = []
        orbito_list = []
        self.tw.setItemWidget(orb_it,2,dialo)

        self.set_boxes_action = []
        self.orb_boxes_action = []

        i={}
        self.surf_actions = []
        for orbit in viewer.orbit_surf_dict.keys():
           i[orbit] = pg.TreeWidgetItem([viewer.data_dict[orbit].get_instrument()+" "+orbit])
           self.tw.addTopLevelItem(i[orbit])
           button_orb = QtGui.QCheckBox()
           orbito_list.append(button_orb)
           self.tw.setItemWidget(i[orbit],1,button_orb)
           orb_boxes_list = []

           for dataset in viewer.orbit_surf_dict[orbit].keys():
               data_it = pg.TreeWidgetItem([dataset])
               i[orbit].addChild(data_it)


               button_set = QtGui.QCheckBox()
               orb_boxes_list.append(button_set)
               self.tw.setItemWidget(data_it,1,button_set)
               set_boxes_list = []

#               spin = pg.SpinBox()
#               dial = QtGui.QDial()
#               dial.setMaximumSize(31,31)
#               self.tw.setItemWidget(data_it,2,dial)

               band_i = 1
               for band in viewer.orbit_surf_dict[orbit][dataset]:
                   band_it= pg.TreeWidgetItem(['Band '+str(band_i)])
                   data_it.addChild(band_it)
                   band_i = band_i+1
                   button = QtGui.QCheckBox()
                   button.setChecked(band.is_visible())
                   self.surf_actions.append(SurfActions(band))
                   button.stateChanged.connect(self.surf_actions[-1].check_box_changed)
                   self.tw.setItemWidget(band_it,1,button)
                   set_boxes_list.append(button)

                   spin = pg.SpinBox(value=band.get_zoff())
                   spin.sigValueChanged.connect(self.surf_actions[-1].spin_changed)
                   spin.sigValueChanging.connect(self.surf_actions[-1].spin_changing)
                   dialo_spins_list.append(spin)

                   self.tw.setItemWidget(band_it,2,spin)


               self.set_boxes_action.append(MultiBoxAction(set_boxes_list))
               button_set.stateChanged.connect(self.set_boxes_action[-1].check_box_changed)

           self.orb_boxes_action.append(MultiBoxAction(orb_boxes_list))
           button_orb.stateChanged.connect(self.orb_boxes_action[-1].check_box_changed)


        self.orbito_action = MultiBoxAction(orbito_list)
        buttono.stateChanged.connect(self.orbito_action.check_box_changed)

        self.dialo_actions = DialActions(dialo, dialo_spins_list)
        dialo.valueChanged.connect(self.dialo_actions.dial_changed)
        dialo.sliderPressed.connect(self.dialo_actions.dial_pressed)

        self.addWidget(self.tw)



class SurfActions():

    def __init__(self, data_surf):
        self.data_surf = data_surf

    def check_box_changed(self, cb):
        self.data_surf.gl_obj.setVisible(cb)

    def run(self, zoff):
        self.data_surf.set_zoff(zoff)

    def spin_changed(self, sb):
        self.run(sb.value())

    def spin_changing(self, sb, value):
        self.run(sb.value())

class MultiBoxAction():

    def __init__(self, boxes_list):
        self.boxes_list = boxes_list

    def check_box_changed(self, cb):
        for box in self.boxes_list:
            box.setChecked(cb)

class DialActions():

    def __init__(self, dial, spins_list):
        self.dial = dial
        self.spins_list = spins_list
        self.v0 = self.dial.value()

    def dial_changed(self, d):
        delta = d-self.v0
        for spin in self.spins_list:
            spin.setValue(spin.value()+delta)

        self.v0 = self.dial.value()

    def dial_pressed(self):
        self.v0 = self.dial.value()








