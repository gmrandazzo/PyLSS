'''
@package aboutdialog.py

aboutdialog.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

from PyQt5 import *
from PyQt5 import *

from gui_aboutdialog import Ui_AboutDialog

class AboutDialog(QtWidgets.QDialog, Ui_AboutDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.closeButton.clicked.connect(self.close_)

    def changeTitle(self, new_title):
        self.label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">"+new_title+"</span></p></body></html>")

    def changeText(self, new_text):
        self.label_2.setText(new_text)

    def close_(self):
        self.reject()
