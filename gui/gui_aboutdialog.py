# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(339, 106)
        self.gridLayout = QtWidgets.QGridLayout(AboutDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AboutDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(AboutDialog)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeButton = QtWidgets.QPushButton(AboutDialog)
        self.closeButton.setMaximumSize(QtCore.QSize(110, 32))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About"))
        self.label.setText(_translate("AboutDialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">PyLSS</span></p></body></html>"))
        self.label_2.setText(_translate("AboutDialog", "<html><head/><body><p><span style=\" font-size:14pt;\">Written by </span><a href=\"mailto:gmrandazzo@gmail.com;marco@chemiome.chm.unipg.it\"><span style=\" font-size:14pt; text-decoration: underline; color:#0057ae;\">Giuseppe Marco Randazzo </span></a></p></body></html>"))
        self.closeButton.setText(_translate("AboutDialog", "Close"))

