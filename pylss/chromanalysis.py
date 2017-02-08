'''
@package chromanalysis

chromanalysis was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
Geneve January 2017

chromanalysis will analyse a chromatogram to convert this into descriptors.

Actually it contains some algorithms such as:

- Central moments to describe the band broadeing
  * Band variance (u1, u2)

'''

import decimal
from miscalgoritms import *

from math import sqrt, fabs
from os.path import isfile, basename

class ChromAnalysis(object):
    def __init__(self, time, signal, k=5, h=1.5):
        self.time = time
        self.signal = signal
        # peak detection settings
        self.k = k
        self.h = h

    def S1(self, x, i, k):
        left = 0.
        for j in range(1, k+1):
            if x[i] - x[i-j] > left:
                left = x[i] - x[i-j]
            else:
                continue

        right = 0.
        for j in range(1, k+1):
            if x[i] - x[i+j] > right:
                right = x[i] - x[i+j]
            else:
                continue
        return (left + right) / 2.

    def S2(self, x, i, k):
        avg_left = 0.
        for j in range(1, k+1):
            avg_left += x[i] - x[i-j]
        avg_left /= float(k)

        avg_right = 0.
        for j in range(1, k+1):
            avg_right = x[i] - x[i+j]
        avg_right /= float(k)
        return (avg_left + avg_right) / 2.

    def S3(self, x, i, k):
        left = 0.
        for j in range(1, k+1):
            left +=  x[i-j]
        left /= float(k)
        left = x[i] - left

        right = 0.
        for j in range(1, k+1):
            right = x[i+j]
        right /= float(k)
        right = x[i] - right
        return (left + right) / 2.

    def getPeaks(self):
        peaks = []
        #default values
        #h = 1
        #k = 5
        a = []
        for i in range(self.k, len(self.signal)-self.k):
            a.append(self.S1(self.signal, i, self.k))
            #a.append(self.S2(self.signal, i, self.k))
            #a.append(self.S3(self.signal, i, self.k))

        #Calculate the mean of only positive value of a
        n = 0
        mean = 0.
        for i in range(len(a)):
            if a[i] > 0:
                mean += a[i]
                n += 1
            else:
                continue
        mean /= float(n)

        #Calculate the standard deviation of only positive value of a
        stdev = 0.
        for i in range(len(a)):
            if a[i] > 0:
                x = (a[i] - mean)
                stdev += x*x
            else:
                continue

        stdev = sqrt(stdev/float(n-1))

        # detect the peaks
        for i in range(len(a)):
            if a[i] > 0 and (a[i] - mean) > (self.h*stdev):
                peaks.append([self.time[i+self.k], self.signal[i+self.k]])
            else:
                peaks.append([self.time[i+self.k], 0.])

        return peaks

    def peaksplit(self, peaks):
        #split peaks
        #TODO: remove adjacet peaks within window size k
        peaklst = []
        p = []
        for i in range(len(peaks)):
            if peaks[i][-1] > 0:
                p.append(peaks[i])
            else:
                if len(p) > 0:
                    peaklst.append([])
                    for row in p:
                        peaklst[-1].append(row)
                    del p[:]
                else:
                    continue
        return peaklst

    def Mu1CentralMoment(self, time_, signal_):
        n = 0.
        d = 0.
        for i in range(len(time_)-1):
            n += (signal_[i]+signal_[i+1])*(time_[i]+time_[i+1])
            d += (signal_[i]+signal_[i+1])
        if d != 0.:
            return n/(2*d)
        else:
            return 0.

    def Mu2CentralMoment(self, time_, signal_, u1_):
        if u1_ == 0 or u1_ == None:
            self.Mu1CentralMoment(time_, signal_)

        n = 0.
        d = 0.
        for i in range(len(time_)-1):
            n += (signal_[i]+signal_[i+1])*(((time_[i]+time_[i+1])/2.) - u1_)**2
            d += (signal_[i]+signal_[i+1])
        if d != 0.:
            return n/d
        else:
            return 0.

def demo():
    import sys
    import string
    fi = open(sys.argv[1], "r")
    signal = []
    time = []
    for line in fi:
        v = str.split(line.strip(), "\t")
        time.append(float(v[0]))
        signal.append(float(v[1]))

    chrom = ChromAnalysis(time, signal)
    peaks = chrom.getPeaks()
    peaklst = chrom.peaksplit(peaks)
    fo = open(sys.argv[2], "w")
    for p in peaklst:
        for row in p:
            fo.write("%f\t%f\n" % (row[0], row[1]))
        fo.write("end\n")
        #print ("%f\t%f" % (row[0], row[1]))

if __name__ == '__main__':
    demo()
