# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotmaps.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PlotMaps(object):
    def setupUi(self, PlotMaps):
        PlotMaps.setObjectName("PlotMaps")
        PlotMaps.resize(811, 654)
        self.gridLayout = QtWidgets.QGridLayout(PlotMaps)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(PlotMaps)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(358, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.modelBox = QtWidgets.QComboBox(PlotMaps)
        self.modelBox.setMinimumSize(QtCore.QSize(260, 26))
        self.modelBox.setObjectName("modelBox")
        self.gridLayout.addWidget(self.modelBox, 0, 2, 1, 1)
        self.plotterBox = QtWidgets.QGroupBox(PlotMaps)
        self.plotterBox.setMinimumSize(QtCore.QSize(551, 311))
        self.plotterBox.setObjectName("plotterBox")
        self.gridLayout.addWidget(self.plotterBox, 1, 0, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(932, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 3)
        self.closeButton = QtWidgets.QPushButton(PlotMaps)
        self.closeButton.setMaximumSize(QtCore.QSize(110, 32))
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 2, 3, 1, 1)
        self.closeButton.raise_()
        self.plotterBox.raise_()

        self.retranslateUi(PlotMaps)
        QtCore.QMetaObject.connectSlotsByName(PlotMaps)

    def retranslateUi(self, PlotMaps):
        _translate = QtCore.QCoreApplication.translate
        PlotMaps.setWindowTitle(_translate("PlotMaps", "Plot maps"))
        self.label_4.setText(_translate("PlotMaps", "Select model"))
        self.plotterBox.setTitle(_translate("PlotMaps", "Selectivity map"))
        self.closeButton.setText(_translate("PlotMaps", "Close"))

