'''
@package computebestgradient.py

computebestgradient.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve February 2015
'''

from PyQt5 import *
from PyQt5 import *
import sys

from gui_automaticelutionwindowstretching import Ui_AutomaticElutionWindowStretching

from optseparation import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np


class AutomaticElutionWindowStretching(QtWidgets.QDialog, Ui_AutomaticElutionWindowStretching):
    def __init__(self, modellst, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.closeButton.clicked.connect(self.close_)
        self.calculateButton.clicked.connect(self.calculate)
        self.modellst = modellst
        for model in self.modellst:
            self.modelBox.addItem(model.modname)

    def close_(self):
        self.reject()

    def calculate(self):
        indx = self.modelBox.currentIndex()
        logkw_s_tab = self.modellst[indx].lss
        v_m = self.modellst[indx].v_m
        v_d = self.modellst[indx].v_d
        flow = self.modellst[indx].flow

        if indx >= 0 and indx < len(self.modellst):
            #predict the retention time for each compound
            # between self.tr_min.value(), self.tr_max.value()
            lss = self.modellst[indx].lss
            opt = OptSep(v_m, v_d, flow, lss)
            gcond = opt.getAutomaticElutionWindowStretching("lss", flow, g_start_min=0.00, g_start_max=0.3, g_stop_min=0.5, g_stop_max=1.0, time_grad_min= self.tr_min.value(), time_grad_max=self.tr_max.value())
            self.doubleSpinBox_6.setValue(gcond[0]*100)
            self.doubleSpinBox_7.setValue(gcond[1]*100)
            self.doubleSpinBox_8.setValue(gcond[2])
