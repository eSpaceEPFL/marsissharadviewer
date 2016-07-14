# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

from gc import collect as gc_collect
from time import sleep

from numpy import inf as np_inf
from numpy import zeros as np_zeros
from numpy import ones as np_ones
from numpy import empty as np_empty
from numpy import rot90 as np_rot90
from numpy import array as np_array
from numpy import linspace as np_linspace
from numpy import interp as np_interp

from marsissharadviewer.pyqtgraphcore.Qt import  QtCore, QtGui

from marsissharadviewer.pyqtgraphcore import GraphicsLayout as pg_GraphicsLayout
from marsissharadviewer.pyqtgraphcore import TextItem as pg_TextItem
from marsissharadviewer.pyqtgraphcore import GridItem as pg_GridItem
from marsissharadviewer.pyqtgraphcore import LinearRegionItem as pg_LinearRegionItem
from marsissharadviewer.pyqtgraphcore import InfiniteLine as pg_InfiniteLine
from marsissharadviewer.pyqtgraphcore import LabelItem as pg_LabelItem
from marsissharadviewer.pyqtgraphcore import ImageItem as pg_ImageItem
from marsissharadviewer.pyqtgraphcore import makeRGBA as pg_makeRGBA
from marsissharadviewer.pyqtgraphcore import PolyLineROI as pg_PolyLineROI

from marsissharadviewer.pyqtgraphcore import opengl as gl

import look_up_tables as lut


class SinglePlot(pg_GraphicsLayout):
    """
    """
    def __init__(self,
                 parent=None,
                 images = [],
                 images_label = [],
                 q_rects = None,
                 label_text = "",
                 roi_movable = True,
                 lock_aspect = True,
                 x_label = 'x',
                 y_label = 'y',
                 x_unit = "",
                 y_unit = "",
                 v_offset = 0,
                 **kargs):
        super(SinglePlot, self).__init__(parent, **kargs)

        self.menu = None
        self.set_menu()
#        self.surf_line = None
#        self.sub_lines = []
        self.images = []

        self.label_text = label_text
        self.images_data = images

        if len(images_label) == 0:
            self.images_label = ["" for im in self.images_data]
        else:
            self.images_label = images_label

        if q_rects == None:
            self.q_rects = [None for im in self.images_data]
        else:
            self.q_rects = q_rects

        self.v_offset = v_offset

        self.label = pg_LabelItem(label_text, justify = "right") #adding label
        self.addItem(self.label, row=0, col=0)

        self.view_box = self.addViewBox(row=1, col=0, lockAspect=lock_aspect) #adding viewbox
        self.depth = DepthTool(self.view_box)

        self.position_label = PositionLabel(x_label = x_label,
                                            y_label = y_label,
                                            x_unit = x_unit,
                                            y_unit = y_unit) #adding position label
        self.position_label.setParentItem(self.label)

        self.grid = pg_GridItem() #adding grid
        self.view_box.addItem(self.grid)
#        self.view_box.setParent(self)
#        for image in images:
#            self._add_image(image)

        for ii in range(len(self.images_data)):
            self._add_image(self.images_data[ii],
                            label = self.images_label[ii],
                            q_rect = self.q_rects[ii])

        self.roi = pg_LinearRegionItem(movable=roi_movable) #adding roi highlight
        self.view_box.addItem(self.roi)
#        self.roi.setParent(self)

        self.v_mark = pg_InfiniteLine(angle=90, movable=True) #adding vertical marker
        self.view_box.addItem(self.v_mark, ignoreBounds=True)
        self.v_mark.sigPositionChanged.connect(self.upd_pos_label)

        self.h_mark = pg_InfiniteLine(angle=0, movable=True) #adding horizontal marker
        self.view_box.addItem(self.h_mark, ignoreBounds=True)
        self.h_mark.sigPositionChanged.connect(self.upd_pos_label)


    def getContextMenus(self, event):

        try:
            if self.depth.surf_line:
                self.surf_line_action.setEnabled(0)
            else:
                self.surf_line_action.setEnabled(1)
        except AttributeError:
            pass


        return self.menu

