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
@package aboutdialog.py

aboutdialog.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

from PyQt6 import QtCore, QtGui, QtWidgets

from .gui_aboutdialog import Ui_AboutDialog

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
