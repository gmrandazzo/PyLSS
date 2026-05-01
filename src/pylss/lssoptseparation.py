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



from .ssengine import *
from .optseparation import *

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
                lssmol = SSGenerator(c_length, c_diameter, c_porosity, t0, v_d, flow)
                var = str.split(line.strip(), ";")
                tr = []
                for item in var:
                    tr.append(float(item))
                lss_logkw, lss_s = lssmol.getlssparameters(tr, tg, init_B, final_B)
                logkw_s_tab.append([lss_logkw, lss_s])
        fi.close()
        if t0 is None or flow is None or v_d is None:
            print("Error: Missing parameters in input file.")
            return
            
        opt = OptSep(float(t0)*float(flow), v_d, flow, logkw_s_tab)
        [phi, tr] = opt.getisoconditions()
        print("Best Percentage of Organic Solvent: %.2f" % (phi))
        print("Compounds will elute in this manner")
        for time in tr:
            print("%.2f" % (time))
        print("_"*20)

        [gcond, tr, Rs] = opt.getgradientconditions("lss", 10)

        if gcond is None:
            print("No valid gradient conditions found.")
            return

        print("Best Gradient Conditions with Rs: %f" % (Rs))
        print(" init B: %f\n final B: %f\n Time Gradient: %f\n Flow rate:%f\n t0: %f" % (gcond[0], gcond[1], gcond[2], flow, opt.v_m/flow))
        for time in tr:
            print("%.2f" % (time))

if __name__ == "__main__":
    main()
