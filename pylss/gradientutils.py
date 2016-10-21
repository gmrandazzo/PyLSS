'''
@package gradientutils

gradientutils was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
Geneve May 2016

gradientutils contains function which are used to estimate:
 - get_lss_gradient_critical_rs: critical couples with their resolutions for linear gradient
 - get_lss_gradient_critical_selectivity: critical couble with their selectivity for linear gradient
 - get_logss_gradient_critical_rs: critical couples with their resolutions for logarithmic gradient
 - get_logss_gradient_critical_selectivity: critical couble with their selectivity for linear gradient
'''

from ssengine import SSGenerator
from math import sqrt, isnan, log, fabs

def get_lss_gradient_critical_rs(c_lenght, c_particle, init_b, final_b, tg, flow, v_m, v_d, lssparam , crit_res=1.8):
    """Function to estimate critical couples and resolutions
       N.B.: The molecule id correspond to the exact position in lssparam.
    """
    if final_b > 1 or final_b < 0 or isnan(final_b) or init_b < 0 or init_b > 1 or isnan(init_b) or tg < 0 or isnan(tg):
        return None
    else:
        deltafi = final_b - init_b
        t0 = v_m/flow
        td = v_d/flow
        N = (c_lenght*10000.)/(3.4*c_particle)
        trtab = []
        lssmol = SSGenerator(None, None, None, t0, v_d, flow)
        i = 0
        for row in lssparam:
            lss_logkw = float(row[0])
            lss_s = float(row[1])
            b = (t0*(final_b-init_b)*lss_s)/tg
            # See D. Guillaume et al / J. Chromatogr. A 1216(2009) 3232-3243
            #W = (4*t0)/sqrt(N)* (1+ 1/(2.3*b))/4
            W = (12*t0)/sqrt(N)* (1+ 1/(2.3*b))
            try:
                tr_tmp = lssmol.rtpred(lss_logkw, lss_s, tg, init_b, final_b, t0, td)
                if tr_tmp < t0 or isnan(tr_tmp):
                    trtab.append([t0, W, i])
                else:
                    trtab.append([tr_tmp, W, i])
            except:
                trtab.append([t0, W, i])
            i += 1

        trtab = sorted(trtab, key=lambda x:x[0])
        if trtab[-1][0] > tg: #if the maximumt time is over the time gradient Error!!
            return None
        else:
            lstcc = []
            for i in range(1, len(trtab)):
                # Multiply by 1.7 to obtain the peak width at base.
                width1 = trtab[i][1] * 1.7
                width2 = trtab[i-1][1] * 1.7
                tr1 = trtab[i-1][0]
                tr2 = trtab[i][0]
                rs = (2.*(tr2-tr1)) / (width1+width2)
                if rs < crit_res:
                    # Save the original id of lssparam
                    lstcc.append([trtab[i-1][2], trtab[i][2], rs])
                else:
                    continue
            return lstcc

def get_lss_gradient_critical_selectivity(c_lenght, c_particle, init_b, final_b, tg, flow, v_m, v_d, lssparam , crit_alpha=1.1):
    """Function to estimate critical couples and selectivity
       N.B.: The molecule id correspond to the exact position in lssparam.
    """
    if final_b > 1 or final_b < 0 or isnan(final_b) or init_b < 0 or init_b > 1 or isnan(init_b) or tg < 0 or isnan(tg):
        return None, None
    else:
        deltafi = final_b - init_b
        t0 = v_m/flow
        td = v_d/flow
        N = (c_lenght*10000.)/(3.4*c_particle)
        trtab = []
        lssmol = SSGenerator(None, None, None, t0, v_d, flow)
        i = 0
        for row in lssparam:
            lss_logkw = float(row[0])
            lss_s = float(row[1])
            b = (t0*(final_b-init_b)*lss_s)/tg
            # See D. Guillaume et al / J. Chromatogr. A 1216(2009) 3232-3243
            #W = (4*t0)/sqrt(N)* (1+ 1/(2.3*b))/4
            W = (12*t0)/sqrt(N)* (1+ 1/(2.3*b))
            try:
                tr_tmp = lssmol.rtpred(lss_logkw, lss_s, tg, init_b, final_b, t0, td)
                if tr_tmp < t0 or isnan(tr_tmp) or tr_tmp > tg:
                    return None, None # these condition are not ok for selectivity calculations
                    #trtab.append([t0, W, i])
                else:
                    trtab.append([tr_tmp, W, i])
            except:
                return None, None # these condition are not ok for selectivity calculations
                #trtab.append([t0, W, i])
            i += 1

        trtab = sorted(trtab, key=lambda x:x[0])

        if trtab[-1][0] > tg or trtab[0][0]-t0 < 1: #if the maximumt time is over the time gradient Error!!
            return None, None
        else:
            lstcc = []
            lowest_alpha = None
            for i in range(1, len(trtab)):
                # Multiply by 1.7 to obtain the peak width at base.
                alpha = trtab[i][0] / trtab[i-1][0]
                if lowest_alpha != None:
                    if alpha < lowest_alpha:
                        lowest_alpha = alpha
                else:
                    lowest_alpha = alpha

                if alpha < crit_alpha:
                    # Save the original id of lssparam
                    lstcc.append([trtab[i-1][2], trtab[i][2], alpha])
                else:
                    continue
            
            if len(lstcc) > 0:
                return lstcc, lowest_alpha/float(len(lstcc))
            else:
                return lstcc, lowest_alpha

