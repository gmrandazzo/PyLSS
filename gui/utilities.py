'''
@package utilities.py

utilities.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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
        self.beginResetModel.emit()
        self.endResetModel.emit()

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

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if len(self.arraydata) > 0:
            return len(self.arraydata[0])
        else:
            return 0

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
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
