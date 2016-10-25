# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotmaps.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PlotMaps(object):
    def setupUi(self, PlotMaps):
        PlotMaps.setObjectName(_fromUtf8("PlotMaps"))
        PlotMaps.resize(811, 654)
        self.gridLayout = QtGui.QGridLayout(PlotMaps)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(PlotMaps)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(358, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.modelBox = QtGui.QComboBox(PlotMaps)
        self.modelBox.setMinimumSize(QtCore.QSize(260, 26))
        self.modelBox.setObjectName(_fromUtf8("modelBox"))
        self.gridLayout.addWidget(self.modelBox, 0, 2, 1, 1)
        self.plotterBox = QtGui.QGroupBox(PlotMaps)
        self.plotterBox.setMinimumSize(QtCore.QSize(551, 311))
        self.plotterBox.setObjectName(_fromUtf8("plotterBox"))
        self.gridLayout.addWidget(self.plotterBox, 1, 0, 1, 4)
        spacerItem1 = QtGui.QSpacerItem(932, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 3)
        self.closeButton = QtGui.QPushButton(PlotMaps)
        self.closeButton.setMaximumSize(QtCore.QSize(110, 32))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.gridLayout.addWidget(self.closeButton, 2, 3, 1, 1)
        self.closeButton.raise_()
        self.plotterBox.raise_()

        self.retranslateUi(PlotMaps)
        QtCore.QMetaObject.connectSlotsByName(PlotMaps)

    def retranslateUi(self, PlotMaps):
        PlotMaps.setWindowTitle(_translate("PlotMaps", "Plot maps", None))
        self.label_4.setText(_translate("PlotMaps", "Select model", None))
        self.plotterBox.setTitle(_translate("PlotMaps", "Selectivity map", None))
        self.closeButton.setText(_translate("PlotMaps", "Close", None))

