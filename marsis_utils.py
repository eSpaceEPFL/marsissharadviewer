# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import gc

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QObject, SIGNAL
from PyQt4.QtGui import QAction, QIcon, QMenu
# Initialize Qt resources from file resources.py
import os.path

from marsis_viewer_dialog import MarsisViewerDialog
from settings_dialog import SettingsDialog
from radar_3d import Radar3D

import prefs

class Marsis:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        #set preferences
        self.prefs = prefs.RadarPrefs()
        self.prefs.set_prefs()

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Marsis_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.iface = iface
        self.marsis_menu = None


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.marsis_menu = QMenu(QCoreApplication.translate("marsis", "MARSIS"))
        self.iface.mainWindow().menuBar().insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.marsis_menu)

        icon = QIcon(':/plugins/MarsisViewer/icon.png')
 #       icon = QIcon(':/plugins/Marsis/icon.png')
        self.marsis_viewer_action = QAction(icon, "Marsis viewer", self.iface.mainWindow())
        QObject.connect(self.marsis_viewer_action, SIGNAL("triggered()"), self.marsis_viewer)
        self.marsis_menu.addAction(self.marsis_viewer_action)

        self.polar_viewer_action = QAction(icon, "Polar viewer", self.iface.mainWindow())
        QObject.connect(self.marsis_viewer_action, SIGNAL("triggered()"), self.polar_viewer)
        self.marsis_menu.addAction(self.polar_viewer_action)

 #       icon = QIcon(':/plugins/Marsis/icon.png')
        self.radar_3d_action = QAction(icon, "Radar 3D", self.iface.mainWindow())
        QObject.connect(self.radar_3d_action, SIGNAL("triggered()"), self.radar_3d)
        self.marsis_menu.addAction(self.radar_3d_action)

#        icon = QIcon(os.path.dirname(__file__) + ":/plugins/Marsis/icon.png")
        self.track_fetch_action = QAction(icon, "Marsis tracks fetch", self.iface.mainWindow())
        QObject.connect(self.track_fetch_action, SIGNAL("triggered()"), self.track_fetch)
        self.marsis_menu.addAction(self.track_fetch_action)

#        icon = QIcon(os.path.dirname(__file__) + ":/plugins/Marsis/icon.png")
        self.radar_fetch_action = QAction(icon, "Marsis radargrams fetch", self.iface.mainWindow())
        QObject.connect(self.radar_fetch_action, SIGNAL("triggered()"), self.radar_fetch)
        self.marsis_menu.addAction(self.radar_fetch_action)

#        icon = QIcon(os.path.dirname(__file__) + ":/plugins/Marsis/icon.png")
        self.settings_action = QAction(icon, "Settings", self.iface.mainWindow())
        QObject.connect(self.settings_action, SIGNAL("triggered()"), self.settings)
        self.marsis_menu.addAction(self.settings_action)

        # Add toolbar button
#        self.iface.addToolBarIcon(self.marsis_viewer_action)

        self.toolbar = self.iface.addToolBar(u'MarsisViewer')
        self.toolbar.setObjectName(u'MarsisViewer')
        self.toolbar.addAction(self.marsis_viewer_action)


    def marsis_viewer(self):
        gc.collect()
        self.dialog = MarsisViewerDialog(self.iface, self.prefs, free_routine = self.marsis_free)
#        dialog.exec_()
        print "vai"

    def marsis_free(self):
        self.dialog = None
#        gc.collect()

    def polar_viewer(self):
        pass

    def radar_3d(self):
        Radar3D(self.iface)

    def track_fetch(self):
        pass

    def radar_fetch(self):
        pass

    def settings(self):
        self.set_dialog = SettingsDialog()

    def update_prefs(self):
        self.prefs.set_prefs()

    def unload(self):

        """Removes the plugin menu item and icon from QGIS GUI."""
        if self.marsis_menu != None:
            self.iface.mainWindow().menuBar().removeAction(self.marsis_menu.menuAction())
        else:
            self.iface.removePluginMenu("&mmqgis", self.marsis_viewer.menuAction())

        self.iface.removeToolBarIcon(self.marsis_viewer_action)