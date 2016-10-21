'''
@package nlssengine

nlssengine was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
Geneve November 2015

nlssengine will calculate kw and s1 and s2 by iterative calculation through
three different linear gradient elution.

The nonlinear solvent strenght theory is vailable for:
RPLC
HILIC
SFC

'''

#from scipy.optimize import fmin
from optimizer import simplex as fmin
from math import sqrt, pi, log10, log, exp, fabs, isnan, isinf, cos, sin, asin
from optseparation import drange
from time import sleep

def square(val):
    """ return the square of val"""
    return val*val

class NLSS(object):
    """
    To test:

     Ca = C0 + DeltaFi/Tg *tR

1) ln(k) = ln(kw) + 1/(S-Fi)

where:
    kw: is the pure retention factor in water
    S: is the parameter two
    Fi: %Organic solvent


2) t = ...

where:
 b: the gradient slope (Fi_f - Fi_i / tG)
 t0: is the time 0
 tD: dwell time

This equation is property of Giuseppe Marco Randazzo

"""
    def __init__(self, CLenght, CDiameter, CPorosity, t0, Vd, flow):
        self.logkw = None
        self.S = None

        if CLenght != None and CDiameter != None and CPorosity != None:
            #Column Parameters
            self.CLenght = float(CLenght)
            self.CDiameter = float(CDiameter)
            self.CPorosity = float(CPorosity)
            self.V0 = ((square(self.CDiameter)*self.CLenght*pi*self.CPorosity)/4.)/1000.
        else:
            self.V0 = None

        #System Parameters
        self.Vd = float(Vd) # Dwell Volume

        # Gradient Parameters
        self.flow = float(flow)

        self.init_B = []
        self.final_B = []
        self.tg = []
        self.tr = []

        if CLenght != None and CDiameter != None and CPorosity != None:
            self.t0 = self.V0/self.flow
        else:
            self.t0 = float(t0)

        self.td = self.Vd/self.flow


        #if self.V0 != None:
          #print("V0 %f t0 %f td %f DeltaFi %f" % (self.V0, self.t0, self.td, self.DeltaFi))
        #else:
          #print("t0 %f td %f DeltaFi %f" % (self.t0, self.td, self.DeltaFi))

    def simplelr(self, x, y):
        """ Linear Regression between x and y """
        slope = 0.
        intercept = 0.
        x_med = sum(x)/float(len(x))
        y_med = sum(y)/float(len(x))
        n = 0.
        d = 0.
        for i in range(len(x)):
            n += (x[i] - x_med) * (y[i]-y_med)
            d += square((x[i] - x_med))
        slope = n/d
        intercept = y_med - slope*x_med
        return slope, intercept

    def iterfun(self, param):
        """ Iterative function to minimize the error in prediction
        lss_param[0] = A = s1
        lss_param[1] = B = s2
        lss_param[2] = C = logkw
        """
        logkw = param[0]
        S = param[1]
        q = param[2]

        res = 0.
        for i in range(len(self.tr)):
            tr_pred = self.rtpred(logkw, S, q, self.tg[i], self.init_B[i], self.final_B[i], self.t0, self.td)
            res += square(self.tr[i]-tr_pred)
        rmsd = sqrt(res)
        return rmsd

    def rtpred(self, kw, S, c, tg, init_B, final_B, t0, td):
        """
        Analyitic solution from the integral which use the following relation:
        ln(k) = ln(kw) + ln(1/(S-Fi))
        """

        try:
            b = (float(final_B) - float(init_B))/float(tg)
            bd = b*td
            bcw = b*(1-c)*kw
            bdfs = -bd-init_B+S
            mc = -1+c
            omc = 1/mc
            a = (((1/bdfs)**mc)/bcw) - t0
            p = (bcw*a)**omc
            if p != p:
                return 9999
            else:
                #print "%f %f %f %f %f %f %f %f %f\n" % (kw, S, c, init_B, final_B, t0, td, tg, b)
                return -1/b *((1+bd * p) + (init_B * p) - (S * p)) * p
        except:
            return 9999


    def getlssparameters(self, tr, tg, init_B, final_B):
        """ Return the logKw and S parameters """
        self.tr = tr
        self.tg = tg
        self.init_B = init_B
        self.final_B = final_B

        #fast static optimization
        param_init =[1., 1., 1.]
        best_param = fmin(self.iterfun, param_init, side=[1., 1., 1.], tol=1e-6, iterations=1000)

        self.logkw = best_param[0]
        self.S = best_param[1]
        c = best_param[1]
        return self.logkw, self.S, c
