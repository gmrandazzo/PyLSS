# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'computelss.ui'
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

class Ui_ComputeLSS(object):
    def setupUi(self, ComputeLSS):
        ComputeLSS.setObjectName(_fromUtf8("ComputeLSS"))
        ComputeLSS.resize(410, 123)
        self.gridLayout = QtGui.QGridLayout(ComputeLSS)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_4 = QtGui.QLabel(ComputeLSS)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.dataBox = QtGui.QComboBox(ComputeLSS)
        self.dataBox.setObjectName(_fromUtf8("dataBox"))
        self.horizontalLayout.addWidget(self.dataBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 3)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lineEdit = QtGui.QLineEdit(ComputeLSS)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_7 = QtGui.QLabel(ComputeLSS)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(222, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.closeButton = QtGui.QPushButton(ComputeLSS)
        self.closeButton.setMaximumSize(QtCore.QSize(110, 32))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.gridLayout.addWidget(self.closeButton, 2, 1, 1, 1)
        self.okButton = QtGui.QPushButton(ComputeLSS)
        self.okButton.setMaximumSize(QtCore.QSize(110, 32))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.gridLayout.addWidget(self.okButton, 2, 2, 1, 1)
        self.okButton.raise_()
        self.closeButton.raise_()
        self.dataBox.raise_()
        self.label_4.raise_()
        self.label_7.raise_()

        self.retranslateUi(ComputeLSS)
        QtCore.QMetaObject.connectSlotsByName(ComputeLSS)

    def retranslateUi(self, ComputeLSS):
        ComputeLSS.setWindowTitle(_translate("ComputeLSS", "Dialog", None))
        self.label_4.setText(_translate("ComputeLSS", "Select Data", None))
        self.label_7.setText(_translate("ComputeLSS", "LSS model name", None))
        self.closeButton.setText(_translate("ComputeLSS", "Close", None))
        self.okButton.setText(_translate("ComputeLSS", "OK", None))

