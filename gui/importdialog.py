from PyQt4 import *
from PyQt4 import *
import sys

from gui_importdialog import Ui_ImportDialog
from os.path import isfile, basename

def nsplit(s, delim=None):
    return [x for x in s.split(delim) if x]

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = []
        self.header = []

    def clean(self):
        del self.arraydata[:]

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
            return self.header[col]
        return None

class ImportDialog(QtGui.QDialog, Ui_ImportDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.tablemodel = TableModel(self)
        self.tableView.setModel(self.tablemodel)
        self.openButton.clicked.connect(self.open_)
        self.closeButton.clicked.connect(self.close_)
        self.okButton.clicked.connect(self.ok_)
        self.splitlineby.currentIndexChanged.connect(self.preview)
        self.lineEdit.textChanged.connect(self.preview)

    def open_(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        if fname and isfile(fname):
            self.lineEdit.setText(fname)
            self.lineEdit_2.setText(str.split(basename(str(fname)), ".")[0])
            self.preview()

    def close_(self):
        self.reject()

    def ok_(self):
        self.accept()

    def preview(self):
        f = open(self.lineEdit.text())
        self.tablemodel.clean()
        i = 0
        for line in f:
            if i < 10:
                v = nsplit(line.strip(), self.splitlineby.currentText())
                self.tablemodel.addRow(v)
                self.tableView.model().layoutChanged.emit()
            else:
                break
        f.close()

    def getdata(self):
        trdata = []
        molname = []
        grad = [self.GStartSpinBox.value()/100., self.GStopSpinBox.value()/100.]
        tg = []
        if self.firstcolobjname.isChecked():
            f = open(self.lineEdit.text())
            self.tablemodel.clean()
            i = 0
            for line in f:
                v = nsplit(line.strip(), self.splitlineby.currentText())
                if i == 0:
                    for item in v[1:-1]:
                        tg.append(float(item))
                else:
                    molname.append(v[0])
                    trdata.append(list())
                    for item in v[1:-1]:
                        trdata[-1].append(float(item))
                i += 1
            f.close()
        else:
            f = open(self.lineEdit.text())
            self.tablemodel.clean()
            i = 0
            trdata = []
            for line in f:
                v = nsplit(line.strip(), self.splitlineby.currentText())
                if i == 0:
                    for item in v:
                        tg.append(float(item))
                else:
                    molname.append("Molecule %d" % (i+1))
                    trdata.append(list())
                    for item in v:
                        trdata[-1].append(float(item))
                i += 1
            f.close()

        return [self.lineEdit_2.text(), molname, trdata, grad, tg,
                self.dwelVolSpinBox.value(), self.t0SpinBox.value(),
                self.flowrateSpinBox.value()]
