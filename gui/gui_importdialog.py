# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importdialog.ui'
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

class Ui_ImportDialog(object):
    def setupUi(self, ImportDialog):
        ImportDialog.setObjectName(_fromUtf8("ImportDialog"))
        ImportDialog.resize(493, 575)
        self.gridLayout_3 = QtGui.QGridLayout(ImportDialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.splitlineby = QtGui.QComboBox(ImportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitlineby.sizePolicy().hasHeightForWidth())
        self.splitlineby.setSizePolicy(sizePolicy)
        self.splitlineby.setMinimumSize(QtCore.QSize(0, 23))
        self.splitlineby.setMaximumSize(QtCore.QSize(112, 23))
        self.splitlineby.setEditable(True)
        self.splitlineby.setObjectName(_fromUtf8("splitlineby"))
        self.splitlineby.addItem(_fromUtf8(""))
        self.splitlineby.addItem(_fromUtf8(""))
        self.splitlineby.addItem(_fromUtf8(""))
        self.splitlineby.addItem(_fromUtf8(""))
        self.splitlineby.addItem(_fromUtf8(""))
        self.gridLayout_3.addWidget(self.splitlineby, 4, 1, 1, 2)
        self.label_4 = QtGui.QLabel(ImportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(0, 23))
        self.label_4.setMaximumSize(QtCore.QSize(159, 23))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 3, 0, 2, 1)
        self.line = QtGui.QFrame(ImportDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_3.addWidget(self.line, 2, 0, 1, 3)
        self.okButton = QtGui.QPushButton(ImportDialog)
        self.okButton.setMaximumSize(QtCore.QSize(110, 32))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.gridLayout_3.addWidget(self.okButton, 7, 2, 1, 1)
        self.closeButton = QtGui.QPushButton(ImportDialog)
        self.closeButton.setMaximumSize(QtCore.QSize(110, 32))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.gridLayout_3.addWidget(self.closeButton, 7, 1, 1, 1)
        self.firstcolobjname = QtGui.QCheckBox(ImportDialog)
        self.firstcolobjname.setMinimumSize(QtCore.QSize(0, 21))
        self.firstcolobjname.setMaximumSize(QtCore.QSize(16777215, 21))
        self.firstcolobjname.setObjectName(_fromUtf8("firstcolobjname"))
        self.gridLayout_3.addWidget(self.firstcolobjname, 5, 0, 1, 1)
        self.tableView = QtGui.QTableView(ImportDialog)
        self.tableView.setMinimumSize(QtCore.QSize(50, 50))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.gridLayout_3.addWidget(self.tableView, 6, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(305, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 7, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.openButton = QtGui.QPushButton(ImportDialog)
        self.openButton.setMaximumSize(QtCore.QSize(110, 32))
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.gridLayout_2.addWidget(self.openButton, 0, 0, 1, 1)
        self.splitter = QtGui.QSplitter(ImportDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.lineEdit = QtGui.QLineEdit(self.splitter)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout_2.addWidget(self.splitter, 0, 1, 1, 1)
        self.label_7 = QtGui.QLabel(ImportDialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(ImportDialog)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 3)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(ImportDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.dwelVolSpinBox = QtGui.QDoubleSpinBox(ImportDialog)
        self.dwelVolSpinBox.setDecimals(3)
        self.dwelVolSpinBox.setMinimum(0.0)
        self.dwelVolSpinBox.setProperty("value", 0.0)
        self.dwelVolSpinBox.setObjectName(_fromUtf8("dwelVolSpinBox"))
        self.gridLayout.addWidget(self.dwelVolSpinBox, 0, 1, 1, 1)
        self.flowrateSpinBox = QtGui.QDoubleSpinBox(ImportDialog)
        self.flowrateSpinBox.setDecimals(3)
        self.flowrateSpinBox.setProperty("value", 0.0)
        self.flowrateSpinBox.setObjectName(_fromUtf8("flowrateSpinBox"))
        self.gridLayout.addWidget(self.flowrateSpinBox, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(ImportDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.t0SpinBox = QtGui.QDoubleSpinBox(ImportDialog)
        self.t0SpinBox.setDecimals(3)
        self.t0SpinBox.setProperty("value", 0.0)
        self.t0SpinBox.setObjectName(_fromUtf8("t0SpinBox"))
        self.gridLayout.addWidget(self.t0SpinBox, 1, 1, 1, 1)
        self.label = QtGui.QLabel(ImportDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 3)

        self.retranslateUi(ImportDialog)
        QtCore.QMetaObject.connectSlotsByName(ImportDialog)

    def retranslateUi(self, ImportDialog):
        ImportDialog.setWindowTitle(_translate("ImportDialog", "Dialog", None))
        self.splitlineby.setItemText(0, _translate("ImportDialog", ";", None))
        self.splitlineby.setItemText(1, _translate("ImportDialog", "TAB", None))
        self.splitlineby.setItemText(2, _translate("ImportDialog", "SPACE", None))
        self.splitlineby.setItemText(3, _translate("ImportDialog", ",", None))
        self.splitlineby.setItemText(4, _translate("ImportDialog", "<CUSTOM>", None))
        self.label_4.setText(_translate("ImportDialog", "Separator:", None))
        self.okButton.setText(_translate("ImportDialog", "OK", None))
        self.closeButton.setText(_translate("ImportDialog", "Close", None))
        self.firstcolobjname.setText(_translate("ImportDialog", "First columns contain object names", None))
        self.openButton.setText(_translate("ImportDialog", "Open", None))
        self.label_7.setText(_translate("ImportDialog", "File name", None))
        self.label_3.setText(_translate("ImportDialog", "Flow rate:", None))
        self.label_2.setText(_translate("ImportDialog", "t0:", None))
        self.label.setText(_translate("ImportDialog", "Dwell Volume:", None))

