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
                if c_length is None or c_diameter is None or c_porosity is None or t0 is None or v_d is None or flow is None:
                    continue
                lssmol = SSGenerator(float(c_length), float(c_diameter), float(c_porosity), float(t0),
                                      float(v_d), float(flow))
                var = str.split(line.strip(), ";")
                if len(var) < 2:
                    continue
                tr = [float(var[0]), float(var[1])]
                # Extract gradients from file if possible, or assume defaults based on the outdated script logic
                # For now, matching the SSGenerator.getlssparameters(tr, tg, init_B, final_B)
                # We need tg1, tg2, init_b, final_b to be defined
                if tg1 is None or tg2 is None or init_b is None or final_b is None:
                    continue
                tg = [float(tg1), float(tg2)]
                init_B = [float(init_b)/100., float(init_b)/100.]
                final_B = [float(final_b)/100., float(final_b)/100.]
                
                lss_logkw, lss_s = lssmol.getlssparameters(tr, tg, init_B, final_B)
                logkw_s_tab.append([lss_logkw, lss_s])
        fi.close()
        if t0 is None or v_d is None or flow is None:
            return
        # OptSep(v_m, v_d, flow, logkw_s_tab)
        isoopt = OptSep(float(t0)*float(flow), float(v_d), float(flow), logkw_s_tab)
        phirs = isoopt.getplotisoconditions()
        for row in phirs:
            print("%f  %f  %f" % (row[0], row[1], row[3]))

if __name__ == "__main__":
    main()
