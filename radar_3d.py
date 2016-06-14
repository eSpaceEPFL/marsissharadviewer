# -*- coding: utf-8 -*-
# Copyright (C) 2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import csv

from get_feature_data import GetFeatureData

class Radar3D(GetFeatureData):
    def __init__(self, iface):
        self.iface = iface
        self.get_layers()
        self.get_selected_features()
        self.get_data()

        self.write_data()

    def write_data(self):
        fw = open('Desktop/test.csv', 'w')
        writerw  = csv.writer(fw)
        writerw.writerow(['orbit', 'x coord', 'y coord', 'z coord', 'data', 'sim'])

        for orbit in self.orbits.keys():
            f = open('Desktop/'+str(orbit)+'.csv', 'w')
            writer  = csv.writer(f)
            writer.writerow(['x coord', 'y coord', 'z coord', 'data', 'sim'])

            print orbit
#            print self.orbits[orbit]['data'][0][0][0,1]
            for point in self.orbits[orbit]['point_id']:
                for ii in range(self.orbits[orbit]['sim'][0][0].shape[1]):
                    if self.orbits[orbit]['data'][0][0][point,ii] > 100:
                        writer.writerow([self.orbits[orbit]['lon_dict'][point],
                                         self.orbits[orbit]['lat_dict'][point],
                                         -ii/10.,
                                         self.orbits[orbit]['data'][0][0][point,ii],
                                         self.orbits[orbit]['sim'][0][0][point,ii]])

                        writerw.writerow([orbit,
                                          self.orbits[orbit]['lon_dict'][point],
                                          self.orbits[orbit]['lat_dict'][point],
                                          -ii/10.,
                                         self.orbits[orbit]['data'][0][0][point,ii],
                                         self.orbits[orbit]['sim'][0][0][point,ii]])


            f.close()

        fw.close()