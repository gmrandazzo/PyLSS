#!/usr/bin/env python

import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from pylss.lssengine import *
from pylss.optseparation import *
from pylss.plotengine import *

def main():
    """ Main function """
    if len(sys.argv) != 3:
        print "Usage: %s <input file Temperature 1> <input file Temperature 2> where t2 > t1" % (sys.argv[0])
        print "\nInput File Format\n:"
        print "Column Lenght: 150"
        print "Column Diamter: 2.1"
        print "Column Porosity: 0.7"
        print "Time zero: 0.969 #to avoid the column parameters..."
        print "Dwell Volume: 0.9"
        print "%B Start: 5"
        print "%B End: 95"
        print "Flow Rate: 0.25"
        print "Time Gradient 1: 5"
        print "Time Gradient 2: 15"
        print "END"
        print "2.32\t4.64"
        print "3.42\t6.86"
        print "3.42\t6.86"
        print "...................."
        print "...................."
        print "....................\n"
    else:
        fi = open(sys.argv[1], "r")
        logkw_s_tab_t1 = []
        t1 = None
        c_length = c_diameter = c_porosity = t0 = v_d = flow = init_b = final_b = tg1 = tg2 = N = None
        for line in fi:
            if "Column Lenght:" in line:
                c_length = str.split(line.strip(), ":")[-1].strip()
            elif "Column Diamter:" in line:
                c_diameter = str.split(line.strip(), ":")[-1].strip()
            elif "Column Porosity:" in line:
                c_porosity = str.split(line.strip(), ":")[-1].strip()
            elif "Dwell Volume:" in line:
                v_d = str.split(line.strip(), ":")[-1].strip()
            elif "%B Start:" in line:
                init_b = str.split(line.strip(), ":")[-1].strip()
            elif "%B End:" in line:
                final_b = str.split(line.strip(), ":")[-1].strip()
            elif "Flow Rate:" in line:
                flow = str.split(line.strip(), ":")[-1].strip()
            elif "Time Gradient 1:" in line:
                tg1 = str.split(line.strip(), ":")[-1].strip()
            elif "Time Gradient 2:" in line:
                tg2 = str.split(line.strip(), ":")[-1].strip()
            elif "Time zero:" in line:
                t0 = float(str.split(line.strip(), ":")[-1].strip())
            elif "Temperature:" in line:
                t1 = float(str.split(line.strip(), ":")[-1].strip())
            elif "Plate Numbers:" in line:
                N = float(str.split(line.strip(), ":")[-1].strip())
            else:
                lssmol = LinearGenerator(c_length, c_diameter, c_porosity, t0,
                                      v_d, flow, init_b, final_b, tg1, tg2)
                var = str.split(line.strip(), ";")
                lss_logkw, lss_s = lssmol.getlssparameters(var[0], var[1])
                logkw_s_tab_t1.append([lss_logkw, lss_s])
        fi.close()
        
        fi = open(sys.argv[2], "r")
        logkw_s_tab_t2 = []
        t2 =  None
        for line in fi:
            if "Column Lenght:" in line:
                c_length = str.split(line.strip(), ":")[-1].strip()
            elif "Column Diamter:" in line:
                c_diameter = str.split(line.strip(), ":")[-1].strip()
            elif "Column Porosity:" in line:
                c_porosity = str.split(line.strip(), ":")[-1].strip()
            elif "Dwell Volume:" in line:
                v_d = str.split(line.strip(), ":")[-1].strip()
            elif "%B Start:" in line:
                init_b = str.split(line.strip(), ":")[-1].strip()
            elif "%B End:" in line:
                final_b = str.split(line.strip(), ":")[-1].strip()
            elif "Flow Rate:" in line:
                flow = str.split(line.strip(), ":")[-1].strip()
            elif "Time Gradient 1:" in line:
                tg1 = str.split(line.strip(), ":")[-1].strip()
            elif "Time Gradient 2:" in line:
                tg2 = str.split(line.strip(), ":")[-1].strip()
            elif "Time zero:" in line:
                t0 = float(str.split(line.strip(), ":")[-1].strip())
            elif "Temperature:" in line:
                t2 = float(str.split(line.strip(), ":")[-1].strip())
            elif "Plate Numbers:" in line:
                N = float(str.split(line.strip(), ":")[-1].strip())
            else:
                lssmol = LinearGenerator(c_length, c_diameter, c_porosity, t0,
                                      v_d, flow, init_b, final_b, tg1, tg2)
                var = str.split(line.strip(), ";")
                lss_logkw, lss_s = lssmol.getlssparameters(var[0], var[1])
                logkw_s_tab_t2.append([lss_logkw, lss_s])
        fi.close()
        
        # Betweent t1 and t2 there is a line which give us access to all the 
        # gamma of logkw and s.
        Rslst = []
        gcondlst = []
        trlst = []
        temps = []
        
        for i in range(len(logkw_s_tab_t1)):
            mlogk = (logkw_s_tab_t2[i][0]-logkw_s_tab_t1[i][0]) / (t2-t1)
            qlogk = (t2*logkw_s_tab_t1[i][0] - t1*logkw_s_tab_t2[i][0]) / (t2-t1)
            mS = (logkw_s_tab_t2[i][1]-logkw_s_tab_t1[i][1]) / (t2-t1)
            qS = (t2*logkw_s_tab_t1[i][1] - t1*logkw_s_tab_t2[i][1]) / (t2-t1)
            print mlogk, qlogk, -1*mS, -1*qS # -1 for the hplc simulatir application
                
        for t in drange(t1, t2+1, 0.5):
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
            opt.maxtg = 3
            opt.maxflow = 1 
            
            [gcond, tr, Rs] = opt.getgradientconditions()
            Rslst.append(Rs)
            gcondlst.append(gcond)
            trlst.append(tr)
        bestrs = Rslst.index(max(Rslst))
        print "Best Gradient Conditions Rs: %f at temperature %f" % (Rslst[bestrs], temps[bestrs])
        gcond = gcondlst[bestrs]
        print "init B: %f\nfinal B: %f\nTime Gradient: %f\nFlow rate:%f\nt0: %f" % (gcond[0], gcond[1], gcond[2], gcond[3], opt.v_m/gcond[3])
        for time in tr:
            print "%.2f" % (time)

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
