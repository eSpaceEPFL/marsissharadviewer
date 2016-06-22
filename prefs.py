# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

from PyQt4.QtCore import QSettings
import radar_readers as rr

class RadarPrefs(object):
    def __init__(self):
        self.s = QSettings("./marsradqgis")


    def set_prefs(self):


        self.DISK_L2_DIR = {"MARSIS": self.s.value("MarsisDataDisk","/media/federico/fc_data/MARSIS_data/L2_Data_full/BROWSE/"),#"/media/federico/Backup/MARSIS/L2_Data/BROWSE/", #"/home/federico/Documents/iMars/MARSIS_data_L2/L2_Data/BROWSE/",
                       "SHARAD": self.s.value("SharadDataDisk","")}
        self.DISK_SIM_DIR = {"MARSIS": self.s.value("MarsisSimDisk","/media/federico/fc_data/MARSIS_data/"),#"/media/federico/Backup/MARSIS/", # "/home/federico/Documents/iMars/MARSIS_data_L2/L2_Data/BROWSE/",
                        "SHARAD": self.s.value("SharadSimDisk","")}

        self.HTTP_L2_DIR = {"MARSIS": self.s.value("MarsisDataHttp","http://127.0.0.1/MARSIS_L2/"),
                       "SHARAD": self.s.value("SharadDataHttp","http://pds-geosciences.wustl.edu/mro/mro-m-sharad-5-radargram-v1/mrosh_2001/browse/thm/")}
        self.HTTP_SIM_DIR = {"MARSIS": self.s.value("MarsisSimHttp","http://127.0.0.1/MARSIS_L2/"),
                        "SHARAD": self.s.value("SharadSimHttp","")}

        self.DATA_SOURCE = {"MARSIS": self.s.value("MarsisDataSource","DISK"),
                       "SHARAD": self.s.value("SharadDataSource","HTTP")}#DISK -> local dir; HTTP -> remote dir (http connection)

        self.SIM_SOURCE = {"MARSIS": self.s.value("MarsisSimSource","DISK"),
                       "SHARAD": self.s.value("SharadSimSource","HTTP")}#DISK -> local dir; HTTP -> remote dir (http connection)

        self.L2_PREFIX = {"MARSIS": "R_",
                     "SHARAD": "s_"}
        self.L2_SUFFIX = {"MARSIS": "_SS3_TRK_CMP_M.png",
                     "SHARAD": "_thm.jpg"}

        self.SIM_PREFIX = {"MARSIS": "E_",
                      "SHARAD": ""}
        self.SIM_SUFFIX = {"MARSIS": "_SS3_TRK_CMP_M_SIM.png",
                      "SHARAD": ""}

        self.L2_DIR = {}
        self.SIM_DIR = {}

        for source in self.DATA_SOURCE:
            if self.DATA_SOURCE[source] == 'DISK':
                self.L2_DIR[source] = self.DISK_L2_DIR[source] #DISK_L2_DIR -> local dir; HTTP_L2_DIR -> remote dir (http connection)

            if self.DATA_SOURCE[source] == 'HTTP':
                self.L2_DIR[source] = self.HTTP_L2_DIR[source] #DISK_L2_DIR -> local dir; HTTP_L2_DIR -> remote dir (http connection)


        for source in self.SIM_SOURCE:
            if self.SIM_SOURCE[source] == 'DISK':
                self.SIM_DIR[source] = self.DISK_SIM_DIR[source] #DISK_SIM_DIR -> local dir; HTTP_SIM_DIR -> remote dir (http connection)

            if self.SIM_SOURCE[source] == 'HTTP':
                self.SIM_DIR[source] = self.HTTP_SIM_DIR[source] #DISK_SIM_DIR -> local dir; HTTP_SIM_DIR -> remote dir (http connection)


        self.CHACHE_BASE_DIR = self.s.value("CacheDir","/home/federico/MarsQgisRadar/")

        self.RADAR_READER = {"MARSIS": rr.MarsisRadarReader(self.L2_DIR["MARSIS"], self.CHACHE_BASE_DIR, self.L2_PREFIX["MARSIS"], self.L2_SUFFIX["MARSIS"]),
                       "SHARAD": rr.SharadRadarReader(self.L2_DIR["SHARAD"], self.CHACHE_BASE_DIR, self.L2_PREFIX["SHARAD"], self.L2_SUFFIX["SHARAD"])}
        self.SIM_READER = {"MARSIS": rr.MarsisSimReader(self.SIM_DIR["MARSIS"], self.CHACHE_BASE_DIR, self.SIM_PREFIX["MARSIS"], self.SIM_SUFFIX["MARSIS"]),
                       "SHARAD": rr.SharadSimReader(self.L2_DIR["SHARAD"], self.CHACHE_BASE_DIR, self.L2_PREFIX["SHARAD"], self.L2_SUFFIX["SHARAD"])}

        self.ORBIT = {"MARSIS":"orbit",
                 "SHARAD":"orbit"}

        self.DEF_LUT = 'radara'

    def set_data_disk(self, key, location):
        self.DISK_L2_DIR[key] = location

    def set_data_http(self, key, location):
        self.HTTP_L2_DIR[key] = location

    def set_sim_disk(self, key, location):
        self.DISK_SIM_DIR[key] = location

    def set_sim_http(self, key, location):
        self.HTTP_SIM_DIR[key] = location

    def set_data_source(self, radar_key, source_key):
        pass