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
@package main.py

main.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve January 2017
'''

import os
import sys

#Need matplotlib

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.backends.backend_qtagg
import matplotlib.pyplot as plt
import numpy as np

from PyQt6 import QtWidgets, QtCore, QtGui

from os.path import isfile, basename
from .gui_chromanalyzer import Ui_ChromAnalyzer
from .aboutdialog import AboutDialog
from .utilities import TableModel
from ..chromanalysis import ChromAnalysis

class ChromAnalyzer(QtWidgets.QWidget, Ui_ChromAnalyzer):
    def __init__(self, parent=None):
        super(ChromAnalyzer, self).__init__(parent)
        self.setupUi(self)

        self.openChromButton.clicked.connect(self.openchrom)
        self.analyzeButton.clicked.connect(self.analyze)
        self.aboutButton.clicked.connect(self.about)
        self.quitButton.clicked.connect(self.quit)

        self.tablemodel = TableModel(self)
        self.tableView.setModel(self.tablemodel)
        self.tableView.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.openTableMenu)

        # Add plot
        self.figure = plt.figure(dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()

        # set the layout
        layout_chormatogram = QtWidgets.QVBoxLayout()
        layout_chormatogram.addWidget(self.canvas)
        self.plotterBox.setLayout(layout_chormatogram)

    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier):
            if e.key() == QtCore.Qt.Key.Key_C: #copy
                selection_model = self.tableView.selectionModel()
                if selection_model is not None and len(selection_model.selectedIndexes()) > 0:
                    previous = selection_model.selectedIndexes()[0]
                    columns: list[list[str]] = []
                    rows: list[str] = []
                    for index in selection_model.selectedIndexes():
                        if previous.column() != index.column():
                            columns.append(rows)
                            rows = []
                        rows.append(str(index.data()))
                        previous = index
                    columns.append(rows)

                    # add rows and columns to clipboard
                    clipboard = ""
                    nrows = len(columns[0])
                    ncols = len(columns)
                    for r in range(nrows):
                        for c in range(ncols):
                            clipboard += columns[c][r]
                            if c != (ncols-1):
                                clipboard += '\t'
                        clipboard += '\n'

                    # copy to the system clipboard
                    sys_clip = QtWidgets.QApplication.clipboard()
                    if sys_clip is not None:
                        sys_clip.setText(clipboard)

    def openTableMenu(self, position):
        """ context menu event """
        menu = QtWidgets.QMenu(self)
        exportAction = menu.addAction("Export table as CSV")
        viewport = self.tableView.viewport()
        if viewport is not None:
            action = menu.exec(viewport.mapToGlobal(position))
            if action == exportAction:
                fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "CSV (*.csv)");
                self.tablemodel.SaveTable(fname)
            else:
                return
        return

    def openchrom(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')
        if fname and isfile(fname):
            self.lineEdit.setText(fname)

    def about(self):
        adialog = AboutDialog()
        adialog.changeTitle("ChromAnalyzer")
        adialog.exec()

    def quit(self):
        QtWidgets.QApplication.quit()


    def analyze(self):
        if self.lineEdit.text() and isfile(self.lineEdit.text()):
            #Clean previous table
            del self.tablemodel.arraydata[:]
            del self.tablemodel.header[:]
            self.tablemodel.clean()

            #set table header
            header = ["Peak", "Peak points", "time min", "time max", "Mu1", "Mu2", "Area"]
            self.tablemodel.setHeader(header)

            #clean prevoius plot
            self.ax.cla()

            signal = []
            time = []
            f = open(self.lineEdit.text())
            for line in f:
                v = str.split(line.strip(), "\t")
                if len(v) == 2:
                    time.append(float(v[0]))
                    signal.append(float(v[1]))
                else:
                    continue
            f.close()

            #plot entire chromatogram
            self.ax.plot(time, signal, "b")

            #Analyse peaks
            h = self.peakthreshold.value()
            k = self.windowsize.value()

            chrom = ChromAnalysis(time, signal, k, h)
            peaks = chrom.getPeaks()
            peaklst = chrom.peaksplit(peaks)

            nleftpnt = self.leftpoints.value()
            nrightpnt = self.rightpoints.value()
            pn = 1
            for i in range(len(peaklst)):
                time_ = []
                signal_ = []
                #print "-"*10
                chrom.addLeftNpoints(peaklst[i], nleftpnt)
                chrom.addRighNpoints(peaklst[i], nrightpnt)
                for row in peaklst[i]:
                    #print row[0], row[1]
                    time_.append(row[0])
                    signal_.append(row[1])

                if len(time_) > 15:
                    # fill peak detected!
                    self.ax.fill(time_, signal_, zorder=10)
                    self.ax.grid(True, zorder=5)

                    u1 = chrom.Mu1CentralMoment(time_, signal_)
                    u2 = chrom.Mu2CentralMoment(time_, signal_, u1)

                    area = chrom.integrate(signal_, 3)
                    self.tablemodel.addRow([pn, len(time_), min(time_), max(time_), u1, u2, area])
                    pn += 1

            #self.ax.grid(True, zorder=5)
            plt.xlabel('Time')
            plt.ylabel('Signal')
            self.canvas.draw()
            return
        else:
            return


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ChromAnalyzer()
    form.show()
    app.exec()

if __name__ == '__main__':
    main()
