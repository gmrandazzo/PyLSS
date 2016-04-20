'''
@package utilities.py

utilities.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

from PyQt4 import QtGui, QtCore

def nsplit(s, delim=None):
    """ Split a string by a delimiter """
    return [x.strip() for x in s.split(delim) if x]

class TableModel(QtCore.QAbstractTableModel):
    """ Class to visualize array in a QTableView """
    def __init__(self, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = []
        self.header = []

    def clean(self):
        del self.arraydata[:]

    def setHeader(self, header):
        self.header = header

    def addRow(self, row):
        self.arraydata.append(list())
        for item in row:
            self.arraydata[-1].append(item)

    def delRowAt(self, indx):
        if indx < len(self.arraydata):
            del self.arraydata[indx]

    def delColAt(self, indx):
        if len(self.arraydata) > 0:
            if indx < len(self.arraydata[0]):
                for i in range(len(self.arraydata)):
                    del self.arraydata[i][indx]

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if len(self.arraydata) > 0:
            return len(self.arraydata[0])
        else:
            return 0

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if col < len(self.header):
                return self.header[col]
            else:
                return None
        return None

    def SaveTable(self, fname):
        fo = open(fname, "w")
        for i in range(len(self.header)-1):
            fo.write("%s;" % (self.header[i]))
        fo.write("%s\n" % (self.header[-1]))
        for row in self.arraydata:
            for i in range(len(row-1)):
                fo.write("%s;" % (row[i]))
            fo.write("%s\n" % (row[-1]))
        fo.close()
