'''
@package main.py

main.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


from pylss.lssengine import *
from pylss.plotengine import BuildChromatogram

import mainwindow as mw
from importdialog import *
from computelss import *
from computebestgradient import *
from aboutdialog import *
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
        self.current_lst_index = -1
        self.addButton.clicked.connect(self.add)
        self.removeButton.clicked.connect(self.remove)
        self.actionCalcLSSParameter.triggered.connect(self.calculatelss)
        self.actionGetBestGradientConditions.triggered.connect(self.calculatebestgrad)
        self.actionAbout.triggered.connect(self.about)
        self.actionQuit.triggered.connect(self.quit)
        self.listView.clicked.connect(self.viewmatrix)
        self.toolBox.currentChanged.connect(self.viewmatrix)

        self.zoomButton.clicked.connect(self.zoom)
        self.panButton.clicked.connect(self.pan)
        self.rescaleButton.clicked.connect(self.home)
        self.modelBox.currentIndexChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_1.valueChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_2.valueChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_3.valueChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_4.valueChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_5.valueChanged.connect(self.gradientanalyser)
        self.ColumnLenghtSpinBox.valueChanged.connect(self.gradientanalyser)
        self.CulumnDiameterSpinBox.valueChanged.connect(self.gradientanalyser)
        self.ColumnPorositySpinBox.valueChanged.connect(self.gradientanalyser)

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

    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            if e.key() == QtCore.Qt.Key_C: #copy
                if len(self.tableView.selectionModel().selectedIndexes()) > 0:
                    previous = self.tableView.selectionModel().selectedIndexes()[0]
                    columns = []
                    rows = []
                    for index in self.tableView.selectionModel().selectedIndexes():
                        if previous.column() != index.column():
                            columns.append(rows)
                            rows = []
                        rows.append(str(index.data().toPyObject()))
                        previous = index
                    columns.append(rows)
                    print columns

                    # add rows and columns to clipboard
                    clipboard = ""
                    nrows = len(columns[0])
                    ncols = len(columns)
                    for r in xrange(nrows):
                        for c in xrange(ncols):
                            clipboard += columns[c][r]
                            if c != (ncols-1):
                                clipboard += '\t'
                        clipboard += '\n'

                    # copy to the system clipboard
                    sys_clip = QtGui.QApplication.clipboard()
                    sys_clip.setText(clipboard)

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
        if idialog.exec_() == 1:
            [name, molname, trdata, grad, tg, td, t0, flow] = idialog.getdata()
            self.datalst.append(Data(name, molname, trdata, grad, tg, td, t0, flow))
            self.lstdatamodel.appendRow(QtGui.QStandardItem(name))

    def remove(self):
        if self.current_lst_index >= 0 and self.current_lst_index < len(self.datalst):
            del self.datalst[self.current_lst_index]
            self.lstdatamodel.removeRow(self.current_lst_index)

    def viewmatrix(self, indx):
        if self.toolBox.currentIndex() == 0:
            if indx:
                self.current_lst_index =  indx.row()
                del self.tablemodel.arraydata[:]
                del self.tablemodel.header[:]
                self.tablemodel.clean()
                self.tableView.model().layoutChanged.emit()
                molname = self.datalst[self.current_lst_index].molname
                trdata = self.datalst[self.current_lst_index].trdata
                grad = self.datalst[self.current_lst_index].grad
                self.tablemodel.header.append("Molecules")
                for i in range(len(grad)):
                    self.tablemodel.header.append("tR %d" % (int(grad[i]*100)))
                if len(molname) > 0:
                    for i in range(len(trdata)):
                        row = [molname[i]]
                        for j in range(len(trdata[i])):
                            row.append(trdata[i][j])
                        self.tablemodel.addRow(row)
                else:
                    for i in range(len(trdata)):
                        row = ["Molecule %d" % (i)]
                        for j in range(len(trdata[i])):
                            row.append(trdata[i][j])
                        self.tablemodel.addRow(row)
                self.tableView.model().layoutChanged.emit()
        else:
            del self.tablemodel.arraydata[:]
            del self.tablemodel.header[:]
            self.tablemodel.clean()
            self.tableView.model().layoutChanged.emit()
            self.gradientanalyser()

    def about(self):
        adialog = AboutDialog()
        adialog.exec_()

    def quit(self):
        QtGui.QApplication.quit()

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

    def calculatebestgrad(self):
        getbestgrad = ComputeBestGradient(self.modellst)
        getbestgrad.exec_()

    def gradientanalyser(self):
        indx = self.modelBox.currentIndex()
        del self.tablemodel.arraydata[:]
        del self.tablemodel.header[:]
        self.tablemodel.clean()
        self.tablemodel.header.append("Molecule")
        self.tablemodel.header.append("Log kW")
        self.tablemodel.header.append("S")
        self.tablemodel.header.append("tR")

        self.tableView.model().layoutChanged.emit()
        if indx >= 0 and indx < len(self.modellst):
            lss = self.modellst[indx].lss
            flow_sofware = float(self.doubleSpinBox_1.value())
            init_B_soft = float(self.doubleSpinBox_2.value())/100.
            final_B_soft = float(self.doubleSpinBox_3.value())/100.
            tg_soft = float(self.doubleSpinBox_4.value())

            c_lenght = self.ColumnLenghtSpinBox.value()
            c_diameter = self.CulumnDiameterSpinBox.value()
            c_particle = self.ColumnPorositySpinBox.value()

            t0_soft = 0.
            td_soft = 0.

            v_m = None
            v_d = float(self.doubleSpinBox_5.value())

            #if c_lenght > 0 and c_diameter > 0 and c_porosity > 0:
            #    v_m = ((square(self.c_diameter)*self.c_length*pi*self.c_porosity)/4.)/1000.
            #else:
            v_m = self.modellst[indx].v_m

            t0_soft = float(v_m/flow_sofware)
            td_soft = float(v_d/flow_sofware)

            A = 1.0

            N = (c_lenght*10000.)/(2.3*c_particle)

            trtab = []
            lssmol = LinearGenerator(None, None, None, t0_soft, float(self.modellst[indx].v_d), flow_sofware)
            i = 1
            for row in lss:
                lss_logkw = float(row[0])
                lss_s = float(row[1])
                b = (t0_soft*(final_B_soft-init_B_soft)*lss_s)/tg_soft
                # See D. Guillazne et al / J. Chromatogr. A 1216(2009) 3232-3243
                W = (4*t0_soft)/sqrt(N)* (1+ 1/(2.3*b))/4
                trtab.append([lssmol.rtpred(lss_logkw, lss_s, tg_soft, init_B_soft, final_B_soft, t0_soft, td_soft), A, W])
                row = ["Molecule %d" % (i), lss_logkw, lss_s, trtab[-1][0]]
                self.tablemodel.addRow(row)
                self.tableView.model().layoutChanged.emit()
                i += 1

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
            plt.xlabel('Time')
            plt.ylabel('Signal')

            self.canvas.draw()
            #self.plotchromatogram()

def main():
    app = QtGui.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
