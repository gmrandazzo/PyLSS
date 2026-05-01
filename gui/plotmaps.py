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
@package plotselectivitymap.py

plotselectivitymap.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve October 2016
'''

from PyQt6 import QtCore, QtGui, QtWidgets
import sys

from .gui_plotmaps import Ui_PlotMaps

from pylss.optseparation import *

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import random

class PlotMaps(QtWidgets.QDialog, Ui_PlotMaps):
    def __init__(self, modellst, type="sel", parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)

        # Create the plot
        #self.figure = plt.figure()
        self.figure, self.axes = plt.subplots(nrows=3, ncols=1)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()
        # set the layout
        layout = QtWidgets.QVBoxLayout()
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
        ax.plot(data, '*-')
        self.canvas.draw()


    def plotresolutionmap(self):
        plt.cla()
        indx = self.modelBox.currentIndex()
        if indx >= 0 and indx < len(self.modellst):
          lss = self.modellst[indx].lss
          flow_sofware = self.modellst[indx].flow
          v_m = self.modellst[indx].v_m
          v_d = self.modellst[indx].v_d

          opt = OptSep(v_m, v_d, flow_sofware, lss)
          [gcondlst, reslst, trlst] = opt.getResMapPlot("lss", float(flow_sofware), g_start_min=0.00, g_start_max=0.30, g_stop_min=0.50, g_stop_max=1.0, time_grad_min=2, time_grad_max=60)

          #Plot resolution map
          x_list = []
          y_gsteepness_list = []
          y_final_b_list = []
          y_tg_list = []
          z_list = []
          for i in range(len(gcondlst)):
              x_list.append(float(gcondlst[i][0])*100)
              y_gsteepness_list.append(float((gcondlst[i][1]-gcondlst[i][0])/gcondlst[i][2])) # alpha
              y_final_b_list.append(float(gcondlst[i][1])*100) # final b
              y_tg_list.append(float(gcondlst[i][2])) # tg
              z_list.append(float(gcondlst[i][-1])) # lowestrs

          x = np.asarray(x_list)
          y_gsteepness = np.asarray(y_gsteepness_list)
          y_final_b = np.asarray(y_final_b_list)
          y_tg = np.asarray(y_tg_list)
          z = np.asarray(z_list)

          if x.size == 0:
              print("No valid conditions found for the map.")
              return

          # Set up a regular grid of interpolation points
          npoints = 500
          xi, yi_gsteepness = np.linspace(x.min(), x.max(), npoints), np.linspace(y_gsteepness.min(), y_gsteepness.max(), npoints)
          xi_grid_gst, yi_grid_gst = np.meshgrid(xi, yi_gsteepness)

          xi_fb, yi_final_b = np.linspace(x.min(), x.max(), npoints), np.linspace(y_final_b.min(), y_final_b.max(), npoints)
          xi_grid_fb, yi_grid_fb = np.meshgrid(xi_fb, yi_final_b)

          xi_tg, yi_tg = np.linspace(x.min(), x.max(), npoints), np.linspace(y_tg.min(), y_tg.max(), npoints)
          xi_grid_tg, yi_grid_tg = np.meshgrid(xi_tg, yi_tg)

          # Interpolate
          zi_gsteepness = scipy.interpolate.griddata((x, y_gsteepness), z, (xi_grid_gst, yi_grid_gst), method='linear')
          zi_final_b = scipy.interpolate.griddata((x, y_final_b), z, (xi_grid_fb, yi_grid_fb), method='linear')
          zi_tg = scipy.interpolate.griddata((x, y_tg), z, (xi_grid_tg, yi_grid_tg), method='linear')

          im = self.axes.flat[0].imshow(zi_gsteepness, vmin=z.min(), vmax=z.max(), origin='lower', extent=[x.min(), x.max(), y_gsteepness.min(), y_gsteepness.max()], aspect='auto')
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
          x_list = []
          y_gsteepness_list = []
          y_final_b_list = []
          y_tg_list = []
          z_list = []
          for i in range(len(gcondlst)):
              x_list.append(float(gcondlst[i][0])*100)
              y_gsteepness_list.append(float((gcondlst[i][1]-gcondlst[i][0])/gcondlst[i][2]+1)) # alpha
              y_final_b_list.append(float(gcondlst[i][1])*100) # final b
              y_tg_list.append(float(gcondlst[i][2])) # tg
              z_list.append(float(gcondlst[i][-1]))

          x = np.asarray(x_list)
          y_gsteepness = np.asarray(y_gsteepness_list)
          y_final_b = np.asarray(y_final_b_list)
          y_tg = np.asarray(y_tg_list)
          z = np.asarray(z_list)

          if x.size == 0:
              print("No valid conditions found for the map.")
              return

          # Set up a regular grid of interpolation points
          npoints = 500
          xi, yi_gsteepness = np.linspace(x.min(), x.max(), npoints), np.linspace(y_gsteepness.min(), y_gsteepness.max(), npoints)
          xi_grid_gst, yi_grid_gst = np.meshgrid(xi, yi_gsteepness)

          xi_fb, yi_final_b = np.linspace(x.min(), x.max(), npoints), np.linspace(y_final_b.min(), y_final_b.max(), npoints)
          xi_grid_fb, yi_grid_fb = np.meshgrid(xi_fb, yi_final_b)

          xi_tg, yi_tg = np.linspace(x.min(), x.max(), npoints), np.linspace(y_tg.min(), y_tg.max(), npoints)
          xi_grid_tg, yi_grid_tg = np.meshgrid(xi_tg, yi_tg)

          # Interpolate
          zi_gsteepness = scipy.interpolate.griddata((x, y_gsteepness), z, (xi_grid_gst, yi_grid_gst), method='linear')
          zi_final_b = scipy.interpolate.griddata((x, y_final_b), z, (xi_grid_fb, yi_grid_fb), method='linear')
          zi_tg = scipy.interpolate.griddata((x, y_tg), z, (xi_grid_tg, yi_grid_tg), method='linear')

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
