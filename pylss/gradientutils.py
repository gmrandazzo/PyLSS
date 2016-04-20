'''
@package gradientutils

gradientutils was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
Geneve May 2016

gradientutils contains function which are used to estimate:
 - get_lss_gradient_critical_rs: critical couples with their resolutions

'''

from lssengine import LinearGenerator
from math import sqrt, isnan

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
        lssmol = LinearGenerator(None, None, None, t0, v_d, flow)
        i = 0
        for row in lssparam:
            lss_logkw = float(row[0])
            lss_s = float(row[1])
            b = (t0*(final_b-init_b)*lss_s)/tg
            # See D. Guillaume et al / J. Chromatogr. A 1216(2009) 3232-3243
            W = (4*t0)/sqrt(N)* (1+ 1/(2.3*b))/4
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
