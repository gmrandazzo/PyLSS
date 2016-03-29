'''
@package computebestgradient.py

computebestgradient.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

from PyQt4 import *
from PyQt4 import *
import sys

from gui_computebestgradient import Ui_ComputeBestGradient

from optseparation import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np


class ComputeBestGradient(QtGui.QDialog, Ui_ComputeBestGradient):
    def __init__(self, models, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.closeButton.clicked.connect(self.close_)
        self.calculateButton.clicked.connect(self.calculate)
        self.models = models
        for model in self.models:
            self.modelBox.addItem(model.modname)

        # Create the plot
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()
        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.plotterBox.setLayout(layout)

    def close_(self):
        self.reject()

    def calculate(self):
        indx = self.modelBox.currentIndex()
        flow_min = self.flowMinSpinBox.value()
        flow_max = self.flowMaxSpinBox.value()
        grad_start_min = self.GStartMinSpinBox.value()/100.
        grad_start_max = self.GSartMaxSpinBox.value()/100.
        grad_stop_min = self.GStoptMinSpinBox.value()/100.
        grad_stop_max = self.GStopMaxSpinBox.value()/100.
        time_min = self.timeMinSpinBox.value()
        time_max = self.timeMaxSpinBox.value()

        logkw_s_tab = self.models[indx].lss
        v_m = self.models[indx].v_m
        v_d = self.models[indx].v_d

        opt = OptSep(v_m, v_d, flow_min, logkw_s_tab)
        [gcondlst, rslst, trlst] = opt.getplotgradientconditions(flow_min, flow_max, grad_start_min, grad_start_max, grad_stop_min, grad_stop_max, time_min, time_max)

        #gcondlst.append([init_b, final_b, tg, flow])
        #rslst.append(small_rs)
        plt.clf()
        ax = self.figure.gca(projection='3d')
        #X = np.arange(-5, 5, 0.25)
        #Y = np.arange(-5, 5, 0.25)
        X = []
        Y = []
        Z = []
        for i in range(len(gcondlst)):
            row = gcondlst[i]
            X.append(100 * ((row[1]-row[0])/row[2]))
            Y.append(row[3])
            if rslst[i] == -9999:
                    Z.append(0)
            else:
                Z.append(rslst[i])

        t = Z
        scatterplot = ax.scatter(X, Y, Z, c=t, cmap='jet', marker='o')
        #X, Y = np.meshgrid(X, Y)
        #R = np.sqrt(X**2 + Y**2)
        #Z = np.sin(R)
        #surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
        #                       linewidth=0, antialiased=False)

        self.figure.colorbar(scatterplot, shrink=0.5, aspect=5).remove()
        self.figure.colorbar(scatterplot, shrink=0.5, aspect=5)

        ax.hold(False)
        ax.set_xlabel('Gradient Steepness')
        ax.set_ylabel('Flow rate')
        ax.set_zlabel('Rs')

        self.canvas.draw()

        best = Z.index(max(Z))
        self.doubleSpinBox_5.setValue(((gcondlst[best][1]-gcondlst[best][0])/gcondlst[best][2]) *100)
        self.doubleSpinBox_1.setValue(gcondlst[best][0]*100)
        self.doubleSpinBox_2.setValue(gcondlst[best][1]*100)
        self.doubleSpinBox_3.setValue(gcondlst[best][2])
        self.doubleSpinBox_4.setValue(gcondlst[best][3])
