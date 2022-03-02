'''
@package main.py

main.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

import os
import sys

path = None
try:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
except NameError:
    path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
path += "/pylss"
print(path)
if not path in sys.path:
    sys.path.insert(1, path)
del path


from PyQt5 import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.backends.backend_tkagg
import matplotlib.pyplot as plt


from ssengine import *
from plotengine import BuildChromatogram

import mainwindow as mw
from importdialog import *
from computelss import *
from automaticelutionwindowstretching import *
from plotmaps import *
from aboutdialog import *
from utilities import *

class Data(object):
    def __init__(self, name, molname, trdata, grad, tg, vd, t0, flow, c_length, c_diameter, c_particle):
        self.name = name
        self.molname = molname
        self.trdata = trdata
        self.grad = grad
        self.tg = tg
        self.t0 = t0
        self.vd = vd
        self.flow = flow
        self.c_length = c_length
        self.c_diameter = c_diameter
        self.c_particle = c_particle

class Model(object):
    def __init__(self):
        self.modname = ""
        self.molname = []
        self.v_m = 0
        self.v_d = 0
        self.flow = 0
        self.lss = []
        self.c_length = 15
        self.c_particle = 1.7
        self.c_diameter = 2.10

class MainWindow(QtWidgets.QMainWindow, mw.Ui_MainWindow):
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
        self.actionAutomaticElutionWindowStretching.triggered.connect(self.calcautelwindowstretch)
        self.actionSelectivityMap.triggered.connect(self.pltselectivitymap)
        self.actionResolutionMap.triggered.connect(self.pltresolutionmap)
        self.actionAbout.triggered.connect(self.about)
        self.actionQuit.triggered.connect(self.quit)
        self.listView.clicked.connect(self.viewmatrix)
        self.toolBox.currentChanged.connect(self.viewmatrix)

        self.zoomButton.clicked.connect(self.zoom)
        self.panButton.clicked.connect(self.pan)
        self.rescaleButton.clicked.connect(self.home)
        self.exportchromatogramButton.clicked.connect(self.exportchromatogram)
        self.setplotoptionsButton.clicked.connect(self.setplotoptions)
        self.modelBox.currentIndexChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_1.valueChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_2.valueChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_3.valueChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_4.valueChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_5.valueChanged.connect(self.gradientanalyser)
        self.doubleSpinBox_6.valueChanged.connect(self.gradientanalyser)
        self.ColumnLenghtSpinBox.valueChanged.connect(self.gradientanalyser)
        self.CulumnDiameterSpinBox.valueChanged.connect(self.gradientanalyser)
        self.ColumnPorositySpinBox.valueChanged.connect(self.gradientanalyser)

        # Add plot
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()

        # set the layout
        layout_chormatogram = QtWidgets.QVBoxLayout()
        layout_chormatogram.addWidget(self.canvas)
        self.plotterBox.setLayout(layout_chormatogram)

        # Add selectivity map plot
        #self.figure_smap = plt.figure()
        #self.canvas_smap = FigureCanvas(self.figure_smap)
        #self.toolbar_smap = NavigationToolbar(self.canvas_smap, self)
        #self.toolbar_smap.hide()

        #layout_smap = QtWidgets.QVBoxLayout()
        #layout_smap.addWidget(self.canvas_smap)
        #self.plotterBox_2.setLayout(layout_smap)

        self.tablemodel = TableModel(self)
        self.tableView.setModel(self.tablemodel)
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.openTableMenu)

        # constant parameters
        self.crit_resolution = 1.8
        self.crit_alpha = 1.1

        self.peaks = None
        self.crit_peaks = None

    def openTableMenu(self, position):
        """ context menu event """
        menu = QtWidgets.QMenu(self)
        exportAction = menu.addAction("Export table as CSV")
        action = menu.exec_(self.tableView.viewport().mapToGlobal(position))

        if action == exportAction:
            fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "CSV (*.csv)");
            self.tablemodel.SaveTable(fname)
        else:
            return


        return


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
                    sys_clip = QtWidgets.QApplication.clipboard()
                    sys_clip.setText(clipboard)

    def home(self):
        self.toolbar.home()

    def zoom(self):
        self.toolbar.zoom()

    def pan(self):
        self.toolbar.pan()

    def setplotoptions(self):
        return

    def exportchromatogram(self):
        if self.peaks != None and self.crit_peaks != None:
            fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "CSV (*.csv)")
            print(os.path.exists(fname))
            if not os.path.exists(fname):
                y = []
                x = []
                for i in range(len(self.peaks)):
                    x.append(self.peaks[i][0])
                    y.append(0.)
                    for j in range(1, len(self.peaks[0])):
                        y[-1] += self.peaks[i][j]

                crit_y = []
                crit_x = []
                for i in range(len(self.crit_peaks)):
                    crit_x.append(self.crit_peaks[i][0])
                    crit_y.append(0.)
                    for j in range(1, len(self.crit_peaks[0])):
                        crit_y[-1] += self.crit_peaks[i][j]

                fo = open(fname, "w")
                for i in range(len(x)):
                    fo.write("%.4f;%.4f\n" % (x[i], y[i]))
                for i in range(len(crit_x)):
                    fo.write("%.4f;%.4f\n" % (crit_x[i], crit_y[i]))
                fo.close()
        else:
            return

    def plotchromatogram(self):
        ''' plot some random stuff '''
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot(data, '*-')
        self.canvas.draw()

    def add(self):
        idialog = ImportDialog()
        if idialog.exec_() == 1:
            [name, molname, trdata, grad, tg, td, t0, flow, c_length, c_diameter, c_particle] = idialog.getdata()
            self.datalst.append(Data(name, molname, trdata, grad, tg, td, t0, flow, c_length, c_diameter, c_particle))
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
                tg = self.datalst[self.current_lst_index].tg
                header = ["Molecule"]
                for j in range(len(tg)):
                    header.append(str("%.1f%% %.1f%% %.1f min" % (round(grad[j][0]*100,1), round(grad[j][1]*100,1), tg[j])))
                self.tablemodel.setHeader(header)
                for i in range(len(trdata)):
                    row = [molname[i]]
                    for j in range(len(trdata[i])):
                        row.append(round(trdata[i][j], 2))
                    self.tablemodel.addRow(row)
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
        QtWidgets.QApplication.quit()

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

            lssmol = SSGenerator(None, None, None, t0, v_d, flow)

            self.modellst.append(Model())
            self.modellst[-1].modname = modelname
            self.modellst[-1].molname = self.datalst[indx].molname
            self.modellst[-1].flow = self.datalst[indx].flow
            self.modellst[-1].c_length = self.datalst[indx].c_length
            self.modellst[-1].c_diameter = self.datalst[indx].c_diameter
            self.modellst[-1].c_particle = self.datalst[indx].c_particle
            self.modelBox.addItem(modelname)

            tg = self.datalst[indx].tg
            init_B = []
            final_B = []
            for i in range(len(tg)):
                init_B.append(self.datalst[indx].grad[i][0])
                final_B.append(self.datalst[indx].grad[i][1])

            self.modellst[-1].v_d = v_d
            self.modellst[-1].v_m = t0 * flow

            for row in self.datalst[indx].trdata:
                lss_logkw, lss_s = lssmol.getlssparameters(row, tg, init_B, final_B)
                self.modellst[-1].lss.append([lss_logkw, lss_s])

            if len(self.modellst) == 1:
                self.gradientanalyser()

    def calcautelwindowstretch(self):
        aws = AutomaticElutionWindowStretching(self.modellst)
        aws.exec_()

    def pltselectivitymap(self):
        smap = PlotMaps(self.modellst, "sel")
        smap.exec_()

    def pltresolutionmap(self):
        rsmap = PlotMaps(self.modellst, "res")
        rsmap.exec_()

    def gradientanalyser(self):
        indx = self.modelBox.currentIndex()
        del self.tablemodel.arraydata[:]
        del self.tablemodel.header[:]
        self.tablemodel.clean()
        header = ["Molecule", "log kW", "S", "tR"]
        self.tablemodel.setHeader(header)
        self.tableView.model().layoutChanged.emit()
        if indx >= 0 and indx < len(self.modellst):
            #predict the retention time for each compound
            molname = [name for name in self.modellst[indx].molname]
            lss = self.modellst[indx].lss
            flow_sofware = float(self.doubleSpinBox_1.value())
            init_B_soft = float(self.doubleSpinBox_2.value())/100.
            final_B_soft = float(self.doubleSpinBox_3.value())/100.
            tg_soft = float(self.doubleSpinBox_4.value())

            c_length = self.ColumnLenghtSpinBox.value()
            c_diameter = self.CulumnDiameterSpinBox.value()
            c_particle = self.ColumnPorositySpinBox.value()

            t0_soft = 0.
            td_soft = 0.

            v_m = None
            v_d = float(self.doubleSpinBox_5.value())

            #if c_length > 0 and c_diameter > 0 and c_porosity > 0:
            #    v_m = ((square(self.c_diameter)*self.c_length*pi*self.c_porosity)/4.)/1000.
            #else:
            #
            #v_m = self.modellst[indx].v_m
            #t0_soft = float(v_m/flow_sofware)
            t0_soft = float(self.doubleSpinBox_6.value())
            td_soft = float(v_d/flow_sofware)

            A = 1.0

            #N = (c_length*10000.)/(3.4*c_particle)
            trtab = []
            lssmol = SSGenerator(None, None, None, t0_soft, float(self.modellst[indx].v_d), flow_sofware)
            i = 0
            trlst = []
            for row in lss:
                lss_logkw = float(row[0])
                lss_s = float(row[1])
                W = get_lss_peak_width(c_length, c_particle, lss_logkw, lss_s, init_B_soft, final_B_soft, tg_soft, flow_sofware, self.modellst[indx].v_m, self.modellst[indx].v_d, None)
                tr = lssmol.rtpred(lss_logkw, lss_s, tg_soft, init_B_soft, final_B_soft, t0_soft, td_soft)
                if tr < t0_soft:
                    trtab.append([t0_soft, A, W])
                else:
                    trtab.append([tr, A, W])
                trlst.append([round(trtab[-1][0], 2), W, molname[i]])
                row = [molname[i], round(lss_logkw, 3), round(lss_s, 3), round(trtab[-1][0],2)]
                self.tablemodel.addRow(row)
                self.tableView.model().layoutChanged.emit()
                i += 1

            # Calculate the critical resolution
            trlst = sorted(trlst, key=lambda x:x[0])
            # get min and max time
            tr_min = tr_max = 0.
            if len(trlst) > 0:
                tr_min = trlst[0][0]
                tr_max = trlst[-1][0]
                # calculate resolution and critical couple
                # get the peak width at base multiplying by 1.7
                self.plainTextEdit.clear()
                text = "Critical couples:\n"
                self.plainTextEdit.appendPlainText(text)

                crit_trtab = []
                crit_molname = []
                ncc = 0
                for i in range(1, len(trlst)):
                    width1 = trlst[i][1] * 1.7
                    width2 = trlst[i-1][1] * 1.7
                    tr1 = trlst[i-1][0]
                    tr2 = trlst[i][0]
                    tmp_rs = (2*(tr2-tr1)) / (width1+width2)
                    if tmp_rs < self.crit_resolution:
                        molname_a = trlst[i-1][2]
                        molname_b = trlst[i][2]
                        text =  "  - %s  %.2f min\n" % (molname_a, round(trlst[i-1][0], 2))
                        text += "  - %s  %.2f min\n" % (molname_b, round(trlst[i][0], 2))
                        text += "Rs: %.2f\n" % round(tmp_rs, 2)
                        text += "#"*20
                        text += "\n"
                        self.plainTextEdit.appendPlainText(text)
                        ncc += 1
                        if molname_a not in crit_molname:
                            # add to critical tr tab
                            a_indx = molname.index(molname_a)
                            crit_trtab.append(trtab.pop(a_indx))
                            crit_molname.append(molname.pop(a_indx))

                        if molname_b not in crit_molname:
                            b_indx = molname.index(molname_b)
                            crit_trtab.append(trtab.pop(b_indx))
                            crit_molname.append(molname.pop(b_indx))
                    else:
                        continue

                self.plainTextEdit.appendPlainText("Total critical couples: %d" % (ncc))

                #Create a cromatogram
                self.peaks = list(zip(*BuildChromatogram(trtab, tg_soft, 0.01)))
                self.crit_peaks = list(zip(*BuildChromatogram(crit_trtab, tg_soft, 0.01)))

                y = []
                x = []
                for i in range(len(self.peaks)):
                    x.append(self.peaks[i][0])
                    y.append(0.)
                    #len(self.peaks[0])
                    for j in range(1, len(self.peaks[0])):
                        y[-1] += self.peaks[i][j]

                crit_y = []
                crit_x = []
                for i in range(len(self.crit_peaks)):
                    crit_x.append(self.crit_peaks[i][0])
                    crit_y.append(0.)
                    #len(peaks[0])
                    for j in range(1, len(self.crit_peaks[0])):
                        crit_y[-1] += self.crit_peaks[i][j]
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.clear()
                ax.plot(x, y, "b", crit_x, crit_y, "r")

                #ax.plot(x, y, '-', color='blue')
                #ax.plot(crit_x, crit_y, '-', color='red')
                plt.xlabel('Time')
                plt.ylabel('Signal')
                plt.xlim([tr_min-((tr_min*10.)/100.), tr_max+((tr_max*10.)/100.)])
                self.canvas.draw()
                #self.plotchromatogram()




def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
