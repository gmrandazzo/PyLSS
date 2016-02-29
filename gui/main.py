'''
@package main.py

main.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

import sys
from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from pylss.lssengine import *
from pylss.plotengine import BuildChromatogram

import mainwindow as mw
from importdialog import *
from computelss import *
from utilities import *

class Data(object):
    def __init__(self, name, molname, trdata, grad, tg, vd, t0, flow):
        self.name = name
        self.molname = molname
        self.trdata = trdata
        self.grad = grad
        self.tg = tg
        self.t0 = t0
        self.vd = vd
        self.flow = flow

class Model(object):
    def __init__(self):
        self.modname = ""
        self.objnamelst = []
        self.v_m = 0
        self.v_d = 0
        self.lss = []

class MainWindow(QtGui.QMainWindow, mw.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.datalst = []
        self.modellst = []
        self.lstdatamodel = QtGui.QStandardItemModel(self.listView)
        self.listView.setModel(self.lstdatamodel)
        self.addButton.clicked.connect(self.add)
        self.actionCalcLSSParameter.triggered.connect(self.calculatelss)
        self.zoomButton.clicked.connect(self.zoom)
        self.panButton.clicked.connect(self.pan)
        self.rescaleButton.clicked.connect(self.home)
        self.modelBox.currentIndexChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_1.valueChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_2.valueChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_3.valueChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_4.valueChanged.connect(self.gradientanalyser)
        self.ColumnLenghtSpinBox.valueChanged.connect(self.gradientanalyser)
        self.CulumnDiameterSpinBox.valueChanged.connect(self.gradientanalyser)
        self.ColumnPorositySpinBox.valueChanged.connect(self.gradientanalyser)
        self.PeakA.valueChanged.connect(self.gradientanalyser)
        self.PeakB.valueChanged.connect(self.gradientanalyser)

        # Add plot
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.plotterBox.setLayout(layout)

        self.tablemodel = TableModel(self)
        self.tableView.setModel(self.tablemodel)

    def home(self):
        self.toolbar.home()
    def zoom(self):
        self.toolbar.zoom()
    def pan(self):
        self.toolbar.pan()

    def plotchromatogram(self):
        ''' plot some random stuff '''
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(data, '*-')
        self.canvas.draw()

    def add(self):
        idialog = ImportDialog()
        idialog.exec_()
        [name, molname, trdata, grad, tg, td, t0, flow] = idialog.getdata()
        self.datalst.append(Data(name, molname, trdata, grad, tg, td, t0, flow))
        self.lstdatamodel.appendRow(QtGui.QStandardItem(name))

    def remove(self):
        print "remove"

    def calculatelss(self):
        items = []
        lstmodel = self.listView.model()
        for index in range(lstmodel.rowCount()):
            item = lstmodel.item(index)
            items.append(item.text())

        runlss = ComputeLSS(items)
        if runlss.exec_() == 1:
            [indx, modelname] = runlss.getdata()
            t0 = self.datalst[indx].t0
            v_d = self.datalst[indx].vd
            flow = self.datalst[indx].flow

            lssmol = LinearGenerator(None, None, None, t0, v_d, flow)

            self.modellst.append(Model())
            self.modellst[-1].modname = modelname
            self.modelBox.addItem(modelname)

            tg = self.datalst[indx].tg
            init_B = []
            final_B = []
            for i in range(len(tg)):
                init_B.append(self.datalst[indx].grad[0])
                final_B.append(self.datalst[indx].grad[1])

            self.modellst[-1].v_d = v_d
            self.modellst[-1].v_m = t0 * flow

            for row in self.datalst[indx].trdata:
                lss_logkw, lss_s = lssmol.getlssparameters(row, tg, init_B, final_B)
                self.modellst[-1].lss.append([lss_logkw, lss_s])

            if len(self.modellst) == 1:
                self.gradientanalyser()

    def gradientanalyser(self):
        indx = self.modelBox.currentIndex()
        self.tablemodel.clean()
        self.tablemodel.header.append("Log kW")
        self.tablemodel.header.append("S")
        self.tablemodel.header.append("tR")

        self.tableView.model().layoutChanged.emit()
        if indx >= 0 and indx < len(self.modellst):
            lss = self.modellst[indx].lss
            flow_sofware = float(self.doubleSpinBox_1.value())
            init_B_soft = float(self.doubleSpinBox_2.value())/100.
            finalB_soft = float(self.doubleSpinBox_3.value())/100.
            tg_soft = float(self.doubleSpinBox_4.value())

            c_lenght = self.ColumnLenghtSpinBox.value()
            c_diameter = self.CulumnDiameterSpinBox.value()
            c_porosity = self.ColumnPorositySpinBox.value()

            t0_soft = 0.
            td_soft = 0.

            v_m = None
            v_d = self.modellst[indx].v_d
            if c_lenght > 0 and c_diameter > 0 and c_porosity > 0:
                v_m = ((square(self.c_diameter)*self.c_length*pi*self.c_porosity)/4.)/1000.
            else:
                v_m = self.modellst[indx].v_m

            t0_soft = float(v_m/flow_sofware)
            td_soft = float(v_d/flow_sofware)

            A = self.PeakA.value()
            B = self.PeakB.value()
            trtab = []
            lssmol = LinearGenerator(None, None, None, t0_soft, float(self.modellst[indx].v_d), flow_sofware)
            for row in lss:
                lss_logkw = float(row[0])
                lss_s = float(row[1])
                trtab.append([lssmol.rtpred(lss_logkw, lss_s, tg_soft, init_B_soft, finalB_soft, t0_soft, td_soft), A, B])
                row = [lss_logkw, lss_s, trtab[-1][0]]
                self.tablemodel.addRow(row)
                self.tableView.model().layoutChanged.emit()

            peaks = BuildChromatogram(trtab, tg_soft, 0.01)
            peaks = zip(*peaks)
            y = []
            x = []
            for i in range(len(peaks)):
                x.append(peaks[i][0])
                y.append(0.)
                len(peaks[0])
                for j in range(1, len(peaks[0])):
                    y[-1] += peaks[i][j]

            ax = self.figure.add_subplot(111)
            ax.hold(False)
            ax.plot(x, y, '-')
            self.canvas.draw()
            #self.plotchromatogram()

def main():
    app = QtGui.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
