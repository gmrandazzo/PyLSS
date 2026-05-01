#!/usr/bin/env python
#
# Copyright (C) 2026 Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
@package computelss.py

computelss.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

from PyQt6 import QtCore, QtGui, QtWidgets
import sys

from .gui_computelss import Ui_ComputeLSS

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
