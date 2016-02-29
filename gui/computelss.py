'''
@package computelss.py

computelss.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

from PyQt4 import *
from PyQt4 import *
import sys

from gui_computelss import Ui_ComputeLSS

class ComputeLSS(QtGui.QDialog, Ui_ComputeLSS):
    def __init__(self, items, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.closeButton.clicked.connect(self.close_)
        self.okButton.clicked.connect(self.ok_)
        for item in items:
            self.dataBox.addItem(item)

    def close_(self):
        self.reject()

    def ok_(self):
        if self.lineEdit.text().isEmpty() == False:
            self.accept()

    def getdata(self):
        return [self.dataBox.currentIndex(), self.lineEdit.text()]