def get_logss_gradient_critical_rs(c_lenght, c_particle, init_b, final_b, tg, flow, v_m, v_d, lssparam , crit_res=1.8):
    """Function to estimate critical couples and resolutions for logarithmic gradient mode
       N.B.: The molecule id correspond to the exact position in lssparam.
    """
    if final_b > 1 or final_b < 0 or isnan(final_b) or init_b < 0 or init_b > 1 or isnan(init_b) or tg < 0 or isnan(tg):
        return None
    else:
        alpha = (final_b - init_b)/log10(tg+1)
        t0 = v_m/flow
        td = v_d/flow
        N = (c_lenght*10000.)/(3.4*c_particle)
        trtab = []
        logssmol = SSGenerator(None, None, None, t0, v_d, flow)
        i = 0
        for row in lssparam:
            lss_logkw = float(row[0])
            lss_s = float(row[1])
            b = lss_s * alpha
            #b = (t0*(final_b-init_b)*lss_s)/tg
            # See D. Guillaume et al / J. Chromatogr. A 1216(2009) 3232-3243
            #W = (4*t0)/sqrt(N)* (1+ 1/(2.3*b))/4
            W = (12*t0)/sqrt(N)* (1+ 1/(2.3*b))
            try:
                tr_tmp = logssmol.logrtpred(lss_logkw, lss_s, tg, init_b, final_b, t0, td)
                if tr_tmp < t0 or isnan(tr_tmp):
                    trtab.append([t0, W, i])
                else:
                    trtab.append([tr_tmp, W, i])
            except:
                trtab.append([t0, W, i])
            i += 1

        trtab = sorted(trtab, key=lambda x:x[0])
        if trtab[-1][0] > tg: #if the maximumt time is over the time gradient Error!!
            return None
        else:
            lstcc = []
            for i in range(1, len(trtab)):
                # Multiply by 1.7 to obtain the peak width at base.
                width1 = trtab[i][1] * 1.7
                width2 = trtab[i-1][1] * 1.7
                tr1 = trtab[i-1][0]
                tr2 = trtab[i][0]
                rs = (2.*(tr2-tr1)) / (width1+width2)
                if rs < crit_res:
                    # Save the original id of lssparam
                    lstcc.append([trtab[i-1][2], trtab[i][2], rs])
                else:
                    continue
            return lstcc


def get_logss_gradient_critical_selectivity(c_lenght, c_particle, init_b, final_b, tg, flow, v_m, v_d, lssparam, crit_alpha=1.1):
    """Function to estimate critical couples and resolutions for logarithmic gradient mode
       N.B.: The molecule id correspond to the exact position in lssparam.
    """
    if final_b > 1 or final_b < 0 or isnan(final_b) or init_b < 0 or init_b > 1 or isnan(init_b) or tg < 0 or isnan(tg):
        return None, None
    else:
        t0 = v_m/flow
        td = v_d/flow
        N = (c_lenght*10000.)/(3.4*c_particle)
        trtab = []
        logssmol = SSGenerator(None, None, None, t0, v_d, flow)
        i = 0
        for row in lssparam:
            lss_logkw = float(row[0])
            lss_s = float(row[1])
            try:
                tr_tmp = logssmol.logrtpred(lss_logkw, lss_s, tg, init_b, final_b, t0, td)
                if tr_tmp < t0 or isnan(tr_tmp):
                    return None, None # these condition are not ok for selectivity calculations
                else:
                    trtab.append([tr_tmp, i])
            except:
                return None, None # these condition are not ok for selectivity calculations
            i += 1

        if len(trtab) == len(lssparam):
            trtab = sorted(trtab, key=lambda x:x[0])
            lstcc = []
            lowest_alpha = (trtab[1][0] - t0) / (trtab[0][0]-t0)

            for i in range(1, len(trtab)):
                alpha = (trtab[i][0]-t0) / (trtab[i-1][0]-t0)
                #print trtab[i][0], trtab[i-1][0], t0, (trtab[i][0] - t0), (trtab[i-1][0]-t0)
                if alpha < lowest_alpha:
                    lowest_alpha = alpha

                if alpha < crit_alpha:
                    # Save the original id of lssparam
                    lstcc.append([trtab[i-1][1], trtab[i][1], alpha])

            return lstcc, lowest_alpha
        else:
            return None, None
