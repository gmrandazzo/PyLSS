'''
@package lssengine

lssengine was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
Geneve July 2014

lss engine will calculate logkw and s by iterative calculation through
two different linear gradient elution.

The lss theory in reversed phase according to Snyder-Dolan[1] says:

tr = t0/b * log10(2.3*k0*b)+td+t0

b = (t0 * DeltaFi * S) / tg

log10(k) = log10(kw) + S*Fi => log10(k0) = log10(kww) + S*Fi0



According to the work of Neue-Kuss[2] the LSS theory in a curvated model is:

1) ln(k) = ln(kw) + 2 ln(1+a*Fi) - (S*Fi)/(1+a*Fi)

where:
a: is the curvature
S: slope
Fi: %Organic solvent


2) tr - t0 - td = (1/b*S) *  N/D

   N =  (1+a*c0)^2 * ln(b*S*k0*exp((-S*c0)/(1+a*c0)) * (t0 - ((td/(1+a*c0)^2)*k0*exp((-S*c0)/(1+a*c0))+1)+1)
   D = (1- ((a/S)*(1+a*c0)*ln(b*S*k0*exp((-S*c0)/(1+a*c0)) * (t0 - ((td/(1+a*c0)^2)*k0*exp((-S*c0)/(1+a*c0))+1)+1))))
   b = ((ce-c0) / tg) * (t0 - (td/k0+1))

where:
ce: final composition organic solvent
c0: initial composition organic solvent
k0: is the retention factor at composition c0


This curvated model require at least three gradients and is eploited for HILIC
Chromatography.


[1]   L.R. Snyder, J.W. Dolan, J.R. Gant
      Gradient elution in high-performance liquid chromatography : I. Theoretical basis for reversed-phase systems
      J. Chromatogr., 165 (1979), p. 3

[2]   Uwe Dieter Neue, Hans-Joachim Kuss
      Retention modeling and method development in hydrophilic interaction chromatography
      Journal of Chromatography A
      Volume 1217, Issue 24, Pages 3794-3803, 2010
'''

#from scipy.optimize import fmin
from optimizer import simplex as fmin
from math import sqrt, pi, log10, log, exp, fabs, isnan, isinf, erf
from optseparation import drange

def square(val):
    """ return the square of val"""
    return val*val

class LinearGenerator(object):
    """Perform the generation of LSS parameters logKw and S

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



    References
    ----------
    Lloyd R. Snyder, John W. Dolan
    High-Performance Gradient Elution:
    The Practical Application of the Linear-Solvent-Strength Model
    ISBN: 978-0-471-70646-5
    January 2007

    """

    def __init__(self, c_length, c_diameter, c_porosity, t0, v_d, flow):
        self.lss_logkw = None
        self.lss_s = None #0.25*sqrt(self.mw) # from Dolan-Snyder
        self.coeff = None #0.25  Position from Dolan-Snyder
        self.mw = None

        if c_length != None and c_diameter != None and c_porosity != None:
            #Column Parameters
            self.c_length = float(c_length)
            self.c_diameter = float(c_diameter)
            self.c_porosity = float(c_porosity)
            self.v0 = ((square(self.c_diameter)*self.c_length*pi*self.c_porosity)/4.)/1000.
        else:
            self.v0 = None

        #System Parameters
        self.v_d = float(v_d) # Dwell Volume

        # Gradient Parameters
        self.flow = float(flow)
        self.init_B = []
        self.final_B = []
        self.tg = []
        self.tr = []

        if c_length != None and c_diameter != None and c_porosity != None:
            self.t0 = self.v0/self.flow
        else:
            self.t0 = float(t0)

        self.td = self.v_d/self.flow



    def rtpred(self, logkw, S, tg, init_B, final_B, t0, td):
        if logkw != None and S != None:
            DeltaFi = final_B - init_B
            b = (t0 * DeltaFi * S) / tg
            if b > 0:
                """
                less powerfull in some cases due to the log10 approximation...
                """
                logk0 = logkw - S*(init_B/100.)
                k0 = pow(10, logk0)
                tr_pred = ((t0/b) * log10(2.3*k0*b))+ t0 + td

                """
                better powerfull
                lnk0 = logkw - S*(self.init_B/100.)
                k0 = exp(lnk0)
                    tr1_pred = log(b1*k0*self.t0+1)/b1 + self.t0 + self.td
                tr2_pred = log(b2*k0*self.t0+1)/b2 + self.t0 + self.td
                """
                return tr_pred
            else:
                return 9999
        else:
            return 9999

    def iterfun(self, lss):
        res = 0.
        for i in range(len(self.tr)):
            tr_pred = self.rtpred(lss[0], lss[1], self.tg[i], self.init_B[i], self.final_B[i], self.t0, self.td)
            res += square(self.tr[i]-tr_pred)
        rmsd = sqrt(res)
        return rmsd

    def getlssparameters(self, tr, tg, init_B, final_B):
        """ Return the logKw and S parameters """
        self.tr = tr
        self.tg = tg
        self.init_B = init_B
        self.final_B = final_B
        lssinit = [0.1, 0.1]
        #simplex optimization
        self.lss_logkw, self.lss_s = fmin(self.iterfun, lssinit, side=[0.1, 0.1], tol=1e-10)
        return self.lss_logkw, self.lss_s


    def getlss_s(self):
        """ Return the S parameter """
        return self.lss_s
