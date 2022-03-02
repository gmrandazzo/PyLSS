#!/usr/bin/env python

import os
import sys

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
from plotengine import *

def main():
    """ Main function """
    if len(sys.argv) != 3:
        print("Usage: %s <input file Temperature 1> <input file Temperature 2> where t2 > t1" % (sys.argv[0]))
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
        logkw_s_tab_t1 = []
        t1 = None
        c_length = c_diameter = c_particle = t0 = v_d = flow = None
        init_B = []
        final_B = []
        tg = []
        for line in fi:
            if "Column Length" in line:
                c_length = float(str.split(line.strip(), ":")[-1].strip())
            elif "Column Diamter" in line:
                c_diameter = float(str.split(line.strip(), ":")[-1].strip())
            elif "Column Particle" in line:
                c_particle = float(str.split(line.strip(), ":")[-1].strip())
            elif "Dwell Volume" in line:
                v_d = float(str.split(line.strip(), ":")[-1].strip())
            elif "Flow Rate" in line:
                flow = float(str.split(line.strip(), ":")[-1].strip())
            elif "Gradient " in line:
                v = str.split(line.strip(), ":")[-1].strip()
                v = str.split(v, " ")
                tg.append(float(v[0]))
                init_B.append(float(v[1])/100.)
                final_B.append(float(v[2])/100.)
            elif "Time zero" in line:
                t0 = float(str.split(line.strip(), ":")[-1].strip())
            elif "Temperature" in line:
                t1 = float(str.split(line.strip(), ":")[-1].strip())
            elif "Plate Numbers" in line:
                continue
            else:
                var = str.split(line.strip(), ";")
                if len(var) == len(tg):
                    lssmol = SSGenerator(c_length, c_diameter, c_particle, t0, v_d, flow)
                    tr = []
                    for item in var:
                        tr.append(float(item))
                    lss_logkw, lss_s = lssmol.getlssparameters(tr, tg, init_B, final_B)
                    logkw_s_tab_t1.append([lss_logkw, lss_s])
                else:
                    continue
        fi.close()

        fi = open(sys.argv[2], "r")
        logkw_s_tab_t2 = []
        t2 =  None
        c_length = c_diameter = c_particle = t0 = v_d = flow = None
        init_B = []
        final_B = []
        tg = []
        for line in fi:
            if "Column Length" in line:
                c_length = float(str.split(line.strip(), ":")[-1].strip())
            elif "Column Diamter" in line:
                c_diameter = float(str.split(line.strip(), ":")[-1].strip())
            elif "Column Particle" in line:
                c_particle = float(str.split(line.strip(), ":")[-1].strip())
            elif "Dwell Volume" in line:
                v_d = float(str.split(line.strip(), ":")[-1].strip())
            elif "Flow Rate" in line:
                flow = float(str.split(line.strip(), ":")[-1].strip())
            elif "Gradient " in line:
                v = str.split(line.strip(), ":")[-1].strip()
                v = str.split(v, " ")
                tg.append(float(v[0]))
                init_B.append(float(v[1])/100.)
                final_B.append(float(v[2])/100.)
            elif "Time zero" in line:
                t0 = float(str.split(line.strip(), ":")[-1].strip())
            elif "Temperature" in line:
                t2 = float(str.split(line.strip(), ":")[-1].strip())
            elif "Plate Numbers" in line:
                continue
            else:
                var = str.split(line.strip(), ";")
                if len(var) == len(tg):
                    lssmol = SSGenerator(c_length, c_diameter, c_particle, t0, v_d, flow)
                    tr = []
                    for item in var:
                        tr.append(float(item))
                    lss_logkw, lss_s = lssmol.getlssparameters(tr, tg, init_B, final_B)
                    logkw_s_tab_t2.append([lss_logkw, lss_s])
                else:
                    continue
        fi.close()

        # Betweent t1 and t2 there is a line which give us access to all the
        # gamma of logkw and s.
        Rslst = []
        gcondlst = []
        trlst = []
        temps = []

        N = (float(c_length)*10000.)/(3.4*float(c_particle))

        for i in range(len(logkw_s_tab_t1)):
            mlogk = (logkw_s_tab_t2[i][0]-logkw_s_tab_t1[i][0]) / (t2-t1)
            qlogk = (t2*logkw_s_tab_t1[i][0] - t1*logkw_s_tab_t2[i][0]) / (t2-t1)
            mS = (logkw_s_tab_t2[i][1]-logkw_s_tab_t1[i][1]) / (t2-t1)
            qS = (t2*logkw_s_tab_t1[i][1] - t1*logkw_s_tab_t2[i][1]) / (t2-t1)
            print(mlogk, qlogk, -1*mS, -1*qS) # -1 for the hplc simulatir application

        fo = open("experimental_design.txt", "w")
        fo.write("Experiment name;Start B;End B;gradient time;temperature;int1-2;int1-3;int1-4;int2-3;int2-4;int3-4;1^2;2^2;3^2;4^2;selectivity\n")
        r = [-2.19, -1, 0, 1, 2.19]
        y = []
        tstep = (t2-t1)/4.
        trstep = (15-5)/4.
        init_b = list(drange(0.0, 0.20, 0.05))
        final_b = list(drange(0.80, 1.0, 0.05))
        tg = list(drange(5, 15, trstep))
        t = list(drange(t1, t2, tstep))


        lssparam = []
        for q in range(len(logkw_s_tab_t1)):
            mlogk = (logkw_s_tab_t2[q][0]-logkw_s_tab_t1[q][0]) / (t2-t1)
            qlogk = (t2*logkw_s_tab_t1[q][0] - t1*logkw_s_tab_t2[q][0]) / (t2-t1)

            mS = (logkw_s_tab_t2[q][1]-logkw_s_tab_t1[i][1]) / (t2-t1)
            qS = (t2*logkw_s_tab_t1[q][1] - t1*logkw_s_tab_t2[q][1]) / (t2-t1)
            lssparam.append([(mlogk*25 +qlogk), (mS*25 +qS)])

            trpred = lssmol.rtpred(lssparam[-1][0], lssparam[-1][1], 5, 0.05, 0.95, t0, v_d/flow)
            print(trpred)

        p = 0
        for i in range(len(init_b)):
            for j in range(len(final_b)):
                for k in range(len(tg)):
                    for m in range(len(t)):
                        lssparam = []
                        for q in range(len(logkw_s_tab_t1)):
                            mlogk = (logkw_s_tab_t2[q][0]-logkw_s_tab_t1[q][0]) / (t2-t1)
                            qlogk = (t2*logkw_s_tab_t1[q][0] - t1*logkw_s_tab_t2[q][0]) / (t2-t1)

                            mS = (logkw_s_tab_t2[q][1]-logkw_s_tab_t1[i][1]) / (t2-t1)
                            qS = (t2*logkw_s_tab_t1[q][1] - t1*logkw_s_tab_t2[q][1]) / (t2-t1)
                            lssparam.append([(mlogk*t[m] +qlogk), (mS*t[m] +qS)])
                        lstcc, lowest_alpha = get_lss_gradient_critical_selectivity(5, 1.8, init_b[i], final_b[j], tg[k], flow, t0*flow, v_d, lssparam , crit_alpha=0.9)

                        if lowest_alpha == None:
                            fo.write("Experiment%d;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f\n" % (p, r[i],r[j],r[k],r[m],r[i]*r[j],r[i]*r[k],r[i]*r[m],r[j]*r[k],r[j]*r[m],r[k]*r[m],r[i]**2,r[j]**2,r[k]**2,r[m]**2,0.))
                        else:
                            fo.write("Experiment%d;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f\n" % (p, r[i],r[j],r[k],r[m],r[i]*r[j],r[i]*r[k],r[i]*r[m],r[j]*r[k],r[j]*r[m],r[k]*r[m],r[i]**2,r[j]**2,r[k]**2,r[m]**2,lowest_alpha))
                        p+=1
        fo.close()

        for t in drange(t1, t2+1, 5):
            print("Temperature %f" % (t))
            temps.append(t)
            logkw_s_tab = []
            for i in range(len(logkw_s_tab_t1)):
                mlogk = (logkw_s_tab_t2[i][0]-logkw_s_tab_t1[i][0]) / (t2-t1)
                qlogk = (t2*logkw_s_tab_t1[i][0] - t1*logkw_s_tab_t2[i][0]) / (t2-t1)
                mS = (logkw_s_tab_t2[i][1]-logkw_s_tab_t1[i][1]) / (t2-t1)
                qS = (t2*logkw_s_tab_t1[i][1] - t1*logkw_s_tab_t2[i][1]) / (t2-t1)
                logkw_s_tab.append([(mlogk*t +qlogk), (mS*t +qS)])
            opt = OptSep(float(t0)*float(flow), v_d, flow, logkw_s_tab)
            opt.plate = float(N)

            [gcondlst, sellst, trlst] = opt.getSelMapPlot("lss", float(flow), g_start_min=0.00, g_start_max=0.10, g_stop_min=0.70, g_stop_max=1.0, time_grad_min=5, time_grad_max=12)
            #getSelMapPlot("lss", flow=0.3, g_start_min=1.00, g_start_max=0.1, g_stop_min=0.7, g_stop_max=1.0, time_grad_min=4, time_grad_max=12)
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
            axes.flat[0].set_ylabel('Gradient steepness')

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

            """
            [gcond, tr, Rs] = opt.getgradientconditions(5,15)
            Rslst.append(Rs)
            gcondlst.append(gcond)
            trlst.append(tr)
        bestrs = Rslst.index(max(Rslst))
        print("Best Gradient Conditions Rs: %f at temperature %f" % (Rslst[bestrs], temps[bestrs])
        gcond = gcondlst[bestrs]
        print("init B: %f\nfinal B: %f\nTime Gradient:%f\n" % (gcond[0], gcond[1], gcond[2])
        for time in tr:
            print("%.2f" % (time)
            """
            #[gconds, rs, trs] = opt.getplotgradientconditions()
            #indxlst  = []
            #for i in range(len(rs)):
            #    if rs[i] < 10 and rs[i] > 0.2:
            #        indxlst.append(i)
            #    else:
            #        continue
            #for indx in indxlst:
            #    trtab = []
            #    for i in range(len(trs[indx])):
            #        trtab.append([trs[indx][i], 1.0, 0.05])
            #    PlotChromatogram(BuildChromatogram(trtab, float(gconds[indx][2]), 0.01))
            #    print rs[indx]
            #    print gconds[indx]
            #    print trs[indx]



if __name__ == "__main__":
    main()
