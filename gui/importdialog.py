'''
@package importdialog.py

importdialog.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

from PyQt6 import QtCore, QtGui, QtWidgets
import sys

from .gui_importdialog import Ui_ImportDialog
from os.path import isfile, basename
from .utilities import TableModel, nsplit
from pylss.io import parse_lss_input

class ImportDialog(QtWidgets.QDialog, Ui_ImportDialog):
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.tablemodel = TableModel(self)
        self.tableView.setModel(self.tablemodel)
        self.openButton.clicked.connect(self.open_)
        self.closeButton.clicked.connect(self.close_)
        self.okButton.clicked.connect(self.ok_)
        self.splitlineby.currentIndexChanged.connect(self.preview)
        self.lineEdit.textChanged.connect(self.preview)
        self.firstcolobjname.stateChanged.connect(self.preview)

    def open_(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')
        if fname and isfile(fname):
            self.lineEdit.setText(fname)
            self.lineEdit_2.setText(str.split(basename(str(fname)), ".")[0])
            self.preview()

    def close_(self):
        self.reject()

    def ok_(self):
        self.accept()

    def preview(self):
        if not isfile(self.lineEdit.text()):
            return
            
        experiment = parse_lss_input(self.lineEdit.text())
        self.tablemodel.clean()
        
        # Update spinboxes
        if experiment.dwell_volume: self.dwelVolSpinBox.setValue(experiment.dwell_volume)
        if experiment.flow_rate: self.flowrateSpinBox.setValue(experiment.flow_rate)
        if experiment.t0: self.t0SpinBox.setValue(experiment.t0)
        
        grad = []
        tg = []
        for g in experiment.gradients:
            tg.append(float(g[0]))
            grad.append([float(g[1])/100., float(g[2])/100.])
            
        header = ["Molecule"]
        for j in range(len(grad)):
            header.append("%.1f%% %.1f%% %.1f min" % (round(grad[j][0]*100,1), round(grad[j][1]*100,1), tg[j]))
        self.tablemodel.setHeader(header)

        for i, v in enumerate(experiment.data[:11]): # Preview first 10 rows
            if not v or v[0].lower() == 'molecule': continue
            
            row: list = []
            if i < 10:
                # Use robust detection for molecule name
                try:
                    float(v[0])
                    # Numeric, use auto-name
                    row.append("Molecule %d" % (i+1))
                    for item in v:
                        try:
                            row.append(float(item))
                        except:
                            row.append(item)
                except ValueError:
                    # String, use it as name
                    row.append(v[0])
                    for j in range(1, len(v)):
                        try:
                            row.append(float(v[j]))
                        except:
                            row.append(v[j])
                
                self.tablemodel.addRow(row)
            else:
                row.append("...")
                for j in range(len(v)):
                    row.append("...")
                self.tablemodel.addRow(row)
                break

    def getdata(self):
        experiment = parse_lss_input(self.lineEdit.text())
        
        trdata: list[list[float]] = []
        molname = []
        grad = []
        tg = []
        
        c_length = experiment.column_length
        c_diameter = experiment.column_diameter
        c_particle = experiment.column_particle
        
        for g in experiment.gradients:
            tg.append(float(g[0]))
            grad.append([float(g[1])/100., float(g[2])/100.])

        for i, v in enumerate(experiment.data):
            if not v or v[0].lower() == 'molecule': continue
            
            trdata.append(list())
            # Logic to handle molecule names
            try:
                float(v[0])
                # It's a number, so it's a retention time
                molname.append("Molecule %d" % (len(trdata)))
                for item in v:
                    trdata[-1].append(float(item))
            except ValueError:
                # It's a string, likely the molecule name
                molname.append(v[0])
                for j in range(1, len(v)):
                    trdata[-1].append(float(v[j]))
        
        return [self.lineEdit_2.text(), molname, trdata, grad, tg,
                self.dwelVolSpinBox.value(), self.t0SpinBox.value(),
                self.flowrateSpinBox.value(), c_length, c_diameter, c_particle]
