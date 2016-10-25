'''
@package plotselectivitymap.py

plotselectivitymap.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve October 2016
'''

from PyQt4 import *
from PyQt4 import *
import sys

from gui_plotmaps import Ui_PlotMaps

from optseparation import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import random

class PlotMaps(QtGui.QDialog, Ui_PlotMaps):
    def __init__(self, modellst, type="sel", parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)

        # Create the plot
        #self.figure = plt.figure()
        self.figure, self.axes = plt.subplots(nrows=3, ncols=1)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()
        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.plotterBox.setLayout(layout)
        self.closeButton.clicked.connect(self.close_)

        if type == "sel":
            self.modelBox.currentIndexChanged.connect(self.plotselectivitymap)
        else:
            self.modelBox.currentIndexChanged.connect(self.plotresolutionmap)

        self.modellst = modellst
        for model in self.modellst:
            self.modelBox.addItem(model.modname)

    def close_(self):
        self.reject()

    def plotchromatogram(self):
        ''' plot some random stuff '''
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(data, '*-')
        self.canvas.draw()


    def plotresolutionmap(self):
        indx = self.modelBox.currentIndex()
        if indx >= 0 and indx < len(self.modellst):
          lss = self.modellst[indx].lss
          flow_sofware = self.modellst[indx].flow
          v_m = self.modellst[indx].v_m
          v_d = self.modellst[indx].v_d
          c_particle = self.modellst[indx].c_particle
          c_length = self.modellst[indx].c_length

          opt = OptSep(v_m, v_d, flow_sofware, lss)
          opt.c_particle = c_particle
          opt.c_length = c_length
          [gcondlst, reslst, trlst] =  opt.getResMapPlot("lss", float(flow_sofware), g_start_min=0.00, g_start_max=0.30, g_stop_min=0.50, g_stop_max=1.0, time_grad_min=2, time_grad_max=60)

          #Plot resolution map
          x = []
          y_gsteepness = []
          y_final_b = []
          y_tg = []
          z = []
          for i in range(len(gcondlst)):
              #gcondlst.append([init_b, final_b, tg, self.flow, lowest_alpha])
              x.append(float(gcondlst[i][0])*100)
              y_gsteepness.append(float((gcondlst[i][1]-gcondlst[i][0])/gcondlst[i][2])) # alpha
              y_final_b.append(float(gcondlst[i][1])*100) # final b
              y_tg.append(float(gcondlst[i][2])) # tg
              z.append(float(gcondlst[i][-1]))

          x = np.asarray(x)
          y_gsteepness = np.asarray(y_gsteepness)
          y_final_b = np.asarray(y_final_b)
          y_tg = np.asarray(y_tg)
          z = np.asarray(z)

          # Set up a regular grid of interpolation points
          npoints = 500
          xi, yi_gsteepness  = np.linspace(x.min(), x.max(), npoints), np.linspace(y_gsteepness .min(), y_gsteepness .max(), npoints)
          xi, yi_gsteepness  = np.meshgrid(xi, yi_gsteepness )

          xi, yi_final_b = np.linspace(x.min(), x.max(), npoints), np.linspace(y_final_b.min(), y_final_b.max(), npoints)
          xi, yi_final_b = np.meshgrid(xi, yi_final_b)

          xi, yi_tg = np.linspace(x.min(), x.max(), npoints), np.linspace(y_tg.min(), y_tg.max(), npoints)
          xi, yi_tg = np.meshgrid(xi, yi_tg)

          # Interpolate
          #rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
          #zi = rbf(xi, yi)

          zi_gsteepness = scipy.interpolate.griddata((x, y_gsteepness ), z, (xi, yi_gsteepness ), method='linear')
          zi_final_b = scipy.interpolate.griddata((x, y_final_b), z, (xi, yi_final_b), method='linear')
          zi_tg = scipy.interpolate.griddata((x, y_tg), z, (xi, yi_tg), method='linear')


          #f, axarr = plt.subplots(3, sharex=True)
          #axes = self.figure.add_subplot(nrows=3, ncols=1)

          im = self.axes.flat[0].imshow(zi_gsteepness , vmin=z.min(), vmax=z.max(), origin='lower', extent=[x.min(), x.max(), y_gsteepness .min(), y_gsteepness .max()], aspect='auto')
          self.axes.flat[0].set_xlabel('Initial B (%)')
          self.axes.flat[0].set_ylabel('Gradient steepness')

          im = self.axes.flat[1].imshow(zi_final_b, vmin=z.min(), vmax=z.max(), origin='lower',
                    extent=[x.min(), x.max(), y_final_b.min(), y_final_b.max()],  aspect='auto')

          self.axes.flat[1].set_xlabel('Initial B (%)')
          self.axes.flat[1].set_ylabel('Final B (%)')

          im = self.axes.flat[2].imshow(zi_tg, vmin=z.min(), vmax=z.max(), origin='lower',
                    extent=[x.min(), x.max(), y_tg.min(), y_tg.max()], aspect='auto')

          self.axes.flat[2].set_xlabel('Initial B (%)')
          self.axes.flat[2].set_ylabel('Time gradient (min)')

          self.figure.colorbar(im, ax=self.axes.ravel().tolist())
          self.canvas.draw()


    def plotselectivitymap(self):
        plt.cla()
        indx = self.modelBox.currentIndex()
        if indx >= 0 and indx < len(self.modellst):
          lss = self.modellst[indx].lss
          flow_sofware = self.modellst[indx].flow
          v_m = self.modellst[indx].v_m
          v_d = self.modellst[indx].v_d

          opt = OptSep(v_m, v_d, flow_sofware, lss)
          [gcondlst, sellst, trlst] = opt.getSelMapPlot("lss", float(flow_sofware), g_start_min=0.00, g_start_max=0.30, g_stop_min=0.50, g_stop_max=1.0, time_grad_min=2, time_grad_max=60)

          #Plot selectivity map
          x = []
          y_gsteepness = []
          y_final_b = []
          y_tg = []
          z = []
          for i in range(len(gcondlst)):
              #gcondlst.append([init_b, final_b, tg, self.flow, lowest_alpha])
              x.append(float(gcondlst[i][0])*100)
              y_gsteepness.append(float((gcondlst[i][1]-gcondlst[i][0])/gcondlst[i][2]+1)) # alpha
              y_final_b.append(float(gcondlst[i][1])*100) # final b
              y_tg.append(float(gcondlst[i][2])) # tg
              z.append(float(gcondlst[i][-1]))

          x = np.asarray(x)
          y_gsteepness = np.asarray(y_gsteepness)
          y_final_b = np.asarray(y_final_b)
          y_tg = np.asarray(y_tg)
          z = np.asarray(z)

          # Set up a regular grid of interpolation points
          npoints = 500
          xi, yi_gsteepness = np.linspace(x.min(), x.max(), npoints), np.linspace(y_gsteepness.min(), y_gsteepness.max(), npoints)
          xi, yi_gsteepness = np.meshgrid(xi, yi_gsteepness)

          xi, yi_final_b = np.linspace(x.min(), x.max(), npoints), np.linspace(y_final_b.min(), y_final_b.max(), npoints)
          xi, yi_final_b = np.meshgrid(xi, yi_final_b)

          xi, yi_tg = np.linspace(x.min(), x.max(), npoints), np.linspace(y_tg.min(), y_tg.max(), npoints)
          xi, yi_tg = np.meshgrid(xi, yi_tg)

          # Interpolate
          #rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
          #zi = rbf(xi, yi)

          zi_gsteepness = scipy.interpolate.griddata((x, y_gsteepness), z, (xi, yi_gsteepness), method='linear')
          zi_final_b = scipy.interpolate.griddata((x, y_final_b), z, (xi, yi_final_b), method='linear')
          zi_tg = scipy.interpolate.griddata((x, y_tg), z, (xi, yi_tg), method='linear')


          #f, axarr = plt.subplots(3, sharex=True)
          #axes = self.figure.add_subplot(nrows=3, ncols=1)


          im = self.axes.flat[0].imshow(zi_gsteepness, vmin=z.min(), vmax=z.max(), origin='lower',
                    extent=[x.min(), x.max(), y_gsteepness.min(), y_gsteepness.max()], aspect='auto')
          self.axes.flat[0].set_xlabel('Initial B (%)')
          self.axes.flat[0].set_ylabel('Gradient steepness')

          im = self.axes.flat[1].imshow(zi_final_b, vmin=z.min(), vmax=z.max(), origin='lower',
                    extent=[x.min(), x.max(), y_final_b.min(), y_final_b.max()],  aspect='auto')

          self.axes.flat[1].set_xlabel('Initial B (%)')
          self.axes.flat[1].set_ylabel('Final B (%)')

          im = self.axes.flat[2].imshow(zi_tg, vmin=z.min(), vmax=z.max(), origin='lower',
                    extent=[x.min(), x.max(), y_tg.min(), y_tg.max()], aspect='auto')

          self.axes.flat[2].set_xlabel('Initial B (%)')
          self.axes.flat[2].set_ylabel('Time gradient (min)')

          self.figure.colorbar(im, ax=self.axes.ravel().tolist())
          self.canvas.draw()
