# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'computebestgradient.ui'
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

class Ui_ComputeBestGradient(object):
    def setupUi(self, ComputeBestGradient):
        ComputeBestGradient.setObjectName(_fromUtf8("ComputeBestGradient"))
        ComputeBestGradient.resize(576, 697)
        self.gridLayout_2 = QtGui.QGridLayout(ComputeBestGradient)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_4 = QtGui.QLabel(ComputeBestGradient)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.modelBox = QtGui.QComboBox(ComputeBestGradient)
        self.modelBox.setObjectName(_fromUtf8("modelBox"))
        self.horizontalLayout.addWidget(self.modelBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(ComputeBestGradient)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.radioButton = QtGui.QRadioButton(ComputeBestGradient)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.verticalLayout_2.addWidget(self.radioButton)
        self.radioButton_2 = QtGui.QRadioButton(ComputeBestGradient)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.verticalLayout_2.addWidget(self.radioButton_2)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(ComputeBestGradient)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_3 = QtGui.QLabel(ComputeBestGradient)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_5.addWidget(self.label_3)
        self.tr_min = QtGui.QDoubleSpinBox(ComputeBestGradient)
        self.tr_min.setDecimals(2)
        self.tr_min.setMinimum(0.0)
        self.tr_min.setMaximum(999999999.0)
        self.tr_min.setProperty("value", 2.0)
        self.tr_min.setObjectName(_fromUtf8("tr_min"))
        self.horizontalLayout_5.addWidget(self.tr_min)
        self.label_5 = QtGui.QLabel(ComputeBestGradient)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_5.addWidget(self.label_5)
        self.tr_max = QtGui.QDoubleSpinBox(ComputeBestGradient)
        self.tr_max.setDecimals(2)
        self.tr_max.setMaximum(999999999.0)
        self.tr_max.setProperty("value", 10.0)
        self.tr_max.setObjectName(_fromUtf8("tr_max"))
        self.horizontalLayout_5.addWidget(self.tr_max)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 3)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.calculateButton = QtGui.QPushButton(ComputeBestGradient)
        self.calculateButton.setMaximumSize(QtCore.QSize(110, 32))
        self.calculateButton.setObjectName(_fromUtf8("calculateButton"))
        self.horizontalLayout_3.addWidget(self.calculateButton)
        spacerItem1 = QtGui.QSpacerItem(796, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 0, 1, 3)
        self.plotterBox = QtGui.QGroupBox(ComputeBestGradient)
        self.plotterBox.setMinimumSize(QtCore.QSize(551, 311))
        self.plotterBox.setObjectName(_fromUtf8("plotterBox"))
        self.gridLayout_2.addWidget(self.plotterBox, 2, 0, 1, 3)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_10 = QtGui.QLabel(ComputeBestGradient)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout_3.addWidget(self.label_10)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_15 = QtGui.QLabel(ComputeBestGradient)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_4.addWidget(self.label_15)
        self.doubleSpinBox_5 = QtGui.QDoubleSpinBox(ComputeBestGradient)
        self.doubleSpinBox_5.setReadOnly(True)
        self.doubleSpinBox_5.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_5.setObjectName(_fromUtf8("doubleSpinBox_5"))
        self.horizontalLayout_4.addWidget(self.doubleSpinBox_5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 3, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(647, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 3, 1, 1, 2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_11 = QtGui.QLabel(ComputeBestGradient)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_2.addWidget(self.label_11)
        self.doubleSpinBox_1 = QtGui.QDoubleSpinBox(ComputeBestGradient)
        self.doubleSpinBox_1.setReadOnly(True)
        self.doubleSpinBox_1.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_1.setObjectName(_fromUtf8("doubleSpinBox_1"))
        self.horizontalLayout_2.addWidget(self.doubleSpinBox_1)
        self.label_12 = QtGui.QLabel(ComputeBestGradient)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.horizontalLayout_2.addWidget(self.label_12)
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(ComputeBestGradient)
        self.doubleSpinBox_2.setReadOnly(True)
        self.doubleSpinBox_2.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.horizontalLayout_2.addWidget(self.doubleSpinBox_2)
        self.label_13 = QtGui.QLabel(ComputeBestGradient)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_2.addWidget(self.label_13)
        self.doubleSpinBox_3 = QtGui.QDoubleSpinBox(ComputeBestGradient)
        self.doubleSpinBox_3.setReadOnly(True)
        self.doubleSpinBox_3.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_3.setObjectName(_fromUtf8("doubleSpinBox_3"))
        self.horizontalLayout_2.addWidget(self.doubleSpinBox_3)
        self.label_14 = QtGui.QLabel(ComputeBestGradient)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.horizontalLayout_2.addWidget(self.label_14)
        self.doubleSpinBox_4 = QtGui.QDoubleSpinBox(ComputeBestGradient)
        self.doubleSpinBox_4.setReadOnly(True)
        self.doubleSpinBox_4.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_4.setObjectName(_fromUtf8("doubleSpinBox_4"))
        self.horizontalLayout_2.addWidget(self.doubleSpinBox_4)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 4, 0, 1, 3)
        spacerItem3 = QtGui.QSpacerItem(932, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 5, 0, 1, 2)
        self.closeButton = QtGui.QPushButton(ComputeBestGradient)
        self.closeButton.setMaximumSize(QtCore.QSize(110, 32))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.gridLayout_2.addWidget(self.closeButton, 5, 2, 1, 1)
        self.closeButton.raise_()
        self.plotterBox.raise_()
        self.label_10.raise_()
        self.label_3.raise_()
        self.label_5.raise_()
        self.radioButton.raise_()
        self.radioButton_2.raise_()
        self.label_2.raise_()

        self.retranslateUi(ComputeBestGradient)
        QtCore.QMetaObject.connectSlotsByName(ComputeBestGradient)

    def retranslateUi(self, ComputeBestGradient):
        ComputeBestGradient.setWindowTitle(_translate("ComputeBestGradient", "Compute best gradient conditions", None))
        self.label_4.setText(_translate("ComputeBestGradient", "Select model", None))
        self.label_2.setText(_translate("ComputeBestGradient", "Search method", None))
        self.radioButton.setText(_translate("ComputeBestGradient", "Grid search", None))
        self.radioButton_2.setText(_translate("ComputeBestGradient", "Simplex", None))
        self.label.setText(_translate("ComputeBestGradient", "Peak window", None))
        self.label_3.setText(_translate("ComputeBestGradient", "<html><head/><body><p>t<span style=\" vertical-align:sub;\">R</span> min</p></body></html>", None))
        self.label_5.setText(_translate("ComputeBestGradient", "<html><head/><body><p>t<span style=\" vertical-align:sub;\">R</span> max</p></body></html>", None))
        self.calculateButton.setText(_translate("ComputeBestGradient", "Calculate", None))
        self.plotterBox.setTitle(_translate("ComputeBestGradient", "Optimization View", None))
        self.label_10.setText(_translate("ComputeBestGradient", "Best conditions:", None))
        self.label_15.setText(_translate("ComputeBestGradient", "Gradient Resolution", None))
        self.label_11.setText(_translate("ComputeBestGradient", "Gradient Start:", None))
        self.label_12.setText(_translate("ComputeBestGradient", "Gradient Stop:", None))
        self.label_13.setText(_translate("ComputeBestGradient", "Time Gradient:", None))
        self.label_14.setText(_translate("ComputeBestGradient", "Flow rate:", None))
        self.closeButton.setText(_translate("ComputeBestGradient", "Close", None))

