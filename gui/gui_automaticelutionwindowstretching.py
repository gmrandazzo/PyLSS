# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'automaticelutionwindowstretching.ui'
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

class Ui_AutomaticElutionWindowStretching(object):
    def setupUi(self, AutomaticElutionWindowStretching):
        AutomaticElutionWindowStretching.setObjectName(_fromUtf8("AutomaticElutionWindowStretching"))
        AutomaticElutionWindowStretching.resize(658, 251)
        self.gridLayout = QtGui.QGridLayout(AutomaticElutionWindowStretching)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.calculateButton = QtGui.QPushButton(AutomaticElutionWindowStretching)
        self.calculateButton.setMaximumSize(QtCore.QSize(110, 32))
        self.calculateButton.setObjectName(_fromUtf8("calculateButton"))
        self.horizontalLayout_3.addWidget(self.calculateButton)
        spacerItem = QtGui.QSpacerItem(796, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 4)
        spacerItem1 = QtGui.QSpacerItem(932, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_4 = QtGui.QLabel(AutomaticElutionWindowStretching)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.modelBox = QtGui.QComboBox(AutomaticElutionWindowStretching)
        self.modelBox.setObjectName(_fromUtf8("modelBox"))
        self.horizontalLayout.addWidget(self.modelBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 4)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(AutomaticElutionWindowStretching)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_3 = QtGui.QLabel(AutomaticElutionWindowStretching)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_5.addWidget(self.label_3)
        self.tr_min = QtGui.QDoubleSpinBox(AutomaticElutionWindowStretching)
        self.tr_min.setDecimals(2)
        self.tr_min.setMinimum(0.0)
        self.tr_min.setMaximum(999999999.0)
        self.tr_min.setProperty("value", 2.0)
        self.tr_min.setObjectName(_fromUtf8("tr_min"))
        self.horizontalLayout_5.addWidget(self.tr_min)
        self.label_5 = QtGui.QLabel(AutomaticElutionWindowStretching)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_5.addWidget(self.label_5)
        self.tr_max = QtGui.QDoubleSpinBox(AutomaticElutionWindowStretching)
        self.tr_max.setDecimals(2)
        self.tr_max.setMaximum(999999999.0)
        self.tr_max.setProperty("value", 10.0)
        self.tr_max.setObjectName(_fromUtf8("tr_max"))
        self.horizontalLayout_5.addWidget(self.tr_max)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 2)
        self.closeButton = QtGui.QPushButton(AutomaticElutionWindowStretching)
        self.closeButton.setMaximumSize(QtCore.QSize(110, 32))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.gridLayout.addWidget(self.closeButton, 4, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(215, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 2)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_16 = QtGui.QLabel(AutomaticElutionWindowStretching)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.horizontalLayout_6.addWidget(self.label_16)
        self.doubleSpinBox_6 = QtGui.QDoubleSpinBox(AutomaticElutionWindowStretching)
        self.doubleSpinBox_6.setReadOnly(True)
        self.doubleSpinBox_6.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_6.setObjectName(_fromUtf8("doubleSpinBox_6"))
        self.horizontalLayout_6.addWidget(self.doubleSpinBox_6)
        self.label_17 = QtGui.QLabel(AutomaticElutionWindowStretching)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.horizontalLayout_6.addWidget(self.label_17)
        self.doubleSpinBox_7 = QtGui.QDoubleSpinBox(AutomaticElutionWindowStretching)
        self.doubleSpinBox_7.setReadOnly(True)
        self.doubleSpinBox_7.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_7.setObjectName(_fromUtf8("doubleSpinBox_7"))
        self.horizontalLayout_6.addWidget(self.doubleSpinBox_7)
        self.label_18 = QtGui.QLabel(AutomaticElutionWindowStretching)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.horizontalLayout_6.addWidget(self.label_18)
        self.doubleSpinBox_8 = QtGui.QDoubleSpinBox(AutomaticElutionWindowStretching)
        self.doubleSpinBox_8.setReadOnly(True)
        self.doubleSpinBox_8.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_8.setObjectName(_fromUtf8("doubleSpinBox_8"))
        self.horizontalLayout_6.addWidget(self.doubleSpinBox_8)
        self.gridLayout.addLayout(self.horizontalLayout_6, 3, 0, 1, 4)
        self.closeButton.raise_()

        self.retranslateUi(AutomaticElutionWindowStretching)
        QtCore.QMetaObject.connectSlotsByName(AutomaticElutionWindowStretching)

    def retranslateUi(self, AutomaticElutionWindowStretching):
        AutomaticElutionWindowStretching.setWindowTitle(_translate("AutomaticElutionWindowStretching", "Automatic elution windows stretching", None))
        self.calculateButton.setText(_translate("AutomaticElutionWindowStretching", "Calculate", None))
        self.label_4.setText(_translate("AutomaticElutionWindowStretching", "Select model", None))
        self.label.setText(_translate("AutomaticElutionWindowStretching", "Peak window", None))
        self.label_3.setText(_translate("AutomaticElutionWindowStretching", "<html><head/><body><p>t<span style=\" vertical-align:sub;\">R</span> min</p></body></html>", None))
        self.label_5.setText(_translate("AutomaticElutionWindowStretching", "<html><head/><body><p>t<span style=\" vertical-align:sub;\">R</span> max</p></body></html>", None))
        self.closeButton.setText(_translate("AutomaticElutionWindowStretching", "Close", None))
        self.label_16.setText(_translate("AutomaticElutionWindowStretching", "Gradient Start:", None))
        self.label_17.setText(_translate("AutomaticElutionWindowStretching", "Gradient Stop:", None))
        self.label_18.setText(_translate("AutomaticElutionWindowStretching", "Time Gradient:", None))

