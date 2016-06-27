# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import os
import gc
#import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4 import uic
#from PyQt4.QtCore import QThread

#from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
#from PyQt4.QtGui import QAction, QIcon, QTreeWidgetItem

#import radar_readers as rr
#import numpy as np
#import prefs
#import time
from get_feature_data import GetFeatureData
#from qgis.core import QgsFeatureRequest

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'marsis_viewer_dialog_base.ui'))

class MarsisViewerDialog(QtGui.QWidget, FORM_CLASS, GetFeatureData):
    """Implement the MARSIS/SHARAD viewer

    *Methods*
    * __init__ - Inizialize the viewer
    * run - Run methods that performs all the real work
    * set_prefs - Set a reference for the plug in preferences
    * show_viewer - Show the viewers
    * set_up_view - Retrieve data
    * set_viewers - Set the viewers
    * get_layer_lat - UNUSED
    * reset - Reset the viewers
    * connect_roi - UNUSED
    * closeEvent - Properly close the viewer
    """

    def __init__(self, iface, prefs, free_routine=None, parent=None):
        """Inizialize the viewer

        iface: QGIS interface
        prefs: Instance of preference (prefs) class
        free_routine: function to call to allow garbage collector to release memory
        parent:
        """
        super(MarsisViewerDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.free_routine = free_routine
        self.iface = iface
        self.prefs = prefs

        self.setupUi(self)

#        self.radar2d.iface = iface

        self.run()


    def run(self):
        """Run method that performs all the real work
        """

#        self._dialog = WaitDialog(parent = self)
#        self._dialog.show()
# ATTEMPT TO ADD THREADS
#        self.process = ThreadProcessing()
#        self.td.start()
#        self.process.set_to_run(self.set_up_view)
#        self.process.finished.connect(self.show_viewer)
#        self.process.start()
#        self._dialog.close()
#######################
        self.set_prefs()
        self.set_up_view()
        self.show_viewer()

    def set_prefs(self):
        """Set a reference for the plug in preferences
        """

        self.radar2d.set_prefs(self.prefs)
        self.sync2d.set_prefs(self.prefs)
        self.threed.set_prefs(self.prefs)


    def show_viewer(self):
        """Show the viewers
        """

#        self._dialog.close()
        self.show()

    def set_up_view(self):
        """Retrieve data
        """

        self.reset()
        self.get_layers()
        self.get_selected_features()
        self.get_data()
        self.set_viewers()

    def set_viewers(self):
        """Set the viewers
        """

        self.radar2d.set_plots(self.orbits)
        self.sync2d.set_plots(self.orbits)
        self.threed.set_plots(self.orbits)

    def get_layer_lat(self):
        pass

    def reset(self):
        """Reset the viewers
        """

        self.gfd_reset()
        self.radar2d.reset()
        self.sync2d.reset()

#    def add_radargram(self, fulldata, data, orbit, region, lat, layer):
##        self.radar2d.add_radargram(fulldata, data, orbit, region, layer)
#        self.sync2d.add_radargram(data, orbit, region, lat)

    def connect_roi(self, orbit, lat):
        self.radar2d.region[str(orbit)][0].sigRegionChanged.connect()

    def closeEvent(self, event):
        """Properly close the viewer
        """

        self.reset()
        self.radar2d.close()
        self.sync2d.close()
        self.threed.close()
        gc.collect()
        if self.free_routine:
            self.free_routine()

class WaitDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        super(WaitDialog, self).__init__(parent)
        self.resize(100, 100)
        l=QtGui.QVBoxLayout(self)
        l.addWidget(QtGui.QLabel("Loading data...", self))
        l.addWidget(QtGui.QProgressBar(self, minimum=0, maximum=0))

class ThreadProcessing(QtCore.QThread):

    def set_to_run(self, to_run):
        self.to_run = to_run

    def run(self):
        self.to_run()
        self.finished.emit()
