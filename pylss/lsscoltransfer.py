'''
@package lssengine

lsscoltransfer was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
Geneve Dec 2015
'''

#from scipy.optimize import fmin
from optimizer import simplex as fmin
from math import sqrt, pi, log10, log, exp, fabs, isnan, isinf, erf
from optseparation import drange
from time import sleep

def square(val):
    """ return the square of val"""
    return val*val

class LSSColTrans(object):
    """Perform the generation of LSS parameters logKw, S, alhpa1 and alpha 2
    to be used in a column transfer.

    Parameters
    ----------
    c_length: float
        Define the column lenght.

    c_diameter: float
        Define the column diameter.

    c_porosity: float
        Define the column particule porisity.

    t0: float
        Define the dead time for the unretained compounds.

    v_d: float
        Define the instrumental dead volume.

    flow: float
        Define the flow rate.

    init_B: list(float)
        Define the initial % of organic modifier in a gradients.

    final_b: list(float)
        Define the final % of organic modifier in a gradients.

    tg: list(float)
        Define the gradients time.


    Returns
    ------
    lss_logkw: float
        Return the LSS logaritmic retention factor in water (logKw)
    lss_s: float
        Return the LSS S molecular parameter
    alpha: list(float)
        Return the column interaction factor for column 1


    References
    ----------
    Lloyd R. Snyder, John W. Dolan
    High-Performance Gradient Elution:
    The Practical Application of the Linear-Solvent-Strength Model
    ISBN: 978-0-471-70646-5
    January 2007

    """

    def __init__(self, c_length, c_diameter, c_porosity, t0, v_d, flow):
        self.logkw = []
        self.s = []
        self.alpha = []

        if c_length != None and c_diameter != None and c_porosity != None:
            #Column Parameters
            self.c_length = float(c_length)
            self.c_diameter = float(c_diameter)
            self.c_porosity = float(c_porosity)
            self.v0 = ((square(self.c_diameter)*self.c_length*pi*self.c_porosity)/4.)/1000.
        else:
            self.v0 = None

        #System Parameters
        self.v_d = v_d # Dwell Volume

        # Gradient Parameters
        self.flow = flow
        self.init_B = []
        self.final_B = []
        self.tg = []
        self.trtab = [] #table of retention times
        self.tr = [] #row of retention times

        self.t0 = []
        if c_length != None and c_diameter != None and c_porosity != None:
            for i in range(len(self.flow)):
                self.t0.append(self.v0/self.flow[i])
        else:
            self.t0 = t0

        self.td = []
        for i in range(len(self.v_d)):
            self.td.append(self.v_d[i]/self.flow[i])



    def rtpred(self, logkw, S, tg, init_B, final_B, alpha, t0, td):
        #print logkw, S, tg, alpha, t0, td
        if logkw != None and S != None and alpha > 0:
            DeltaFi = final_B - init_B
            b = (t0 * DeltaFi) / tg
            if b > 0:
                try:
                    kw = exp(logkw)
                    lnk0 = log(kw*alpha[0]) - S*alpha[1]*(init_B/100.)
                    k0 = exp(lnk0)
                    tr_pred = log(b*k0*S*t0+1)/(b*S*alpha) + t0 + td
                    return tr_pred
                except:
                    return 9999
            else:
                return 9999
        else:
            return 9999

    def iterfun(self, lss):
        res = 0.
        for i in range(len(self.tr)):
            tr_pred = self.rtpred(lss[0], lss[1], self.tg[i], self.init_B[i], self.final_B[i], self.alpha[i%len(self.alpha)], self.t0[i%len(self.alpha)], self.td[i%len(self.alpha)])
            res += square(self.tr[i]-tr_pred)
        rmsd = sqrt(res)
        return rmsd

    def iterfunalpha(self, alpha):
        """ Return the logKw and S parameters """
        self.alpha = alpha
        rmsd = 0.
        for i in range(len(self.trtab)):
            self.tr = self.trtab[i]
            lssinit = [0.1, 0.1]
            #simplex optimization
            logkw, s = fmin(self.iterfun, lssinit, side=[0.1, 0.1], tol=1e-10)
            #calcualte retention time of all compounds with this alpha
            sz_grad = len(self.flow)

            for j in range(len(self.trtab[i])):
                trpred = self.rtpred(logkw, s, self.tg[j % sz_grad], self.init_B[j % sz_grad], self.final_B[j % sz_grad], self.alpha[j % sz_grad], self.t0[j % sz_grad], self.td[j % sz_grad])
                rmsd += square(self.trtab[i][j] - trpred)
                print("%.2f %.2f [%f %f]") % (self.trtab[i][j], trpred, self.t0[j % sz_grad], self.td[j % sz_grad])

        #print alpha
        print ("-"*20)
        sleep(1)
        rmsd /= float(len(self.trtab))
        rmsd = sqrt(rmsd)
        return rmsd

    def getlssparameters(self, trtab, tg, init_B, final_B, alpha):
        self.trtab = trtab
        self.tg = tg
        self.init_B = init_B
        self.final_B = final_B
        alphainit = []
        asides = []
        for i in range(len(alpha)):
            alphainit.append(1.0)
            asides.append(0.1)
        self.alpha = fmin(self.iterfunalpha, alphainit, side=asides, tol=1e-10)

        for i in range(len(self.trtab)):
            self.tr = trtab[i]
            lssinit = [0.1, 0.1]
            logkw, s = fmin(self.iterfun, lssinit, side=[0.1, 0.1], tol=1e-3)
            self.logkw.append(logkw)
            self.s.append(s)
        return self.logkw, self.s, self.alpha
