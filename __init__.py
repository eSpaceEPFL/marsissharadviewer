# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Marsis
                                 A QGIS plugin
 Utilities to work with MARSIS data
                             -------------------
        begin                : 2015-09-07
        copyright            : (C) 2015-2016 by EPFL-eSpace
        email                : federico.cantini@epfl.ch
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Marsis class from file Marsis.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .marsis_utils import Marsis
    return Marsis(iface)
