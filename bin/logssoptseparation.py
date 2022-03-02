#!/usr/bin/env python

import os
import sys

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.interpolate

path = None
try:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
except NameError:
    path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
path += "/pylss"
if not path in sys.path:
    sys.path.insert(1, path)
del path

from ssengine import *
from optseparation import *

def main():
    """ Main function """
    if len(sys.argv) != 2:
        print("Usage: %s <input file>" % (sys.argv[0]))
        print("\nInput File Format\n:")
        print("Column Lenght: 150")
        print("Column Diamter: 2.1")
        print("Column Porosity: 0.7")
        print("Time zero: 0.969 #to avoid the column parameters...")
        print("Dwell Volume: 0.9")
        print("%B Start: 5")
        print("%B End: 95")
        print("Flow Rate: 0.25")
        print("Time Gradient 1: 5")
        print("Time Gradient 2: 15")
        print("END")
        print("2.32\t4.64")
        print("3.42\t6.86")
        print("3.42\t6.86")
        print("....................")
        print("....................")
        print("....................\n")
    else:
        fi = open(sys.argv[1], "r")
        logkw_s_tab = []
        c_length = c_diameter = c_porosity = t0 = v_d = flow = None
        init_B = []
        final_B = []
        tg = []
        for line in fi:
            if "Column Lenght" in line:
                c_length = str.split(line.strip(), ":")[-1].strip()
            elif "Column Diamter" in line:
                c_diameter = str.split(line.strip(), ":")[-1].strip()
            elif "Column Porosity" in line:
                c_porosity = str.split(line.strip(), ":")[-1].strip()
            elif "Dwell Volume" in line:
                v_d = str.split(line.strip(), ":")[-1].strip()
            elif "Flow Rate" in line:
                flow = str.split(line.strip(), ":")[-1].strip()
            elif "Gradient " in line:
                v = str.split(line.strip(), ":")[-1].strip()
                v = str.split(v, " ")
                tg.append(float(v[0]))
                init_B.append(float(v[1])/100.)
                final_B.append(float(v[2])/100.)
            elif "Time zero" in line:
                t0 = str.split(line.strip(), ":")[-1].strip()
            elif "Temperature:" in line:
                continue
            elif "Plate Numbers" in line:
                continue
            else:
                logssmol = SSGenerator(c_length, c_diameter, c_porosity, t0, v_d, flow)
                var = str.split(line.strip(), ";")
                tr = []
                for item in var:
                    tr.append(float(item))
                lss_logkw, lss_s = logssmol.getlogssparameters(tr, tg, init_B, final_B)
                logkw_s_tab.append([lss_logkw, lss_s])
        fi.close()
        opt = OptSep(float(t0)*float(flow), v_d, flow, logkw_s_tab)
        #[phi, tr] = opt.getisoconditions()
        #print("Best Percentage of Organic Solvent: %.2f" % (phi)
        #print("Compounds will elute in this manner"
        #for time in tr:
    #        print("%.2f" % (time)
#        print("_"*20

        #[gcond, tr, Rs] = opt.getloggradientconditions(10,20)

        #[gconds, rs] = opt.getplotgradientconditions()
        #indx = rs.index(max(rs))
        #gcond = gconds[indx]
        #tr = []
        #Rs = max(rs)

        #print("Best Gradient Conditions with Rs: %f" % (Rs)
        #print("init B: %f\nfinal B: %f\nTime Gradient: %f\n" % (gcond[0], gcond[1], gcond[2])
        #for time in tr:
        #    print("%.2f" % (time)

        [gcondlst, sellst, trlst] = opt.getlogssselMapPlot(float(flow), g_start_min=0.00, g_start_max=0.10, g_stop_min=0.90, g_stop_max=1.0, time_grad_min=5, time_grad_max=30)
        #Plot selectivity map
        x = []
        y_alpha = []
        y_final_b = []
        y_tg = []
        z = []
        for i in range(len(gcondlst)):
            #gcondlst.append([init_b, final_b, tg, self.flow, lowest_alpha])
            x.append(float(gcondlst[i][0])*100)
            y_alpha.append(float((gcondlst[i][1]-gcondlst[i][0])/log(gcondlst[i][2]+1))) # alpha
            y_final_b.append(float(gcondlst[i][1])*100) # final b
            y_tg.append(float(gcondlst[i][2])) # tg
            z.append(float(gcondlst[i][-1]))

        x = np.asarray(x)
        y_alpha = np.asarray(y_alpha)
        y_final_b = np.asarray(y_final_b)
        y_tg = np.asarray(y_tg)
        z = np.asarray(z)

        # Set up a regular grid of interpolation points
        npoints = 1000
        xi, yi_alpha = np.linspace(x.min(), x.max(), npoints), np.linspace(y_alpha.min(), y_alpha.max(), npoints)
        xi, yi_alpha = np.meshgrid(xi, yi_alpha)

        xi, yi_final_b = np.linspace(x.min(), x.max(), npoints), np.linspace(y_final_b.min(), y_final_b.max(), npoints)
        xi, yi_final_b = np.meshgrid(xi, yi_final_b)

        xi, yi_tg = np.linspace(x.min(), x.max(), npoints), np.linspace(y_tg.min(), y_tg.max(), npoints)
        xi, yi_tg = np.meshgrid(xi, yi_tg)

        # Interpolate
        #rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
        #zi = rbf(xi, yi)

        zi_alpha = scipy.interpolate.griddata((x, y_alpha), z, (xi, yi_alpha), method='linear')
        zi_final_b = scipy.interpolate.griddata((x, y_final_b), z, (xi, yi_final_b), method='linear')
        zi_tg = scipy.interpolate.griddata((x, y_tg), z, (xi, yi_tg), method='linear')


        #f, axarr = plt.subplots(3, sharex=True)
        fig, axes = plt.subplots(nrows=3, ncols=1)

        im = axes.flat[0].imshow(zi_alpha, vmin=z.min(), vmax=z.max(), origin='lower',
                  extent=[x.min(), x.max(), y_alpha.min(), y_alpha.max()], aspect='auto')
        axes.flat[0].set_xlabel('Initial B (%)')
        axes.flat[0].set_ylabel('Alpha')

        im = axes.flat[1].imshow(zi_final_b, vmin=z.min(), vmax=z.max(), origin='lower',
                  extent=[x.min(), x.max(), y_final_b.min(), y_final_b.max()],  aspect='auto')

        axes.flat[1].set_xlabel('Initial B (%)')
        axes.flat[1].set_ylabel('Final B (%)')

        im = axes.flat[2].imshow(zi_tg, vmin=z.min(), vmax=z.max(), origin='lower',
                  extent=[x.min(), x.max(), y_tg.min(), y_tg.max()], aspect='auto')

        axes.flat[2].set_xlabel('Initial B (%)')
        axes.flat[2].set_ylabel('Time gradient (min)')

        fig.colorbar(im, ax=axes.ravel().tolist())

        #plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
        #          extent=[x.min(), x.max(), y.min(), y.max()], cmap=plt.get_cmap("bwr"), aspect='auto')
        #plt.scatter(x, y, c=z)
        #plt.colorbar()

        plt.show()

if __name__ == "__main__":
    main()
