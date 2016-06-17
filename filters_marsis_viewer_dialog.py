# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FiltersMarsisViewerDialog
                                 A QGIS plugin
 MARSIS radargram viewer
                             -------------------
        begin                : 2015-08-14
        git sha              : $Format:%H$
        copyright            : (C) 2015 by eSpace - EPFL
        email                : federico.cantini@epfl.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'filters_marsis_viewer_dialog_base.ui'))


class FiltersMarsisViewerDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, orbit, data, region, parent=None):
        """Constructor."""
        super(FiltersMarsisViewerDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.iface = iface
        self.orbit = orbit
        self.data = data
        self.region = region
        self.setupUi(self)
        self.run()

    def run(self):
        """Run method that performs all the real work"""
#############################################################
#        arr = np.ones((1024, 512), dtype=float)
#        arr += np.random.normal(size=(1024,512))
#############################################################

#        layer = self.iface.activeLayer()
#        orbits = {}
#        for feature in layer.selectedFeatures():
#            key = str(feature.attribute('orbitnumber'))
#            if orbits.has_key(key) == False:
#                orbits[key] = []
#            orbits[key].append((feature.attribute('point_id')))
#
#        r_read = rr.PngReader(orbits.keys()[0], base_dir = "/home/federico/Documents/iMars/MARSIS_data_L2/L2_Data/BROWSE/")
#
        self.set_active_layer(self.iface.activeLayer())
        self.set_orbit_num(self.orbit)
        self.set_data(self.data)
        self.set_region(self.region[0], self.region[1])
#        self.set_region(min(orbits[orbits.keys()[0]]), max(orbits[orbits.keys()[0]]))
        # show the dialog

    def set_data(self, data):
        self.radar_plot.set_data(data)

    def set_region(self, start, stop):
        self.radar_plot.set_region(start, stop)

    def set_orbit_num(self, on):
        self.radar_plot.set_orbit_num(on)

    def set_active_layer(self, layer):
        self.radar_plot.set_active_layer(layer)
