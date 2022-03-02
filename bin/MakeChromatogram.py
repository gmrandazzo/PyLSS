#!/usr/bin/env python

'''
@package MakeChromatogram

MakeChromatogram was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
Geneve Jan 2015

MakeChromatogram will create a chromatogram from retention times or LSS parameters

tr = t0/b * log10(2.3*k0*b+1)+td

b = (t0 * DeltaFi * S) / tg

log10(k) = log10(kw) + S*Fi => log10(k0) = log10(kww) + S*Fi0


peak = A*exp(-(time-B)^2/C^2)

A = peak amplitude
B = Retention Time of the peack
C = peak width

'''


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

import string
import re
from plotengine import *

def main():
    if len(sys.argv) < 5:
        print("Usage: %s  [input file time] [float(max time)] [float(delta time)] [ouput chromatogram]" % (sys.argv[0]))
    else:

        trtab = []
        namelst = ["time"]
        fi = open(sys.argv[1], "r")
        for line in fi:
            peak = []
            v = str.split(re.sub('\s+',' ',line))
            v = filter(None, v)
            namelst.append(v[0])
            trtab.append([float(v[1]), float(v[2]), float(v[3])])
        fi.close()

        peaks = BuildChromatogram(trtab, float(sys.argv[2]), float(sys.argv[3]))
        PlotChromatogram(peaks)
        #PlotDelayedChromatogram(peaks)
        fo = open(sys.argv[4], "w")
        nrows = len(peaks)
        ncols = len(peaks[0])
        for i in range(len(peaks)):
            fo.write("%s\t" % (namelst[i]))
            for j in range(len(peaks[i])-1):
                fo.write("%.3f\t" % (peaks[i][j]))
            fo.write("%.3f\n" % (peaks[i][-1]))
        fo.close()


if __name__=="__main__":
    main()
