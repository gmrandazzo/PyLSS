#!/usr/bin/env python

import os
import sys

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

def main():
    """ Main function """
    if len(sys.argv) != 3:
        print("Usage: %s <input file> <output file>" % (sys.argv[0]))
        print("\nInput File Format:\n")
        print("Column Lenght: 150")
        print("Column Diamter: 2.1")
        print("Column Porosity: 0.7")
        print("Time zero: 0.969 #to avoid the column parameters...")
        print("Dwell Volume: 0.9")
        print("%B Start: 5")
        print("%B End: 95")
        print("Flow Rate: 0.25")
        print("Gradient 1: 5 5 95")
        print("Gradient 2: 15 5 95")
        print("END")
        print("2.32\t4.64")
        print("3.42\t6.86")
        print("3.42\t6.86")
        print("....................")
        print("....................")
        print("....................\n")
    else:
        fi = open(sys.argv[1], "r")
        fo = open(sys.argv[2], "w")
        fo.write("Log Kw\tS\n")
        c_length = c_diameter = c_porosity = t0 = v_d = flow = None
        init_B = []
        final_B = []
        tg = []
        for line in fi:
            if "Column Length" in line:
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
                var = str.split(line.strip(), ";")
                if len(var) == len(tg) or len(var) == len(tg)+1:
                    lssmol = SSGenerator(c_length, c_diameter, c_porosity, t0, v_d, flow)
                    tr = []
                    if len(var) == 3:
                        for i in range(1, len(var)):
                            tr.append(float(var[i]))
                    else:
                        for item in var:
                            tr.append(float(item))

                    lss_logkw, lss_s = lssmol.getlssparameters(tr, tg, init_B, final_B)
                    com = ""
                    t0_ = lssmol.t0 #0.969 #lssmol.t0
                    td_ = lssmol.td #0.120/0.3 #lssmol.td
                    #tg_ = tg #[16.80, 16.80]#tg
                    tg_ = [47.67, 87.67]
                    for i in range(len(tr)):
                        trpred = lssmol.rtpred(lss_logkw, lss_s, tg_[i], init_B[i], final_B[i], t0_, td_)
                        if len(var) == 3:
                            com += str("%s\t%.2f\t%.2f\t" % (var[0], tr[i], trpred))
                        else:
                            com += str("%.2f\t%.2f\t" % (tr[i], trpred))
                    print(com)
                    del tr[:]
                    fo.write("%.10f\t%.10f\n" % (float(lss_logkw), float(lss_s)))
                else:
                    continue

        fi.close()
        fo.close()

if __name__ == "__main__":
    main()
