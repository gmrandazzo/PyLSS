'''
@package plotengine

optimizer was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
Geneve September 2015

'''

import string
from math import exp
from pylab import plot, xlabel, ylabel, grid, show

def seq(start, stop, step=1):
    n = int(round((stop - start)/float(step)))
    if n > 1:
        return([float(start) + float(step*i) for i in range(n+1)])
    else:
        return([])

def square(x):
    return x*x

def BuildChromatogram(trtab, maxtime, delta_time):
    peaks = []
    time = []
    time.extend(seq(0, maxtime, delta_time))
    peaks.append(time)

    for mol in trtab:
        peak = []
        tr = float(mol[0])
        A = float(mol[1])
        C = float(mol[2])
        for i in range(0, len(time)):
            peak.append(A*exp( - square((time[i]-tr)) / square(C)))
        peaks.append(peak)
    nrows = len(peaks)
    ncols = len(peaks[0])
    return [[peaks[row][col] for col in range(0, ncols)] for row in range(0, nrows) ]

def PlotChromatogram(peaks):
    time = []
    signal = []
    for j in range(1, len(peaks[0])):
        time.append(peaks[0][j])
        signal.append(float(0))

    for i in range(1, len(peaks)):
        # first column is label
        for j in range(1, len(peaks[i])):
            signal[j-1] += peaks[i][j]
    plot(time, signal)

    xlabel('time')
    ylabel('Signal')
    grid(True)
    show()
