'''
@package optseparation

optseparation was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
Geneve May 2015

optseparation will calculate logkw and s by iterative calculation through
the lss engine and after will try to find the optimal separation conditions
automatically trough the L-BFGS-B method.

'''

from optimizer import simplex as fmin
from gradientutils import *
from math import sqrt, log10, log, fabs, isnan, isinf
from miscalgoritms import *
import numpy as np

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
    None.

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
        self.c_lenght = 15 #cm
        self.c_particle = 1.7 #um
        self.tr_min = 1
        self.tr_max = 60


    def getSelMapPlot(self, model, flow=0.3, g_start_min=0.00, g_start_max=1.0, g_stop_min=0.1, g_stop_max=1.0, time_grad_min=2, time_grad_max=60):
        """ Plot the Selectivity function of the different parameters
	    to optimize under gradient conditions
        """
        gcondlst = []
        sellst = []
        trlst = []
        #d_init_b = (g_start_max - g_start_min)/20.
        #d_final_b = (g_stop_max-g_stop_min)/20.
        #print d_init_b, d_final_b
        step = 0.05
        #for init_b in drange(g_start_min, g_start_max, step):
        for init_b in np.linspace(g_start_min, g_start_max, 20, endpoint=True):
            #for final_b in drange(g_stop_min+init_b, float(g_stop_max), step):
            for final_b in np.linspace(g_stop_min, g_stop_max, 20, endpoint=True):
                for tg in drange(time_grad_min, time_grad_max,  2):
                    lsscc = None
                    lowest_alpha = None
                    if model == "lss":
                        lsscc, lowest_alpha = get_lss_gradient_critical_selectivity(self.c_lenght, self.c_particle, init_b, final_b, tg, flow, self.v_m, self.v_d, self.logkw_s_tab, crit_alpha=1.01)
                    else:#
                        lsscc, lowest_alpha = get_logss_gradient_critical_selectivity(self.c_lenght, self.c_particle, init_b, final_b, tg, flow, self.v_m, self.v_d, self.logkw_s_tab, crit_alpha=1.01)

                    if lowest_alpha != None:
                        #print init_b, final_b, tg, lowest_alpha
                        gcondlst.append([init_b, final_b, tg, self.flow, lowest_alpha])
                        # lsscc: first two column correspond to the object id, the last to the rs associated
                        if lsscc != None and len(lsscc) > 0:
                            totsel = 0.
                            for i in range(len(lsscc)):
                                totsel += lsscc[i][-1]
                            avgrs = totsel/float(len(lsscc))
                            sellst.append(avgrs)
                        else:
                            continue
                    else:
                        continue
        return gcondlst, sellst, trlst

    def getAutomaticElutionWindowStretching(self, model, flow=0.3, g_start_min=0.00, g_start_max=1.0, g_stop_min=0.1, g_stop_max=1.0, time_grad_min=2, time_grad_max=60):
        """ Calculate the automatic elution window stretching to optimise the separation
        """
        gcond = []
        best_dindx = None
        t0 = self.v_m *self.flow
        td = self.v_d *self.flow
        lssmol = SSGenerator(None, None, None, t0, self.v_d, self.flow)
        print(g_start_min, g_stop_min)
        for init_b in np.linspace(g_start_min, g_start_max, 20, endpoint=True):
            for final_b in np.linspace(g_stop_min, g_stop_max, 20, endpoint=True):
                for tg in drange(time_grad_min, time_grad_max,  2):
                    trtab = []
                    i = 0
                    opt_spacing = (tg - (t0+1))/float(len(self.logkw_s_tab))
                    for row in self.logkw_s_tab:
                        lss_logkw = row[0]
                        lss_s =  row[1]
                        tr_tmp = None
                        if model == "lss":
                            tr_tmp = lssmol.rtpred(lss_logkw, lss_s, tg, init_b, final_b, t0, td)
                        else:#
                            tr_tmp = logssmol.logrtpred(lss_logkw, lss_s, tg, init_b, final_b, t0, td)

                        if tr_tmp < t0 or isnan(tr_tmp) or tr_tmp == None:
                            break # these condition are not ok for automatic elution window stretching calculations
                        else:
                            trtab.append([tr_tmp, i])
                        i+=1

                    if len(trtab) == len(self.logkw_s_tab):
                        trtab = sorted(trtab, key=lambda x:x[0])
                        dindx = 0.

                        for i in range(1, len(trtab)):
                            dindx += ((trtab[i][0]-trtab[i-1][0]) - opt_spacing)**2
                        dindx = sqrt(dindx)

                        #print dindx, init_b, final_b, tg
                        if best_dindx == None:
                            best_dindx = dindx
                        else:
                            if dindx < best_dindx:
                                best_dindx = dindx
                                gcond = [init_b, final_b, tg]
                            else:
                                continue

        return gcond

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

    def getResMapPlot(self, model, flow=0.3, g_start_min=0.00, g_start_max=1.0, g_stop_min=0.1, g_stop_max=1.0, time_grad_min=2, time_grad_max=60):
        """ Plot the Resolution function of the different parameters
	    to optimize under gradient conditions
        """
        gcondlst = []
        reslst = []
        trlst = []
        step = 0.05
        for init_b in np.linspace(g_start_min, g_start_max, 20, endpoint=True):
            for final_b in np.linspace(g_stop_min, g_stop_max, 20, endpoint=True):
                for tg in drange(time_grad_min, time_grad_max,  2):
                    lsscc = None
                    lowest_alpha = None
                    if model == "lss":
                        lsscc, lowestrs = get_lss_gradient_critical_rs(self.c_lenght, self.c_particle, init_b, final_b, tg, flow, self.v_m, self.v_d, self.logkw_s_tab, crit_res=1.8)
                    else:#
                        lsscc, lowestrs = get_logss_gradient_critical_rs(self.c_lenght, self.c_particle, init_b, final_b, tg, flow, self.v_m, self.v_d, self.logkw_s_tab, crit_res=1.8)


                    if lsscc != None and len(lsscc) > 0:
                        totres = 0.
                        for i in range(len(lsscc)):
                            totres += lsscc[i][-1]
                        avgrs = totres/float(len(lsscc))
                        reslst.append(avgrs)
                        gcondlst.append([init_b, final_b, tg, self.flow, lowestrs])

                    else:
                        continue
        return gcondlst, reslst, trlst

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

    def optgradfun(self, grad):
        init_b = grad[0]
        final_b = grad[1]
        tg = grad[2]
        if final_b > 1 or final_b < 0 or init_b < 0 or init_b > 1 or tg < 0 or tg > self.maxtg or fabs(init_b-0.01) < 1e-1 or fabs(final_b-0.01) < 1e-1:
            return 9999
        else:
            #lsscc, lowestrs = get_lss_gradient_critical_rs(self.c_lenght, self.c_particle, init_b, final_b, tg, self.flow, self.v_m, self.v_d, self.logkw_s_tab, crit_res=2.0)
            lsscc, lowestsel = get_lss_gradient_critical_selectivity(self.c_lenght, self.c_particle, init_b, final_b, tg, self.flow, self.v_m, self.v_d, self.logkw_s_tab, 1.2)
            # lsscc: first two column correspond to the object id, the last to the rs associated

            if lowestsel != None:
                if lowestsel != 0:
                    return 1/lowestsel
                else:
                    return 9999
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
        best_rsmax = None
        best_gcond = None
        for init_b in drange(0.0, 0.2, 0.05):
            for final_b in drange(0.7, 1.0, 0.05):
                for tg in drange(self.tr_min, self.tr_max, 2.):
                    gcond = [init_b, final_b, tg]
                    tmp_bestgcond = fmin(self.optgradfun, gcond, side=[0.05, 0.05, 1], tol=1e-2)
                    tmp_rsmax = self.optgradfun(tmp_bestgcond)
                    if best_rsmax != None:
                        if tmp_rsmax < best_rsmax:
                            best_rsmax = tmp_rsmax
                            best_gcond = tmp_bestgcond
                        else:
                            continue
                    else:
                        best_gcond = tmp_bestgcond
                        best_rsmax = tmp_rsmax


        init_b = best_gcond[0]
        final_b = best_gcond[1]
        tg = best_gcond[2]

		# Function calculation
        deltafi = final_b - init_b
        t0 = self.v_m/self.flow
        td = self.v_d/self.flow

        tr = []
        for row in self.logkw_s_tab:
            b = float((self.v_m * deltafi * row[1]) / (tg*self.flow))
            k0 = pow(10, row[0] - (row[1] * init_b))
            tr.append(((t0/b) * log10(2.3*k0*b)) + t0 + td)
        # return the best condition, the retention times and the best rs average
        return best_gcond, tr, 1/best_rsmax

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
        for init_b in drange(g_start_min, g_start_max, 0.05):
            for final_b in drange(g_stop_min+init_b, g_stop_max, 0.05):
                for tg in drange(time_grad_min, time_grad_max,  1):
                    lsscc, lowestrs = get_lss_gradient_critical_rs(self.c_lenght, self.c_particle, init_b, final_b, tg, self.flow, self.v_m, self.v_d, self.logkw_s_tab, crit_res=2.0)
                    # lsscc: first two column correspond to the object id, the last to the rs associated
                    if lsscc != None:
                        totrs = 0.
                        for i in range(len(lsscc)):
                            totrs += lsscc[i][-1]
                        avgrs = totrs/float(len(lsscc))
                        gcondlst.append([init_b, final_b, tg, self.flow])
                        rslst.append(avgrs)
                    else:
                        continue

        return gcondlst, rslst, trlst

    def optloggradfun(self, grad):
        init_b = grad[0]
        final_b = grad[1]
        tg = grad[2]
        t0 = self.v_m/self.flow
        td = self.v_d/self.flow
        logssmol = SSGenerator(None, None, None, t0, self.v_d, self.flow)
        if final_b > 1 or final_b < 0 or init_b > final_b or init_b < 0 or init_b > 1 or tg < 0 or tg > self.maxtg:
            return 9999
        else:
            tr = []
            for i in range(len(self.logkw_s_tab)):
                logkw = self.logkw_s_tab[i][0]
                s = self.logkw_s_tab[i][1]
                try:
                    tr.append(logssmol.logrtpred(logkw, s, tg, init_b, final_b, t0, td))
                except:
                    continue

            if len(tr) == len(self.logkw_s_tab):
                mintr = min(tr)
                maxtr = max(tr)
                lower_lim =  t0+(t0*0.3)
                upper_lim = tg - (tg*0.1)
                if maxtr > upper_lim or mintr < lower_lim:
                    return 9999.
                else:
                    ss = 0.
                    for i in range(len(tr)):
                        for j in range(i, len(tr)):
                            ss += square(tr[i]-tr[j])

                    return 1/ss
            else:
                return 9999.

    def getloggradientconditions(self, tr_min, tr_max):
        """
        Optimize the logarithmic gradient conditions
        finding different value of flow rate,
        initial and final organic solvent and time gradient.
        The equation to be used are these and the equation for the resolution
        it is the same of the isocratic conditions.
        """
        self.maxtg = tr_max
        self.tr_min = tr_min
        self.tr_max = tr_max
        best_ss = None
        best_gcond = None

        for init_b in drange(0.00, 1.0, 0.1):
            for final_b in drange(init_b+0.1, 1.0, 0.1):
                for tg in drange(1, self.maxtg, 1):
                    gcond = [init_b, final_b, tg]
                    tmp_bestgcond = fmin(self.optloggradfun, gcond, side=[0.05, 0.05, 1], tol=1e-10)
                    tmp_ssmax = self.optloggradfun(tmp_bestgcond)
                    if best_ss != None:
                        if tmp_ssmax < best_ss:
                            best_ss = tmp_ssmax
                            best_gcond = tmp_bestgcond
                        else:
                            continue
                    else:
                        best_gcond = tmp_bestgcond
                        best_ss = tmp_ssmax

        """
        self.maxtg = 15
        gcond = [0.05, 1., 15]
        best_gcond = fmin(self.optloggradfun, gcond, side=[0.05, 0.05, 1], tol=1e-10)
        best_ss = self.optloggradfun(best_gcond)
        """
        init_b = best_gcond[0]
        final_b = best_gcond[1]
        tg = best_gcond[2]

		# Function calculation
        t0 = self.v_m/self.flow
        td = self.v_d/self.flow
        logssmol = SSGenerator(None, None, None, t0, self.v_d, self.flow)

        tr = []
        for i in range(len(self.logkw_s_tab)):
            logkw = self.logkw_s_tab[i][0]
            s = self.logkw_s_tab[i][1]
            tr.append(logssmol.logrtpred(logkw, s, tg, init_b, final_b, t0, td))

        # return the best condition, the retention times and the best rs average
        return best_gcond, tr, 1/best_ss
