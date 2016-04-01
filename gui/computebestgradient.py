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

        logkw_s_tab = self.models[indx].lss
        v_m = self.models[indx].v_m
        v_d = self.models[indx].v_d
        flow = self.models[indx].flow

        opt = OptSep(v_m, v_d, flow, logkw_s_tab)
        best_gcond, tr, rs_avg = opt.getgradientconditions(self.tr_min.value(), self.tr_max.value())

        init_b = best_gcond[0]
        final_b = best_gcond[1]
        tg = best_gcond[2]
        flow = best_gcond[3]

        # Constant flow!
        flow_min = flow-(flow*0.2)
        flow_max = flow+(flow*0.2)
        grad_start_min = init_b-(init_b*0.2)
        grad_stop_min = init_b+(init_b*0.2)
        grad_start_max = final_b-(final_b*0.2)
        grad_stop_max = final_b+(final_b*0.2)

        tg_min = tg-(tg*0.2)
        tg_max = tg+(tg*0.2)

        [gcondlst, rslst, trlst] = opt.getplotgradientconditions(flow_min, flow_max, grad_start_min, grad_start_max, grad_stop_min, grad_stop_max, tg_min, tg_max)

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
            Y.append(row[0])
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
        ax.set_xlabel('Gradient slope %%/min')
        ax.set_ylabel('%%initial of gradient')
        ax.set_zlabel('Resolution')

        self.canvas.draw()

        best = Z.index(max(Z))
        self.doubleSpinBox_5.setValue(rs_avg)
        self.doubleSpinBox_1.setValue(init_b*100)
        self.doubleSpinBox_2.setValue(final_b*100)
        self.doubleSpinBox_3.setValue(tg)
        self.doubleSpinBox_4.setValue(flow)
