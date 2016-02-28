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

def square(val):
    """ return the square of val"""
    return val*val

class NLSS(object):
    """
1) k = kw + S1*exp(-S2*fi)

where:
    kw: is the pure retention factor in water
    S1: is the parameter one
    S2: is the parameter two
    Fi: %Organic solvent


2) t = (b*kw*t0 + fi0) / b  - ln(-1 * (S1*exp(b*S2*kw*t0) - kw*exp(fi0*S2) - S1)/kw) / (b*S2) + tD

where:
 b: the gradient slope (Fi_f - Fi_i / tG)
 t0: is the time 0
 tD: dwell time

This equation is property of Giuseppe Marco Randazzo

"""
    def __init__(self, CLenght, CDiameter, CPorosity, t0, Vd, flow):
        self.lss_logkw = None
        self.lss_A = None
        self.lss_B = None

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

    def iterfun(self, lss_param):
        """ Iterative function to minimize the error in prediction
        lss_param[0] = A = s1
        lss_param[1] = B = s2
        lss_param[2] = C = logkw
        """
        S1 = lss_param[0]
        S2 = lss_param[1]
        logkw = lss_param[2]

        res = 0.
        for i in range(len(self.tr)):
            tr_pred = self.rtpred4(S1, S2, logkw, self.tg[i], self.init_B[i], self.final_B[i], self.t0, self.td)
            kpred = (tr_pred - self.td -self.t0)/self.t0
            k = (self.tr[i] - self.td -self.t0)/self.t0
            res += square(k-kpred)
        rmsd = sqrt(res)

        return rmsd

    def rtpred4(self, A, B, C, tg, init_B, final_B, t0, td):
        """
        k = kw + S/fi^2
        """
        kw = exp(C)
        S1 = A
        S2 = B
        DeltaFi = final_B - init_B
        b = DeltaFi/tg

        try:
            trpred = (sqrt(init_B*(4*b*S1*t0 + init_B**3)) * fabs(init_B**2*kw+S1))/(2*b*S1*init_B) - (init_B*(init_B**2*kw+S1))/(2*b*S1) + t0 + td
            return trpred
        except:
            return 9999

    def rtpred3(self, A, B, C, tg, init_B, final_B, t0, td):
        """
        logk = logkw + S1*log(fi)
        """
        kw = exp(C)
        S1 = A
        DeltaFi = final_B - init_B
        b = DeltaFi/tg
        tpred = ((init_B**(-1*S1)*(init_B-b*kw*t0*init_B**S1*(S1-1)))**(1/(1-S1)))/b - init_B/b
        return tpred


    def rtpred2(self, A, B, C, tg, init_B, final_B, t0, td):
        """
        logkw = logkw + S1/(S2-x)
        """
        try:
            kw = exp(C)
            S1 = A
            S2 = B
            DeltaFi = final_B - init_B
            b = DeltaFi/tg
            com = (init_B*S1 + square(S2))
            n = exp(b*S1*kw*t0*exp(S1/S2)/square(S2))*com
            d = b*S1
            tpred = (n/d) - (com/d) + t0 + td
            return tpred
        except:
            return 9999

    def rtpred(self, A, B, C, tg, init_B, final_B, t0, td):
        """
        Analyitic solution from the integral which use the following relation:
        k = kw + S1*exp(-S2*fi)
        """
        try:
            kw = C
            S1 = A
            S2 = B
            DeltaFi = float(final_B) - float(init_B)
            b = DeltaFi/float(tg)
            p = (b*kw*t0+init_B)/b
            exp1a = exp(init_B*S2)
            exp1b = exp(b*S2*kw*t0)
            x = -1 * (S1*exp1b - kw*exp1a -S1)/kw
            if x > 0:
                return (p - log(x)/(b*S2) + t0 + td)
            else:
                return 9999
        except:
            return 9999

    def getlssparameters(self, tr, tg, init_B, final_B):
        """ Return the logKw and S parameters """
        self.tr = tr
        self.tg = tg
        self.init_B = init_B
        self.final_B = final_B

        #fast static optimization
        #lss_param_init =[0.5, 0.01, 0.01]
        lss_param_init =[1., 1., 1.]
        #lss_param_init = [4.012136916119, -3.280816332293, 102.010647704]
        lss_param = fmin(self.iterfun, lss_param_init, side=[0.01, 0.01, 1], tol=1e-10, iterations=2000)

        self.lss_A = lss_param[0]
        self.lss_B = lss_param[1]
        self.lss_logkw = lss_param[2]
        return self.lss_logkw, self.lss_A, self.lss_B
