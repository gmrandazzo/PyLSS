#!/usr/bin/env python

import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from pylss.lssengine import *
from pylss.optseparation import *

def main():
    """ Main function """
    if len(sys.argv) != 2:
        print "Usage: %s <input file>" % (sys.argv[0])
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
        logkw_s_tab = []
        c_length = c_diameter = c_porosity = t0 = v_d = flow = None
        init_B = []
        final_B = []
        tg = []
        for line in fi:
            if "Column Lenght" in line:
                c_length = float(str.split(line.strip(), ":")[-1].strip())
            elif "Column Diamter" in line:
                c_diameter = float(str.split(line.strip(), ":")[-1].strip())
            elif "Column Porosity" in line:
                c_porosity = float(str.split(line.strip(), ":")[-1].strip())
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
                t0 = str.split(line.strip(), ":")[-1].strip()
            elif "Temperature:" in line:
                continue
            elif "Plate Numbers" in line:
                continue
            else:
                lssmol = LinearGenerator(c_length, c_diameter, c_porosity, t0, v_d, flow)
                var = str.split(line.strip(), ";")
                tr = []
                for item in var:
                    tr.append(float(item))
                lss_logkw, lss_s = lssmol.getlssparameters(tr, tg, init_B, final_B)
                logkw_s_tab.append([lss_logkw, lss_s])
        fi.close()
        opt = OptSep(float(t0)*float(flow), v_d, flow, logkw_s_tab)
        [phi, tr] = opt.getisoconditions()
        print "Best Percentage of Organic Solvent: %.2f" % (phi)
        print "Compounds will elute in this manner"
        for time in tr:
            print "%.2f" % (time)
        print "_"*20

        [gcond, tr, Rs] = opt.getgradientconditions(1, 10)

        #[gconds, rs] = opt.getplotgradientconditions()
        #indx = rs.index(max(rs))
        #gcond = gconds[indx]
        #tr = []
        #Rs = max(rs)

        print "Best Gradient Conditions with Rs: %f" % (Rs)
        print " init B: %f\n final B: %f\n Time Gradient: %f\n Flow rate:%f\n t0: %f" % (gcond[0], gcond[1], gcond[2], flow, opt.v_m/flow)
        for time in tr:
            print "%.2f" % (time)

if __name__ == "__main__":
    main()
