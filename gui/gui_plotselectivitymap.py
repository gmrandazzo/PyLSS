# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotselectivitymap.ui'
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

class Ui_PlotSelectivityMap(object):
    def setupUi(self, PlotSelectivityMap):
        PlotSelectivityMap.setObjectName(_fromUtf8("PlotSelectivityMap"))
        PlotSelectivityMap.resize(811, 654)
        self.gridLayout = QtGui.QGridLayout(PlotSelectivityMap)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(PlotSelectivityMap)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(358, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.modelBox = QtGui.QComboBox(PlotSelectivityMap)
        self.modelBox.setMinimumSize(QtCore.QSize(260, 26))
        self.modelBox.setObjectName(_fromUtf8("modelBox"))
        self.gridLayout.addWidget(self.modelBox, 0, 2, 1, 1)
        self.plotterBox = QtGui.QGroupBox(PlotSelectivityMap)
        self.plotterBox.setMinimumSize(QtCore.QSize(551, 311))
        self.plotterBox.setObjectName(_fromUtf8("plotterBox"))
        self.gridLayout.addWidget(self.plotterBox, 1, 0, 1, 4)
        spacerItem1 = QtGui.QSpacerItem(932, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 3)
        self.closeButton = QtGui.QPushButton(PlotSelectivityMap)
        self.closeButton.setMaximumSize(QtCore.QSize(110, 32))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.gridLayout.addWidget(self.closeButton, 2, 3, 1, 1)
        self.closeButton.raise_()
        self.plotterBox.raise_()

        self.retranslateUi(PlotSelectivityMap)
        QtCore.QMetaObject.connectSlotsByName(PlotSelectivityMap)

    def retranslateUi(self, PlotSelectivityMap):
        PlotSelectivityMap.setWindowTitle(_translate("PlotSelectivityMap", "Selectivity map", None))
        self.label_4.setText(_translate("PlotSelectivityMap", "Select model", None))
        self.plotterBox.setTitle(_translate("PlotSelectivityMap", "Selectivity map", None))
        self.closeButton.setText(_translate("PlotSelectivityMap", "Close", None))