#    def raiseContextMenu(self, ev):
#        menu = self.getMenu()
#        if self.surf_line:
#            self.surf_line_action.setEnabled(0)
##        menu = self.scene().addParentContextMenus(self, menu, ev)
#        pos = ev.screenPos()
#        menu.popup(QtCore.QPoint(pos.x(), pos.y()))

    def set_menu(self):
        self.menu = QtGui.QMenu()
        self.menu.setTitle("Depth measurement")

        self.surf_line_action = QtGui.QAction("Add surface line", self.menu)
        self.surf_line_action.triggered.connect(self.add_surf_line)
        self.menu.addAction(self.surf_line_action)

        sub_line = QtGui.QAction("Add subsurface line", self.menu)
        sub_line.triggered.connect(self.add_sub_line)
        self.menu.addAction(sub_line)
        self.menu.sub_line = sub_line

    def add_surf_line(self):
        (x1,x2) = self.roi.getRegion()
        h = self.q_rects[0].top()+self.q_rects[0].height()/2.

        self.depth.add_surf_line([x1,x2],[h,h])

    def add_sub_line(self):
        (x1,x2) = self.roi.getRegion()
        h = self.q_rects[0].top()+self.q_rects[0].height()/2.

        self.depth.add_sub_line([x1,x2],[h,h])

    def set_label(self, label_text):
        self.label.setText(label_text)

    def set_roi(self, min_max, bounds = None):

        self.roi.setRegion(min_max)
        if bounds:
            self.roi.setBounds(bounds)

    def set_roi_bounds(self, bounds):
        self.roi.setBounds(bounds)

    def _add_image(self, img, label = "", q_rect = None):
        self.images.append(pg_ImageItem(img))
        self.images_label.append(label)

        if q_rect != None:
            self.images[-1].setRect(q_rect)

        if len(self.images) > 1:
            self.show_superposed(images_idx = [0,1])
#            self.images[-1].setCompositionMode(QtGui.QPainter.CompositionMode_Overlay)
        self.view_box.addItem(self.images[-1])


    def add_image(self, img, label = ""):

        self.view_box.removeItem(self.v_mark)
        self.view_box.removeItem(self.h_mark)
        self.view_box.removeItem(self.roi)

        self._add_image(img, label = label)

        self.view_box.addItem(self.v_mark, ignoreBounds=True)
        self.view_box.addItem(self.h_mark, ignoreBounds=True)
        self.view_box.addItem(self.roi)

        self.view_box.autoRange()

    def reset_images(self):
        for image in self.images:
            self.view_box.removeItem(image)

        self.images = []

    def _mark_connect(self, mark, cb):
        mark.sigPositionChanged.connect(cb)

    def h_mark_connect(self, cb):
        self._mark_connect(self.h_mark, cb)

    def v_mark_connect(self, cb):
        self._mark_connect(self.v_mark, cb)

    def roi_connect(self, cb):
        self.roi.sigRegionChangeFinished.connect(cb)

    def upd_pos_label(self):
        self.position_label.x = self.v_mark.value()
        self.position_label.y = self.h_mark.value()
        self.position_label.update()

    def upd_h_mark(self, a):
        self.h_mark.setValue(a.value())

    def upd_v_mark(self, a):
        self.v_mark.setValue(a.value())

    def upd_roi(self, a):
        self.roi.setRegion(a.getRegion())

    def set_x_link(self, to):
        self.view_box.setXLink(to.view_box)

    def set_y_link(self, to):
        self.view_box.setYLink(to.view_box)

    def set_xy_link(self, to):
        self.set_x_link(to)
        self.set_y_link(to)

    def set_h_mark_link(self, to):
        self.h_mark.sigPositionChanged.connect(to.upd_h_mark)
        to.h_mark.sigPositionChanged.connect(self.upd_h_mark)

    def set_v_mark_link(self, to):
        self.v_mark.sigPositionChanged.connect(to.upd_v_mark)
        to.v_mark.sigPositionChanged.connect(self.upd_v_mark)

    def set_marks_link(self, to):
        self.set_h_mark_link(to)
        self.set_v_mark_link(to)

    def set_roi_link(self, to):
        self.roi.sigRegionChanged.connect(to.upd_roi)
        to.roi.sigRegionChanged.connect(self.upd_roi)

    def set_full_link(self, to):
        self.set_xy_link(to)
        self.set_marks_link(to)
        self.set_roi_link(to)

    def show_superposed(self,
                        images_idx,
                        luts = [lut.RedAlphaLUT().get_lut(),
                                lut.GreenAlphaLUT().get_lut()],
                        comp_modes = [QtGui.QPainter.CompositionMode_Plus,
                                      QtGui.QPainter.CompositionMode_Plus]):

        self._set_all_visible(is_visible = False)

        if len(images_idx) == 2:
            for ii in images_idx:
                self.images[ii].setVisible(True)
                self.images[ii].setLookupTable(luts[ii])
                self.images[ii].setCompositionMode(comp_modes[ii])


    def show_single_image(self,
                         image_idx,
                         lut = lut.GrayAlphaLUT().get_lut(),
                         comp_mode = QtGui.QPainter.CompositionMode_Plus):

        self._set_all_visible(is_visible = False)

        self.images[image_idx].setVisible(True)
        self.images[image_idx].setLookupTable(lut)
        self.images[image_idx].setCompositionMode(comp_mode)

    def _set_all_visible(self, is_visible = True):

        for image in self.images:
            image.setVisible(is_visible)

    def get_v_offset(self):
        return self.v_offset

    def set_v_offset(self, offset):
        self.v_offset = offset
        for ii in range(len(self.images)):
            self.images[ii].setRect(QtCore.QRectF(self.q_rects[ii].x(),
                                                  self.q_rects[ii].y()+offset,
                                                  self.q_rects[ii].width(),
                                                  self.q_rects[ii].height()))

