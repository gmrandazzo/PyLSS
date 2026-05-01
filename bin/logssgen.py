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


import os
import sys



from pylss.ssengine import *

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
                v_parts = str.split(v, " ")
                tg.append(float(v_parts[0]))
                init_B.append(float(v_parts[1])/100.)
                final_B.append(float(v_parts[2])/100.)
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
                com = ""
                for i in range(len(tr)):
                    trpred = logssmol.logrtpred(lss_logkw, lss_s, tg[i], init_B[i], final_B[i], logssmol.t0, logssmol.td)
                    com += str("%.2f\t%.2f\t" % (tr[i], trpred))
                print(com)
                del tr[:]
                fo.write("%.10f\t%.10f\n" % (float(lss_logkw), float(lss_s)))

        fi.close()
        fo.close()

if __name__ == "__main__":
    main()
