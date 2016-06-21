# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

from PyQt4.QtCore import QSettings
import radar_readers as rr

s = QSettings("./marsradqgis")

DISK_L2_DIR = {"MARSIS": s.value("MarsisDataDisk","/media/federico/fc_data/MARSIS_data/L2_Data_full/BROWSE/"),#"/media/federico/Backup/MARSIS/L2_Data/BROWSE/", #"/home/federico/Documents/iMars/MARSIS_data_L2/L2_Data/BROWSE/",
               "SHARAD": s.value("SharadDataDisk","")}
DISK_SIM_DIR = {"MARSIS": s.value("MarsisSimDisk","/media/federico/fc_data/MARSIS_data/"),#"/media/federico/Backup/MARSIS/", # "/home/federico/Documents/iMars/MARSIS_data_L2/L2_Data/BROWSE/",
                "SHARAD": s.value("SharadSimDisk","")}

HTTP_L2_DIR = {"MARSIS": s.value("MarsisDataHttp","http://127.0.0.1/MARSIS_L2/"),
               "SHARAD": s.value("SharadDataHttp","http://pds-geosciences.wustl.edu/mro/mro-m-sharad-5-radargram-v1/mrosh_2001/browse/thm/")}
HTTP_SIM_DIR = {"MARSIS": s.value("MarsisSimHttp","http://127.0.0.1/MARSIS_L2/"),
                "SHARAD": s.value("SharadSimHttp","")}

DATA_SOURCE = {"MARSIS": s.value("MarsisDataSource","DISK"),
               "SHARAD": s.value("SharadDataSource","HTTP")}#DISK -> local dir; HTTP -> remote dir (http connection)

L2_PREFIX = {"MARSIS": "R_",
             "SHARAD": "s_"}
L2_SUFFIX = {"MARSIS": "_SS3_TRK_CMP_M.png",
             "SHARAD": "_thm.jpg"}

SIM_PREFIX = {"MARSIS": "E_",
              "SHARAD": ""}
SIM_SUFFIX = {"MARSIS": "_SS3_TRK_CMP_M_SIM.png",
              "SHARAD": ""}

L2_DIR = {}
SIM_DIR = {}

for source in DATA_SOURCE:
    if DATA_SOURCE[source] == 'DISK':
        L2_DIR[source] = DISK_L2_DIR[source] #DISK_L2_DIR -> local dir; HTTP_L2_DIR -> remote dir (http connection)
        SIM_DIR[source] = DISK_SIM_DIR[source] #DISK_SIM_DIR -> local dir; HTTP_SIM_DIR -> remote dir (http connection)

    if DATA_SOURCE[source] == 'HTTP':
        L2_DIR[source] = HTTP_L2_DIR[source] #DISK_L2_DIR -> local dir; HTTP_L2_DIR -> remote dir (http connection)
        SIM_DIR[source] = HTTP_SIM_DIR[source] #DISK_SIM_DIR -> local dir; HTTP_SIM_DIR -> remote dir (http connection)



CHACHE_BASE_DIR = s.value("CacheDir","/home/federico/MarsQgisRadar/")

RADAR_READER = {"MARSIS": rr.MarsisRadarReader(L2_DIR["MARSIS"], CHACHE_BASE_DIR, L2_PREFIX["MARSIS"], L2_SUFFIX["MARSIS"]),
               "SHARAD": rr.SharadRadarReader(L2_DIR["SHARAD"], CHACHE_BASE_DIR, L2_PREFIX["SHARAD"], L2_SUFFIX["SHARAD"])}
SIM_READER = {"MARSIS": rr.MarsisSimReader(SIM_DIR["MARSIS"], CHACHE_BASE_DIR, SIM_PREFIX["MARSIS"], SIM_SUFFIX["MARSIS"]),
               "SHARAD": rr.SharadSimReader(L2_DIR["SHARAD"], CHACHE_BASE_DIR, L2_PREFIX["SHARAD"], L2_SUFFIX["SHARAD"])}

ORBIT = {"MARSIS":"orbit",
         "SHARAD":"orbit"}

DEF_LUT = 'radara'