###############################################################################
###############################################################################
###############################################################################

class DepthTool(object):
    def __init__(self, vb):
        self.vb = vb

        self.surf_line = None
        self.sub_lines = []


    def add_surf_line(self, x, y):
        self.surf_line = pg_PolyLineROI([[x[0],y[0]], [x[1],y[1]]], closed=False, removable=True, pen = (0,9), movable = True)
        self.vb.addItem(self.surf_line)
        self.surf_line.sigRemoveRequested.connect(self.rm_surf_line)

    def rm_surf_line(self):
        self.surf_line.sigRemoveRequested.disconnect(self.rm_surf_line)
        self.vb.removeItem(self.surf_line)
#        self.surf_line.stateChanged()
        del self.surf_line
        self.surf_line = None

    def add_sub_line(self, x, y):
        self.sub_lines.append(SubLine([[x[0],y[0]], [x[1],y[1]]], self.sub_lines, closed=False, removable=True, vb = self.vb, pen = (3,9), movable = True))
        self.vb.addItem(self.sub_lines[-1])
        self.sub_lines[-1].sigRemoveRequested.connect(self.sub_lines[-1].remove)

    def measure(self):
        if self._check_extent():
            return -1

        self.i_sub = []
        self.depths = []
        self.i_surf = self._interp_line(self.surf_line)
        for line in self.sub_lines:
            self.i_sub.append(self._interp_line(line))
            self.depths.append(self._compute_depth(self.i_sub[-1]))

    def _compute_depth(self, line):
        x0 = -self.i_surf[0][0] + line[0][0]
#        xf = self.i_surf[0][-1] - line[0][-1]

        return (line[0], line[1]-self.i_surf[1][x0:x0+len(line[1])])

    def _check_extent(self):
        x0_surf = self.surf_line.getLocalHandlePositions()[0][1].x()
        xf_surf = self.surf_line.getLocalHandlePositions()[-1][1].x()

        for line in self.sub_lines:
            handles = line.getLocalHandlePositions()
            if handles[0][1].x() < x0_surf:
                return 1

            if handles[-1][1].x() > xf_surf:
                return 1

        return 0

    def _interp_line(self, line):
        handles = line.getLocalHandlePositions()
        x = []
        y = []
        for h in handles:
            x.append(h[1].x())
            y.append(h[1].y())

        xi = range(int(x[0]),int(x[-1])+1)
        yi = np_interp(np_array(xi), np_array(x), np_array(y))


        return (xi,yi)

class SubLine(pg_PolyLineROI):

    def __init__(self, positions, sub_list, closed=False, pos=None, vb = None, **args):
        super(SubLine, self).__init__(positions, closed=False, pos=None, **args)
        self.vb = vb
        self.list = sub_list

    def remove(self):
        self.sigRemoveRequested.disconnect(self.remove)
        self.vb.removeItem(self)
        self.list.remove(self)
        self = None

class PositionLabel(pg_TextItem):

    def __init__(self,
                 text="(x = 0.0 y = 0.0)",
                 is_visible = True,
                 color=(200, 200, 200),
                 html=None,
                 anchor=(0, 0),
                 border=None,
                 fill=None,
                 angle=0,
                 x_label = 'x',
                 y_label = 'y',
                 x_unit = "",
                 y_unit = ""):

        super(PositionLabel, self).__init__(text, color=color, html=html, anchor=anchor, border=border, fill=fill, angle=angle)
        self.x = 0.0
        self.y = 0.0

        self.x_label = x_label
        self.y_label = y_label

        self.x_unit = x_unit
        self.y_unit = y_unit

        if is_visible:
            self.set_visible()
        else:
            self.set_hidden()

    def set_x_label(self, x_label):
        self.x_label = x_label

    def set_y_label(self, y_label):
        self.y_label = y_label

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def visible_update(self):
        self.setText("(%s = %0.1f %s : %s = %0.1f %s)" % (self.x_label, self.x, self.x_unit, self.y_label, self.y, self.y_unit))

    def hidden_update(self):
        self.setText("")

    def set_visible(self):
        self.is_visible = True
        self.update = self.visible_update
        self.update()

    def set_hidden(self):
        self.is_visible = False
        self.update = self.hidden_update
        self.update()

