'''
@package computelss.py

computelss.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

from PyQt5 import *
from PyQt5 import *
import sys

from gui_computelss import Ui_ComputeLSS

class ComputeLSS(QtWidgets.QDialog, Ui_ComputeLSS):
    def __init__(self, items, parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.closeButton.clicked.connect(self.close_)
        self.okButton.clicked.connect(self.ok_)
        for item in items:
            self.dataBox.addItem(item)

    def close_(self):
        self.reject()

    def ok_(self):
        if len(self.lineEdit.text()) > 0:
            self.accept()

    def getdata(self):
        return [self.dataBox.currentIndex(), self.lineEdit.text()]
