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
from .io import parse_lss_input

def main():
    """ Main function """
    if len(sys.argv) != 3:
        print("Usage: %s <input file> <output file>" % (sys.argv[0]))
        print("\nNew Input File Format (Recommended):\n")
        print("---")
        print("t0: 0.969")
        print("dwell_volume: 0.375")
        print("flow_rate: 0.30")
        print("gradients:")
        print("  - [14, 5, 95] # [tg, startB, endB]")
        print("  - [60, 5, 95]")
        print("---")
        print("Molecule; Tr1; Tr2")
        print("Compound_A; 8.53; 22.11")
        print("\nLegacy format is still supported for backward compatibility.")
    else:
        experiment = parse_lss_input(sys.argv[1])
        
        with open(sys.argv[2], "w") as fo:
            fo.write("Log Kw\tS\n")
            
            t0 = experiment.t0
            v_d = experiment.dwell_volume
            flow = experiment.flow_rate
            c_length = experiment.column_length
            c_diameter = experiment.column_diameter
            c_porosity = experiment.metadata.get('column_porosity') # Optional

            tg = []
            init_B = []
            final_B = []
            for g in experiment.gradients:
                tg.append(float(g[0]))
                init_B.append(float(g[1])/100.)
                final_B.append(float(g[2])/100.)

            for var in experiment.data:
                # Skip header if present
                if var[0].lower() == 'molecule':
                    continue
                    
                if len(var) == len(tg) or len(var) == len(tg)+1:
                    lssmol = SSGenerator(c_length, c_diameter, c_porosity, t0, v_d, flow)
                    tr: list[float] = []
                    # Check if first column is molecule name
                    try:
                        float(var[0])
                        # it's a number, so it's a retention time
                        start_idx = 0
                        mol_name = f"Molecule_{len(tr)}"
                    except ValueError:
                        # it's a string, likely molecule name
                        start_idx = 1
                        mol_name = var[0]

                    for i in range(start_idx, len(var)):
                        tr.append(float(var[i]))

                    if len(tr) != len(tg):
                        continue

                    lss_logkw, lss_s = lssmol.getlssparameters(tr, tg, init_B, final_B)
                    
                    # Log prediction to stdout
                    com = f"{mol_name}\t"
                    for i in range(len(tr)):
                        trpred = lssmol.rtpred(lss_logkw, lss_s, tg[i], init_B[i], final_B[i], lssmol.t0, lssmol.td)
                        com += f"{tr[i]:.2f}\t{trpred:.2f}\t"
                    print(com.strip())
                    
                    fo.write(f"{lss_logkw:.10f}\t{lss_s:.10f}\n")
                else:
                    continue

if __name__ == "__main__":
    main()
