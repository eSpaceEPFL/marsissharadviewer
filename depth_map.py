# -*- coding: utf-8 -*-
# Copyright (C) 2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Maintainer: Federico Cantini <federico.cantini@epfl.ch>

import os.path

from marsissharadviewer.pyqtgraphcore.Qt import QtCore, QtGui
from qgis.core import  QgsVectorLayer, QgsMapLayerRegistry, QgsField, QgsFeature, QgsVectorFileWriter, QgsProject
from qgis import utils


class DepthMap(object):

    def __init__(self, iface):
        self.layers = iface.legendInterface().selectedLayers()

        self._run(iface)

    def _run(self, iface):
        self._get_n_surfs()

        # create layer
        layer_name = 'depth_map'
        vl = QgsVectorLayer("Point", layer_name, "memory")
        pr = vl.dataProvider()

        # changes are only possible when editing the layer
        vl.startEditing()
        # add fields
        pr.addAttributes([QgsField("instrument", QtCore.QVariant.String),
                          QgsField("orbit", QtCore.QVariant.Int),
                          QgsField("point_id", QtCore.QVariant.Int),
                          QgsField("band", QtCore.QVariant.Int),
                          QgsField("n_surf", QtCore.QVariant.Int)
                        ])

        for ii in range(self.n_surfs):
            pr.addAttributes([QgsField("depth_"+str(ii), QtCore.QVariant.Double)])


        sim_surf = 0
        for layer in self.layers:
            instrument = self._get_instrument(layer)
            for feature in layer.getFeatures():
                attr_list = [instrument,
                             feature.attribute('orbit'),
                             feature.attribute('point_id'),
                             feature.attribute('band')]

                sub_surf = []
                add_feat = 0
                for ii in range(self.n_surfs):
                    field_name = "depth_"+str(ii)+"_t"
                    if feature.fieldNameIndex(field_name) > 0:
                        attribute = feature.attributes()[feature.fieldNameIndex(field_name)]
                        if isinstance(attribute, float):
                            add_feat = 1
                            sub_surf.append(-attribute)

                sub_surf.sort(reverse=True)

                l_sub_surf = len(sub_surf)
                if l_sub_surf > sim_surf:
                    sim_surf = l_sub_surf

                attr_list.append(l_sub_surf)
                attr_list.extend(sub_surf)

                if add_feat:
                    new_feat = QgsFeature()
                    new_feat.setGeometry(feature.geometry())
                    new_feat.setAttributes(attr_list)

                    pr.addFeatures([new_feat])


        # commit to stop editing the layer
        vl.commitChanges()

        # update layer's extent when new features have been added
        # because change of extent in provider is not propagated to the layer
        vl.updateExtents()

        # add layer to the legend
#        QgsMapLayerRegistry.instance().addMapLayer(vl)
        path = QgsProject.instance().readPath("./")
        file_name = os.path.join(path, 'depth.sqlite')
        fname = QtGui.QFileDialog().getSaveFileName(iface.mainWindow(), 'Map file',  file_name, '*.sqlite')

        QgsVectorFileWriter.writeAsVectorFormat(vl, fname, "utf-8", None, "SQLite")
        iface.addVectorLayer(fname, fname.split('/')[-1][0:-len('.sqlite')], "ogr")

#        for layer in self.layers:
#            sub_surf_n = (layer.fields().count()-7)/6
#            print layer.name()+": "+str(sub_surf_n)

    def _get_n_surfs(self):

        l_surfs = []
        for layer in self.layers:
            l_surfs.append((layer.fields().count()-7)/6)

        self.n_surfs = max(l_surfs)


    def _get_instrument(self, layer):
        if ((layer.name().find('SHARAD') > -1) or (layer.name().find('sharad') > -1)):
            return 'SHARAD'

        if ((layer.name().find('MARSIS') > -1) or (layer.name().find('marsis') > -1)):
            return 'MARSIS'