###############################################################################
###############################################################################
class ThreeDPlot(gl.GLViewWidget):

    def __init__(self, parent = None):
        super(ThreeDPlot, self).__init__(parent)
        self.surfaces = []
        self.ref_surf = None
        self.opts['distance'] = 200

        self.set_offsets()
        self.set_k()

    def set_offsets(self, xoff=0, yoff=0, zoff=0):
        self.xoff = xoff
        self.yoff = yoff
        self.zoff = zoff

    def set_k(self, kx=1, ky=1, kz=1):
        self.kx = kx
        self.ky = ky
        self.kz = kz

    def add_surface(self, x, y, z, col_mat):

        renderer = (ThreeDImageRenderer(x,
                                      y,
                                      z,
                                      col_mat,
                                      self.xoff,
                                      self.yoff,
                                      self.zoff,
                                      self.kx,
                                      self.ky,
                                      self.kz))


        self.surfaces.append(renderer.get_object())
        self.addItem(self.surfaces[-1])

        return self.surfaces[-1]

    def add_reference_surface(self, xmin, xmax, ymin, ymax, image):
        cx = np_linspace(xmin/self.kx,xmax/self.kx,image.shape[1])
        cy = np_linspace(ymin/self.ky,ymax/self.ky,image.shape[0])
        cz = np_zeros((image.shape[1],image.shape[0]))


        ref_tex = pg_makeRGBA(np_rot90(image, k=3))[0]/255.
        self.ref_surf = gl.GLSurfacePlotItem(x=cx, y=cy, z=cz, colors = ref_tex, shader='balloon')
        self.ref_surf.translate(-self.xoff,-self.yoff,self.zoff)
        self.addItem(self.ref_surf)

        return self.ref_surf

    def set_grid(self):
        zgrid = gl.GLGridItem()
        self.addItem(zgrid)

    def move_surface_z(self, surface, dz):
        surface.translate(0,0,dz)

    def move_ref_surf_z(self, dz):
        self.move_surface_z(self.ref_surf, dz)

    def set_surface_visible(self, surface, visible):
        surface.setVisible(visible)

###############################################################################
class ThreeDRenderer(object):

    @classmethod
    def get_implementations(cls):
        """Return the subclasses
        """
        implementations = cls.__subclasses__() + [g for s in cls.__subclasses__() for g in s.get_implementations()]
        exec_impl = []
        for implementation in implementations:
            if implementation.is_exec:
                exec_impl.append(implementation)

        return exec_impl

    def __init__(self,
                 x,
                 y,
                 z,
                 color_matrix,
                 xoff = 0,
                 yoff = 0,
                 zoff = 0,
                 kx = 1,
                 ky = 1,
                 kz = 1,
                 threshold = np_inf):

        self.x = x
        self.y = y
        self.z = z
        self.col_mat = color_matrix

        self.xoff = xoff
        self.yoff = yoff
        self.zoff = zoff

        self.kx = kx
        self.ky = ky
        self.kz = kz
        self.threshold = threshold

        self.set_data()
        self.render()

    def set_data(self):
        pass

    def render(self):
        pass

    def get_object(self):
        return self.gl_obj

class ThreeDImageRenderer(ThreeDRenderer):

    name = "Image plot"
    is_exec = True

    def set_data(self):
        self.x_mat = np_zeros((self.col_mat.shape[1], self.col_mat.shape[0]))

        self.x_mat[:,:] = self.x
        self.tex = pg_makeRGBA(np_rot90(self.col_mat), levels= (50., 255.))[0]/255.
        self.tex[...,3] = self.tex[...,0]

    def render(self):
        self.gl_obj = gl.GLSurfacePlotItem(x=self.z/self.kz, y=self.y/self.ky, z=self.x_mat/self.kx, colors = self.tex)
        self.gl_obj.rotate(90, 0, 1, 0)
        self.gl_obj.translate(-self.xoff, -self.yoff, -self.zoff)


class ThreeDScatterRenderer(ThreeDRenderer):

    name = "Scatter plot"
    is_exec = True

    def set_data(self):
        data_len = self.col_mat.shape[0]*self.col_mat.shape[1]
        self.pos = np_empty((data_len, 3))
        self.size = np_ones((data_len))*.1
        self.color = np_empty((data_len, 4))

        jj = 0
        for ii in range(len(self.y)):
            for zz in range(len(self.z)):
                self.pos[jj,:] = np_array((self.x[ii]/self.kx,self.y[ii]/self.ky,zz/self.kz))
                self.color[jj,:] = self.col_mat[ii,zz]/255.
                jj = jj + 1


    def render(self):
        self.gl_obj = gl.GLScatterPlotItem(pos=self.pos, size=self.size, color=self.color, pxMode=False)
        self.gl_obj.translate(-self.xoff, -self.yoff, -self.zoff)


