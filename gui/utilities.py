'''
@package utilities.py

utilities.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

from PyQt6.QtCore import (
    Qt, QAbstractTableModel, pyqtSignal, QModelIndex, QVariant, QTimer
)
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import QApplication, QFileDialog

def nsplit(s, delim=None):
    """ Split a string by a delimiter """
    return [x.strip() for x in s.split(delim) if x]

class TableModel(QAbstractTableModel):
    """ Class to visualize array in a QTableView """
    refreshTable = pyqtSignal()

    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = []
        self.header = []
        self.timer = self.startTimer(300)

    def timerEvent(self, e):
        if self.timer == e.timerId():
            self.refreshTable.emit()
        else:
            super(TableModel, self).timerEvent(e)

    def refreshTableSlot(self):
        self.beginResetModel()
        self.endResetModel()

    def clean(self):
        del self.arraydata[:]

    def setHeader(self, header):
        self.header = header

    def addRow(self, row):
        self.beginResetModel()
        self.arraydata.append(list())
        for item in row:
            self.arraydata[-1].append(item)
        self.endResetModel()

    def delRowAt(self, indx):
        self.beginResetModel()
        if indx < len(self.arraydata):
            del self.arraydata[indx]
        self.endResetModel()

    def delColAt(self, indx):
        self.beginResetModel()
        if len(self.arraydata) > 0:
            if indx < len(self.arraydata[0]):
                for i in range(len(self.arraydata)):
                    del self.arraydata[i][indx]
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self.arraydata)

    def columnCount(self, parent=QModelIndex()):
        if len(self.arraydata) > 0:
            return len(self.arraydata[0])
        else:
            return 0

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        elif role != Qt.ItemDataRole.DisplayRole:
            return None
        return self.arraydata[index.row()][index.column()]

    def headerData(self, col, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if col < len(self.header):
                return self.header[col]
            else:
                return None
        return None

    def SaveTable(self, fname):
        if fname != None:
            fo = open(fname, "w")
            for i in range(len(self.header)-1):
                fo.write("%s;" % (self.header[i]))
            fo.write("%s\n" % (self.header[-1]))
            for row in self.arraydata:
                for i in range(len(row)-1):
                    fo.write("%s;" % (row[i]))
                fo.write("%s\n" % (row[-1]))
            fo.close()
            return
        else:
            return
