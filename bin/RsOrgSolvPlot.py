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
        c_length = c_diameter = c_porosity = t0 = v_d = flow = init_b = final_b = tg1 = tg2 = None
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
                t0 = str.split(line.strip(), ":")[-1].strip()
            else:
                lssmol = LinearGenerator(c_length, c_diameter, c_porosity, t0,
                                      v_d, flow, init_b, final_b, tg1, tg2)
                var = str.split(line.strip(), ";")
                lss_logkw, lss_s = lssmol.getlssparameters(var[0], var[1])
                logkw_s_tab.append([lss_logkw, lss_s])
        fi.close()
        isoopt = OptSep(t0, logkw_s_tab)
        phirs = isoopt.getplotisoconditions()
        for row in phirs:
            print("%f  %f  %f" % (row[0], row[1], row[3]))

if __name__ == "__main__":
    main()
