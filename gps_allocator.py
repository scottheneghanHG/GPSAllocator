# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GPSAllocator
                                 A QGIS plugin
 This plugin allocates GPS point positions to nearby linear features
                              -------------------
        begin                : 2017-07-22
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Scott Heneghan
        email                : scott.heneghan@gmail.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from gps_allocator_dialog import GPSAllocatorDialog
import os.path
import os
from qgis.core import *
import qgis.utils


class GPSAllocator:
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
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GPSAllocator_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GPSAllocator')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'GPSAllocator')
        self.toolbar.setObjectName(u'GPSAllocator')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GPSAllocator', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = GPSAllocatorDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/GPSAllocator/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'GPS Allocator'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&GPSAllocator'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # this code will populate the combo box with all

        # vector layer from the Table of Content

        self.dlg.layerListCombo.clear()
        self.dlg.filePath.clear()

        layers = self.iface.legendInterface().layers()
        layer_list = []
        for layer in layers:
            layerType = layer.type()
            if layerType == QgsMapLayer.VectorLayer:
                layer_list.append(layer.name())
        self.dlg.layerListCombo.addItems(layer_list)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # substitute with your code.
            # delete selected feature from layer chosen by user

            selectedLayerIndex = self.dlg.layerListCombo.currentIndex()
            #filePathFilled = self.dlg.filePath.currentIndex()
            filePathFilled = self.dlg.filePath.toPlainText()
            selectedLayer = layers[selectedLayerIndex]
            # selFeatures = selectedLayer.selectedFeatures()
            # ids = [f.id() for f in selFeatures]
            # selectedLayer.startEditing()
            # for fid in ids:
            #     selectedLayer.deleteFeature(fid)
            #     selectedLayer.commitChanges()
            #
            # mc = self.iface.mapCanvas()
            # mc.refresh()

            gpxFiles = []
            for filename in os.listdir(filePathFilled):
                if filename.endswith(".gpx"):
                    gpxFiles.append(filename)
            print(gpxFiles)

            # layer = qgis.utils.iface.addVectorLayer(filePathFilled, "GPS Layer", "ogr")
            # if not layer:
            #     print
            #     "Layer failed to load!"

            # pick out the parts of the gpx file we want
            #loadGPXdata()

            #determine their spatial extent

            # calculate the time interval of the GPS data

            # perform overpass query

            # Separate overpass results by intersection and write them to a Spatialite table

            # Compute time-on-shard and output line datasets and results based on user input summary stats

def loadGPXdata():
    uri = "path/to/gpx/file.gpx?type=track"
    vlayer = QgsVectorLayer(uri, "layer name you like", "gpx")