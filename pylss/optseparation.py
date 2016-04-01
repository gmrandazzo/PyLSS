'''
@package optseparation

optseparation was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
Geneve May 2015

optseparation will calculate logkw and s by iterative calculation through
the lss engine and after will try to find the optimal separation conditions
automatically trough the L-BFGS-B method.

'''

from optimizer import simplex as fmin
from lssengine import LinearGenerator
from math import sqrt, log10, fabs, isnan, isinf
from miscalgoritms import *

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
        self.minflow = 0.2
        self.maxflow = 0.6
        self.c_lenght = 15 #cm
        self.c_particle = 1.7 #um
        self.tr_min = 1
        self.tr_max = 60

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
        if len(self.temp) > 1: # Two temperature experiments according to de Vant Hoff
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


    def get_gradient_rs(self, grad):
        """ Function to optimise gradient trough simplex iteration """
        init_b = grad[0]
        final_b = grad[1]
        tg = grad[2]
        flow = grad[3]
        if final_b > 1 or final_b < 0 or init_b < 0 or init_b > 1 or flow < 0 or tg < 0:
            return 9999
        else:
            deltafi = final_b - init_b
            t0 = self.v_m/flow
            td = self.v_m/flow
            N = (self.c_lenght*10000.)/(2.3*self.c_particle)
            trtab = []
            lssmol = LinearGenerator(None, None, None, t0, self.v_d, flow)
            i = 0
            for row in self.logkw_s_tab:
                lss_logkw = float(row[0])
                lss_s = float(row[1])
                b = (t0*(final_b-init_b)*lss_s)/tg
                # See D. Guillaume et al / J. Chromatogr. A 1216(2009) 3232-3243
                W = (4*t0)/sqrt(N)* (1+ 1/(2.3*b))/4
                try:
                    trtab.append([lssmol.rtpred(lss_logkw, lss_s, tg, init_b, final_b, t0, td), W, i])
                except:
                    trtab.append([9999, W, i])
                i += 1


            trtab = sorted(trtab, key=lambda x:x[0])


            # get min and max time
            tr_min = trtab[0][0]
            tr_max = trtab[-1][0]
            if tr_min > self.tr_min and tr_max < self.tr_max and tr_min > t0 and tr_max < tg:
                #minimise the inverse of the sum of the resolutions
                width1 = trtab[1][1]
                width2 = trtab[1-1][1]
                tr1 = trtab[1-1][0]
                tr2 = trtab[1][0]
                rs = (2.*(tr2-tr1)) / (width1+width2)
                for i in range(1, len(trtab)):
                    width1 = trtab[i][1]
                    width2 = trtab[i-1][1]
                    tr1 = trtab[i-1][0]
                    tr2 = trtab[i][0]
                    tmp_rs = (2.*(tr2-tr1)) / (width1+width2)
                    if tmp_rs < rs:
                        rs = tmp_rs
                    else:
                        continue
                return 1.0/(rs)
            else:
                return 9999


    def getgradientconditions(self, tr_min, tr_max):
	"""
	Optimize the gradient conditions
	finding different value of flow rate,
	initial and final organic solvent and time gradient.
	The equation to be used are these and the equation for the resolution
	it is the same of the isocratic conditions.
    """
        self.tr_min = tr_min
        self.tr_max = tr_max
        best_rs = None
        best_gcond = None
        for init_b in drange(0.00, 1.0, 0.1):
            for final_b in drange(init_b+0.1, 1.0, 0.1):
                for tg in drange(1, self.maxtg, 9):
                    for flow in drange(0.1, self.maxflow, 0.1):
                        gcond = [init_b, final_b, tg, flow]
                        try:
                            tmp_bestgcond = fmin(self.get_gradient_rs, gcond, side=[0.05, 0.05, 1, 0.1], tol=1e-10)
                            tmp_rs = self.get_gradient_rs(tmp_bestgcond)
                            if best_rs != None:
                                if tmp_rs < best_rs:
                                    best_rs = tmp_rs
                                    best_gcond = tmp_bestgcond
                                else:
                                    continue
                            else:
                                best_gcond = tmp_bestgcond
                                best_rs = tmp_rs
                        except:
                            continue

        #self.tr_min = float(tr_min)
        #self.tr_max = float(tr_max)
        #gcond = [0.05, 0.95, 60, 0.3]
        #best_gcond = fmin(self.get_gradient_rs, gcond, side=[0.05, 0.05, 1, 0.1], tol=1e-10)
        #best_rs = self.get_gradient_rs(best_gcond)
        init_b = best_gcond[0]
        final_b = best_gcond[1]
        tg = best_gcond[2]
        flow = best_gcond[3]

		# Function calculation
        deltafi = final_b - init_b
        t0 = self.v_m/flow
        td = self.v_d/flow

        tr = []
        for row in self.logkw_s_tab:
            b = float((self.v_m * deltafi * row[1]) / (tg*flow))
            k0 = pow(10, row[0] - (row[1] * init_b))
            tr.append(((t0/b) * log10(2.3*k0*b)) + t0 + td)
        return best_gcond, tr, 1/best_rs

    def getplotgradientconditions(self, flow_min=0.2, flow_max=0.6, g_start_min=0.00, g_start_max=0.98,
                                  g_stop_min=0.0, g_stop_max=0.98, time_grad_min=2, time_grad_max=60):
        """ Plot the Rs function of the different parameters
	    to optimize under gradient conditions
        """
        gcondlst = []
        rslst = []
        trlst = []
        d_init_b = (g_start_max - g_start_min)/20.
        d_final_b = (g_stop_max-g_stop_min)/20.
        N = (self.c_lenght*10000.)/(2.3*self.c_particle)
        for init_b in drange(g_start_min, g_start_max, 0.05):
            for final_b in drange(g_stop_min+init_b, g_stop_max, 0.05):
                for tg in drange(time_grad_min, time_grad_max,  1):
                    for flow in drange(flow_min, flow_max, 0.1):
                        # Function calculation
                        deltafi = final_b - init_b
                        t0 = self.v_m/flow
                        td = self.v_d/flow
                        trtab = []
                        i = 0
                        lssmol = LinearGenerator(None, None, None, t0, self.v_d, flow)
                        for row in self.logkw_s_tab:
                            lss_logkw = float(row[0])
                            lss_s = float(row[1])
                            b = (t0*(final_b-init_b)*lss_s)/tg
                            # See D. Guillaume et al / J. Chromatogr. A 1216(2009) 3232-3243
                            W = (4*t0)/sqrt(N)* (1+ 1/(2.3*b))/4
                            trtab.append([lssmol.rtpred(lss_logkw, lss_s, tg, init_b, final_b, t0, td), W, i])
                            i += 1

                        # Resolution will be calculated according to the fundamental equation of chromatography
                        if len(trtab) == len(self.logkw_s_tab):
                            trlst.append(list())
                            for i in range(len(trtab)):
                                trlst[-1].append(trtab[i][0])
                            trtab = sorted(trtab, key=lambda x:x[0])
                            rs = []
                            for i in range(1, len(trtab)):
                                width1 = trtab[i][1]
                                width2 = trtab[i-1][1]
                                tr1 = trtab[i-1][0]
                                tr2 = trtab[i][0]
                                rs.append((2.*(tr2-tr1))/(width1+width2))
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
                            continue

        return gcondlst, rslst, trlst
