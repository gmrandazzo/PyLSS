'''
@package optseparation

optseparation was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
Geneve May 2015

optseparation will calculate logkw and s by iterative calculation through
the lss engine and after will try to find the optimal separation conditions
automatically trough the L-BFGS-B method.

'''

from pylss.optimizer import simplex as fmin
from math import sqrt, log10, fabs, isnan, isinf

def drange(start, stop, step):
    """ create a list of float arithmetic progress"""
    r = start
    while r < stop:
        yield r
        r += step

class OptSep(object):
    """Perform the optimization of a separation using the LSS parameters

    Parameters
    ----------
    v_m: float
        Define the dead volume for the unretained compounds.

	v_d: float
		Define the dwell volume of the system.
		This parameter is not necessary under isocratic conditions.

    flow: float
        Define the flow rate standard to calculate

    logkw_s_tab: array, shape(molecules,2)
        Define tje logkw_s_table. This can be calculated
        through the lss engine or can be inputed manually.

    rs_min: float
        Define the minimal resolution between two peaks

    plate: float
        Define the plate number for the colum
        according to the rule N = 5.54 * (tR/w)^2

    kisomin: float, default: 1
       Define the minimum k to measure.
       The default value of 1 means that the compound
       stay equally to the mobile and stationary phases

    kisomax: float, default 20:
        Define the maximum k to measure.
        The default value of 20 means that the compound
        stay too much in the stationary phase

    Returns
    ------
    phi: float
        Return the optimal % of organic modifier
        under isocratic conditions

    phirs: array, shape(objects, 4)
        Return the plot coordinates where
        the first column is the % of organic modifier;
        the second column is the worst rs;
        the third column is the retention time of the first peak;
        the fourth column is the retention time of the last peak.

    Notes
    -----
    See examples/plot_mdc_example.py for an example.

    References
    ----------
    Lloyd R. Snyder, John W. Dolan
    High-Performance Gradient Elution:
    The Practical Application of the Linear-Solvent-Strength Model
    ISBN: 978-0-471-70646-5
    January 2007

    """

    def __init__(self, v_m, v_d, flow, logkw_s_tab):
        self.v_m = float(v_m) # dead volume
        self.flow = float(flow) # flow rate for the logkw and s
        if v_d != None: # dwell volume (system volume)
		    self.v_d = float(v_d)
        self.logkw_s_tab = logkw_s_tab # table of lss parameters
        self.temp = [] # temperatures
        self.rs_min = 1.8  # resolution max
        self.plate = 20000 # plate number for the column N = 5.54 * (tR/w)^2
        self.kisomin = 1   # the compound stay equally to the mobile and stationary phases
        self.kisomax = 20  # the compound stay too much in the stationary phase
        self.mintg = 1
        self.maxtg = 60
        self.minflow = 0.1
        self.maxflow = 1
    def isocratic_iterfun(self, phi):
        """ Iterative function which minimize the rs.
        This function will take into account also the
        peak enlargement function of the organic modifier utilized."""
        if phi > 0:
            tr = []
            for row in self.logkw_s_tab:
                logk = row[0] - (row[1]*phi)
                k = pow(10, logk)
                if k > self.kisomin and k < self.kisomax:
                    t0 = self.v_m/self.flow
                    tr_tmp = (k *t0) + t0
                    tr.append(tr_tmp)
                else:
                    continue
            if len(tr) == len(self.logkw_s_tab):
                tr.sort()
                rs = []
                for i in range(1, len(tr)):
                    width1 = sqrt((5.54*tr[i-1]*tr[i-1])/ self.plate)
                    width2 = sqrt((5.54*tr[i]*tr[i]) / self.plate)
                    rs.append((2.*(tr[i]-tr[i-1]))/(width1+width2))

                # Search the critical couple
                small_rs = max(rs)
                for i in range(len(rs)):
                    if rs[i] < small_rs and rs[i] > 0:
                        small_rs = rs[i]
                    else:
                        continue
                return 1/small_rs
            else:
                return 9999
        else:
            return 9999

    def getisoconditions(self):
        """ Optimizer function starting
        from the 10% of organic modifier"""
        if len(self.temp) > 1: # According to de Vant Hoff
            return 0
        else: # one temperature experiment
            phi = fmin(self.isocratic_iterfun, [0.2], side=[0.1], tol=1e-10)
            tr = []
            for row in self.logkw_s_tab:
                logk = row[0] - row[1]*phi
                k = pow(10, logk)
                t0 = self.v_m/self.flow
                tr.append((k * t0) + t0)
            return phi*100, tr


    def getplotisoconditions(self):
        """ Plot the coordinates of the worst rs
        at differen % of organic modifier"""
        phirs = []
        for phi in drange(0.01, 0.9, 0.01):
            tr = []
            for row in self.logkw_s_tab:
                logk = row[0] - (row[1]*phi)
                k = pow(10, logk)
                t0 = self.v_m/self.flow
                tr_tmp = (k * t0) + t0
                tr.append(tr_tmp)

            if len(tr) == len(self.logkw_s_tab):
                tr.sort()
                rs = []
                for i in range(1, len(tr)):
                    width1 = sqrt((5.54*tr[i-1]*tr[i-1])/ self.plate)
                    width2 = sqrt((5.54*tr[i]*tr[i]) / self.plate)
                    rs.append((2.*(tr[i]-tr[i-1]))/(width1+width2))

                small_rs = max(rs)
                for i in range(len(rs)):
                    if rs[i] < small_rs and rs[i] > 0:
                        small_rs = rs[i]
                    else:
                        continue
                phirs.append([phi, small_rs, tr[0], tr[-1]])
            else:
                phirs.append([phi, 0., 0., 0.])
        return phirs


    def gradient_iterfun(self, gcond):
        """ Iterative function to scan for get the
        best gradient conditions.
        gcond is a vector which contain the conditions

        tr = t0/b * log10(2.3*k0*b)+t0+td

        b = (Vm * DeltaFi * S) / (tg*F)

        log10(k) = log10(kw) + S*Fi => log10(k0) = log10(kww) + S*Fi0
        Rs = 1/4 * [k2 / (1+k2)] * (alpha -1) * sqrt(N)
        """
        for item in gcond:
            if item > 0:
                continue
            else:
                return 9999

        init_b = gcond[0]
        final_b = gcond[1]
        tg = gcond[2]
        flow = gcond[3]
        if init_b < 0 or final_b < 0 or init_b > final_b or fabs(init_b - final_b) < 1e-1 or tg < self.mintg or tg > self.maxtg or flow < self.minflow or flow > self.maxflow:
            return 9999
        else:
		    # Function calculation
            deltafi = final_b - init_b
            t0 = self.v_m/flow
            td = self.v_d/flow
            tr = []
            kstar = []
            for row in self.logkw_s_tab:
                b = (self.v_m * deltafi * row[1]) / (tg*flow)
                kstar.append(float(1.0/(1.15*b)))
                logk0 = row[0] - (row[1] * init_b)
                k0 = float(pow(10, logk0))
                tr_tmp = ((t0/b) * log10(2.3*k0*b)) + t0 + td
                if tr_tmp < 0 or isnan(tr_tmp) == True or isinf(tr_tmp) == True or tr_tmp > tg or tr_tmp < t0:
                    continue
                else:
                    tr.append(float(tr_tmp))


		    # Resolution will be calculated according to the fundamental equation of chromatography
            if len(tr) == len(self.logkw_s_tab):
                print len(tr), len(self.logkw_s_tab)
                tr.sort()
                small_rs = tr[-1] - tr[0]

                #rs = []
                #for i in range(1, len(tr)):
                #    width1 = t0/sqrt(self.plate) * (1 + kstar[i])
                #    width2 = t0/sqrt(self.plate) * (1 + kstar[i-1])
                #    rs.append((2.*(tr[i]-tr[i-1]))/(width1+width2))
			    # Search the critical couple
                #small_rs = max(rs)
                #for i in range(len(rs)):
                #    if rs[i] < small_rs and rs[i] > 0:
                #        small_rs = rs[i]
                #    else:
                #        continue

                return 1/small_rs
            else:
                return 9999

    def getgradientconditions(self):
	"""
	Optimize the gradient conditions
	finding different value of flow rate,
	initial and final organic solvent and time gradient.
	The equation to be used are these and the equation for the resolution
	it is the same of the isocratic conditions.
	"""
        rslst = []
        gcondlst = []
        for init_b in drange(0.05, 0.60, 0.05):
            for final_b in drange(init_b+0.05, 0.95, 0.05):
                for tg in drange(1, self.maxtg, 1):
                    for flow in drange(0.1, self.maxflow, 0.05):
                        gcond = [init_b, final_b, tg, flow]
                        from scipy.optimize import fmin
                        tmp_bestgcond = fmin(self.gradient_iterfun, gcond, xtol=1e-3)
                        rslst.append(1/self.gradient_iterfun(tmp_bestgcond))
                        gcondlst.append(tmp_bestgcond)

        indx = rslst.index(max(rslst))
        bestgcond = gcondlst[indx]

        #init_b = 0.25 # 5%
        #final_b = 0.60 # 95 %
        #tg = 16 # 2 min defailt
        #flow = 0.6 # ml/min default
        #gcond = [init_b, final_b, tg, flow]

        #from scipy.optimize import fmin_l_bfgs_b
        #bounds = [(0.05, 0.95), (0.05, 0.95), (3, 40), (0.2, 1.5)] #CONSTRAINT
        #res = fmin_l_bfgs_b(self.gradient_iterfun, gcond, bounds, approx_grad=True, epsilon=0.01)
        #bestgcond = list(res[0])

        #from scipy.optimize import fmin
        #bestgcond = fmin(self.gradient_iterfun, gcond, xtol=1e-3)

        #bestgcond = fmin(self.gradient_iterfun, gcond, side=[0.01, 0.01, 1, 0.05], tol=1e-10)

        init_b = bestgcond[0]
        final_b = bestgcond[1]
        tg = bestgcond[2]
        flow = bestgcond[3]

		# Function calculation
        deltafi = final_b - init_b
        t0 = self.v_m/flow
        td = self.v_d/flow

        tr = []
        for row in self.logkw_s_tab:
            b = float((self.v_m * deltafi * row[1]) / (tg*flow))
            k0 = pow(10, row[0] - (row[1] * init_b))
            tr.append(((t0/b) * log10(2.3*k0*b)) + t0 + td)

        return bestgcond, tr, 1/self.gradient_iterfun(bestgcond)

    def getplotgradientconditions(self):
        """ Plot the Rs function of the different parameters
	    to optimize under gradient conditions
        """
        gcondlst = []
        rslst = []
        trlst = []
        for init_b in drange(0.10, 0.90, 0.1):
            for final_b in drange(init_b+0.1, 0.9, 0.1):
                for tg in drange(5, self.maxtg,  1):
                    for flow in drange(0.4, self.maxflow, 0.1):
                        # Function calculation
                        deltafi = final_b - init_b
                        t0 = self.v_m/flow
                        td = self.v_d/flow
                        tr = []
                        kstar = []
                        for row in self.logkw_s_tab:
                            b = (self.v_m * deltafi * row[1]) / (tg*flow)
                            kstar.append(float(1.0/(1.15*b)))
                            k0 = pow(10, row[0] - row[1] * init_b)
                            try:
                                tr_tmp = ((t0/b) * log10(2.3*k0*b)) + t0 + td
                            except:
                                tr_tmp = -1


                            if fabs(init_b - final_b) < 1e-1 or tr_tmp < 0 or isnan(tr_tmp) == True or isinf(tr_tmp) == True or tr_tmp > tg or tr_tmp < t0:
                                continue
                            else:
                                tr.append(float(tr_tmp))

                        # Resolution will be calculated according to the fundamental equation of chromatography
                        if len(tr) == len(self.logkw_s_tab):
                            trlst.append(tr)
                            tr.sort()
                            rs = []
                            for i in range(1, len(tr)):
                                width1 = t0/sqrt(self.plate) * (1 + kstar[i])
                                width2 = t0/sqrt(self.plate) * (1 + kstar[i-1])
                                rs.append((2.*(tr[i]-tr[i-1]))/(width1+width2))
                            # Search the critical couple

                            small_rs = max(rs)
                            for i in range(len(rs)):
                                if rs[i] < small_rs and rs[i] > 0:
                                    small_rs = rs[i]
                                else:
                                    continue
                            gcondlst.append([init_b, final_b, tg, flow])
                            rslst.append(small_rs)
                        else:
                            gcondlst.append([init_b, final_b, tg, flow])
                            rslst.append(-9999)
                            trlst.append(tr)
        return gcondlst, rslst, trlst

    def getplotselectivitygradientconditions(self):
        """ Plot the selectivity alpha function of the different parameters:
        - initial B
        - gradient steepness
        """
        gcondlst = []
        alphalst = []
        trlst = []
        for init_b in drange(0.05, 0.90, 0.05):
            for final_b in drange(init_b+0.05, 0.95, 0.05):
                for tg in drange(1, self.maxtg,  1):
                    for flow in drange(0.1, self.maxflow, 0.1):
                        # Function calculation
                        deltafi = final_b - init_b
                        t0 = self.v_m/flow
                        td = self.v_d/flow
                        tr = []
                        for row in self.logkw_s_tab:
                            b = (self.v_m * deltafi * row[1]) / (tg*flow)
                            k0 = pow(10, row[0] - row[1] * init_b)
                            try:
                                tr_tmp = ((t0/b) * log10(2.3*k0*b)) + t0 + td
                            except:
                                tr_tmp = -1

                            if fabs(init_b - final_b) < 1e-1 or tr_tmp < 0 or isnan(tr_tmp) == True or isinf(tr_tmp) == True or tr_tmp > tg or tr_tmp < t0:
                                continue
                            else:
                                tr.append(float(tr_tmp))

                        # Resolution will be calculated according to the fundamental equation of chromatography
                        if len(tr) == len(self.logkw_s_tab):
                            trlst.append(tr)
                            tr.sort()
                            alpha = []
                            for i in range(1, len(tr)):
                                alpha.append(tr[i]/tr[i-1])
                            # Search the critical selectivity

                            small_alpha = max(alpha)
                            for i in range(len(alpha)):
                                if alpha[i] < small_alpha and alpha[i] > 0:
                                    small_alpha = alpha[i]
                                else:
                                    continue
                            gcondlst.append([init_b, final_b, tg, flow])
                            alphalst.append(small_alpha)
                        else:
                            gcondlst.append([init_b, final_b, tg, flow])
                            alphalst.append(-9999)
                            trlst.append(tr)
        return gcondlst, alphalst, trlst
