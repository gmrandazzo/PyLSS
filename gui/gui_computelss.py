# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'computelss.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ComputeLSS(object):
    def setupUi(self, ComputeLSS):
        ComputeLSS.setObjectName("ComputeLSS")
        ComputeLSS.resize(307, 173)
        self.gridLayout = QtWidgets.QGridLayout(ComputeLSS)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(ComputeLSS)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.dataBox = QtWidgets.QComboBox(ComputeLSS)
        self.dataBox.setObjectName("dataBox")
        self.horizontalLayout.addWidget(self.dataBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(ComputeLSS)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.gradientModeBox = QtWidgets.QComboBox(ComputeLSS)
        self.gradientModeBox.setObjectName("gradientModeBox")
        self.gradientModeBox.addItem("")
        self.gradientModeBox.addItem("")
        self.verticalLayout.addWidget(self.gradientModeBox)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 3)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(ComputeLSS)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(ComputeLSS)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 2, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(222, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.closeButton = QtWidgets.QPushButton(ComputeLSS)
        self.closeButton.setMaximumSize(QtCore.QSize(110, 32))
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 3, 1, 1, 1)
        self.okButton = QtWidgets.QPushButton(ComputeLSS)
        self.okButton.setMaximumSize(QtCore.QSize(110, 32))
        self.okButton.setObjectName("okButton")
        self.gridLayout.addWidget(self.okButton, 3, 2, 1, 1)
        self.okButton.raise_()
        self.closeButton.raise_()

        self.retranslateUi(ComputeLSS)
        QtCore.QMetaObject.connectSlotsByName(ComputeLSS)

    def retranslateUi(self, ComputeLSS):
        _translate = QtCore.QCoreApplication.translate
        ComputeLSS.setWindowTitle(_translate("ComputeLSS", "Dialog"))
        self.label_4.setText(_translate("ComputeLSS", "Select data"))
        self.label_5.setText(_translate("ComputeLSS", "Gradient mode type"))
        self.gradientModeBox.setItemText(0, _translate("ComputeLSS", "Linear time gradient"))
        self.gradientModeBox.setItemText(1, _translate("ComputeLSS", "Logarithmic time gradient"))
        self.label_7.setText(_translate("ComputeLSS", "LSS model name"))
        self.closeButton.setText(_translate("ComputeLSS", "Close"))
        self.okButton.setText(_translate("ComputeLSS", "OK"))

