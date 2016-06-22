# -*- coding: utf-8 -*-
# Copyright (C) 2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import os

from PyQt4 import uic
from pyqtgraph.Qt import QtGui


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'settings.ui'))

class SettingsDialog(QtGui.QWidget, FORM_CLASS):

    def __init__(self, prefs, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.prefs = prefs
        self.setupUi(self)
        self.set_dialog()
        self.show()

        print dir(self.prefs)

    def set_dialog(self):
        #MARSIS
        self.lineMarsisDataDisk.setText(self.prefs.DISK_L2_DIR['MARSIS'])
        self.lineMarsisSimDisk.setText(self.prefs.DISK_SIM_DIR['MARSIS'])

        self.lineMarsisDataHttp.setText(self.prefs.HTTP_L2_DIR['MARSIS'])
        self.lineMarsisSimHttp.setText(self.prefs.HTTP_SIM_DIR['MARSIS'])

        if self.prefs.DATA_SOURCE['MARSIS'] == 'DISK':
            self.radioMarsisDataDisk.setChecked(True)

        if self.prefs.DATA_SOURCE['MARSIS'] == 'HTTP':
            self.radioMarsisDataHttp.setChecked(True)

        if self.prefs.SIM_SOURCE['MARSIS'] == 'DISK':
            self.radioMarsisSimDisk.setChecked(True)

        if self.prefs.SIM_SOURCE['MARSIS'] == 'HTTP':
            self.radioMarsisSimHttp.setChecked(True)


        #SHARAD
        self.lineSharadDataDisk.setText(self.prefs.DISK_L2_DIR['SHARAD'])
        self.lineSharadSimDisk.setText(self.prefs.DISK_SIM_DIR['SHARAD'])

        self.lineSharadDataHttp.setText(self.prefs.HTTP_L2_DIR['SHARAD'])
        self.lineSharadSimHttp.setText(self.prefs.HTTP_SIM_DIR['SHARAD'])

        if self.prefs.DATA_SOURCE['SHARAD'] == 'DISK':
            self.radioSharadDataDisk.setChecked(True)

        if self.prefs.DATA_SOURCE['SHARAD'] == 'HTTP':
            self.radioSharadDataHttp.setChecked(True)

        if self.prefs.SIM_SOURCE['SHARAD'] == 'DISK':
            self.radioSharadSimDisk.setChecked(True)

        if self.prefs.SIM_SOURCE['SHARAD'] == 'HTTP':
            self.radioSharadSimHttp.setChecked(True)

        #MISC
        self.lineCacheDir.setText(self.prefs.CHACHE_BASE_DIR)

    def accept(self):
        pass

    def reject(self):
        self.close()