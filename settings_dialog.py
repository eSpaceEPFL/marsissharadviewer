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
        try: 
           self.lineSharadDataDisk.setText(self.prefs.DISK_L2_DIR['SHARAD'])
        except TypeError: 
        	print "Opps! Type Error" 
           
        try:
        	self.lineSharadSimDisk.setText(self.prefs.DISK_SIM_DIR['SHARAD'])
        except TypeError:
        	print "Opps! Type Error" 
        	
        try:
        	self.lineSharadDataHttp.setText(self.prefs.HTTP_L2_DIR['SHARAD'])
        except TypeError:
        	print "Opps! Type Error" 
        
        try:
        	self.lineSharadSimHttp.setText(self.prefs.HTTP_SIM_DIR['SHARAD'])
        except TypeError:
        	print "Opps! Type Error" 
        	
        	
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

    def upd_prefs(self):

        self.prefs.set_marsis_data_disk(self.lineMarsisDataDisk.text())
        self.prefs.set_marsis_data_http(self.lineMarsisDataHttp.text())
        self.prefs.set_marsis_sim_disk(self.lineMarsisSimDisk.text())
        self.prefs.set_marsis_sim_http(self.lineMarsisSimHttp.text())
        self.prefs.set_sharad_data_disk(self.lineSharadDataDisk.text())
        self.prefs.set_sharad_data_http(self.lineSharadDataHttp.text())
        self.prefs.set_sharad_sim_disk(self.lineSharadSimDisk.text())
        self.prefs.set_sharad_sim_http(self.lineSharadSimHttp.text())

        self.prefs.set_cache_dir(self.lineCacheDir.text())

        if self.radioMarsisDataDisk.isChecked():
            self.prefs.set_marsis_data_source('DISK')

        if self.radioMarsisDataHttp.isChecked():
            self.prefs.set_marsis_data_source('HTTP')


        if self.radioMarsisSimDisk.isChecked():
            self.prefs.set_marsis_sim_source('DISK')

        if self.radioMarsisSimHttp.isChecked():
            self.prefs.set_marsis_sim_source('HTTP')


        if self.radioSharadDataDisk.isChecked():
            self.prefs.set_sharad_data_source('DISK')

        if self.radioSharadDataHttp.isChecked():
            self.prefs.set_sharad_data_source('HTTP')


        if self.radioSharadSimDisk.isChecked():
            self.prefs.set_sharad_sim_source('DISK')

        if self.radioSharadSimHttp.isChecked():
            self.prefs.set_sharad_sim_source('HTTP')


        self.prefs.set_prefs()
        self.set_dialog()

    def toolMarsisDataClicked(self):
       dirname = QtGui.QFileDialog.getExistingDirectory(self, 'Select MARSIS data dir', self.lineMarsisDataDisk.text())
       if dirname:
           self.lineMarsisDataDisk.setText(os.path.normpath(dirname))

    def toolMarsisSimClicked(self):
       dirname = QtGui.QFileDialog.getExistingDirectory(self, 'Select MARSIS simulations dir', self.lineMarsisSimDisk.text())
       if dirname:
           self.lineMarsisSimDisk.setText(os.path.normpath(dirname))

    def toolSharadDataClicked(self):
       dirname = QtGui.QFileDialog.getExistingDirectory(self, 'Select SHARAD data dir', self.lineSharadDataDisk.text())
       if dirname:
           self.lineSharadDataDisk.setText(os.path.normpath(dirname))

    def toolSharadSimClicked(self):
       dirname = QtGui.QFileDialog.getExistingDirectory(self, 'Select SHARAD simulations dir', self.lineSharadSimDisk.text())
       if dirname:
           self.lineSharadSimDisk.setText(os.path.normpath(dirname))

    def toolCacheClicked(self):
       dirname = QtGui.QFileDialog.getExistingDirectory(self, 'Select cache dir', self.lineCacheDir.text())
       if dirname:
           self.lineCacheDir.setText(os.path.normpath(dirname))

    def accept(self):
        self.upd_prefs()
        self.close()

    def reject(self):
        self.close()