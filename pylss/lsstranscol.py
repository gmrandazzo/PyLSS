#!/usr/bin/env python

"""
This module try to find a linear relationship between logKw and S between two
column. The job is done by selecting a growing subset of object in which the
prediction error is analyzed in therms of LogKw and S and tr prediction.
The bootstrap method is used to analize this calculation and 10000 models are
generated to evaluate the transfer performancies. The final output is the list
of object to use to transfer from a column to an other minimizing the error as
best as possible.
"""

from math import sqrt, log10, ceil
from random import randint

def square(x):
    return x*x

class Point(object):
    def __init__(self, id, x, err):
        self.id = id
        self.x = x
        self.err = err

    def __lt__(self, other):
        return self.x < other.x


class LSSTranCol(object):
    def __init__(self, logkw_a, s_a, logkw_b, s_b, tg_b, init_B_b, final_B_b, t0_b, td_b, tr_b):
        """
        This function will assign the objet lss parameters
        """
        self.logkw_a = logkw_a
        self.s_a = s_a

        self.logkw_b = logkw_b
        self.s_b = s_b
        #Parameter to predict in B from A
        self.tg_b = tg_b
        self.init_B_b = init_B_b
        self.final_B_b = final_B_b
        self.t0_b = t0_b
        self.td_b = td_b
        self.tr_b = tr_b


    def split_train_test(self, X, ids):
        XTrain = []
        XTest = []
        objsz = len(X)
        for i in range(objsz):
            if i in ids:
                XTrain.append(X[i])
            else:
                XTest.append(X[i])
        return XTrain, XTest

    def build_pntlst(self, logkwmx, smx):
        x = [row[0] for row in logkwmx]
        y = [row[1] for row in logkwmx]
        m_logkw, k_logkw = self.linreg(x, y)
        logkwpred = self.linregpred(x, m_logkw, k_logkw)
        err1 = []
        for i in range(len(y)):
            err1.append(sqrt(square(y[i]-logkwpred[i])))
        x = [row[0] for row in smx]
        y = [row[1] for row in smx]
        m_s, k_s = self.linreg(x, y)
        spred = self.linregpred(x, m_s, k_s)
        err2 = []
        for i in range(len(y)):
            err2.append(sqrt(square(y[i]-spred[i])))

        ids = []
        plst = []
        for i in range(len(err1)):
            plst.append(Point(i, logkwmx[i][0], (err1[i]+err2[i])/2.))
        plst.sort()
        return plst

    def block_split_id(self, blocksz, plst):
        ids = []
        maxerror = 0.
        for i in range(len(plst)):
            maxerror += plst[i].err
        maxerror /= float(len(plst))

        step = int(ceil(len(plst)/float(blocksz)))
        k = 0
        for i in range(0, blocksz-1):
            while True:
                id_ = randint(k, k+step)
                if k+step < len(plst):
                    if plst[id_].err < maxerror:
                        ids.append(plst[id_].id)
                        k+=step
                        break
                    else:
                        continue
                else:
                    break;
        return ids

    def rndid(self, objsz, maxsize):
        """
        Split a matrix X in train and testset
        """
        ids = []
        for i in range(objsz):
            while True:
                id_ = randint(0, maxsize-1)
                if id_ in ids:
                    continue
                else:
                    ids.append(id_)
                    break;
        return ids

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

    def bootstrap(self):
        """
        Bootstrap function
        1. for each cycle from obj:10 to all obj:all-10 do:
        2.   split the all dataset in two: one of size obj for the model
             the latter used to predict the answer.
         3. Calculate the linear regression with the dataset one
         4. Calculate the linear regression prediction with the dataset two
         5. Store the error in a matrix in therms of:
            - error of logkw prediction
            - error of s prediction
            - error of tr prediction
        """
        XLogkw = []
        XS = []
        for i in range(len(self.logkw_a)):
            XLogkw.append([self.logkw_a[i], self.logkw_b[i]])
            XS.append([self.s_a[i], self.s_b[i]])

        logkwres = []
        sres = []
        trres = []
        selidserr = [0. for i in range(len(XLogkw)+1)] # collect id vs rsq for tr
        plst = self.build_pntlst(XLogkw, XS)
        for iteration in range(10000):
            #for obj in range(10, len(XLogkw)-10):
            for obj in range(5, 16):
                #get random split
                #ids = self.rndid(obj, len(XLogkw))
                # get id splitting by ordred block and minimizing the error.
                ids = self.block_split_id(obj, plst)
                # LogKw
                XTrain, XTest = self.split_train_test(XLogkw, ids)
                x = [row[0] for row in XTrain]
                y = [row[1] for row in XTrain]
                m_logkw, k_logkw = self.linreg(x, y)
                x = [row[0] for row in XTest]
                y = [row[1] for row in XTest]
                logkwpred = self.linregpred(x, m_logkw, k_logkw)
                rsq, err, rerr = self.linregerr(y, logkwpred)
                logkwres.append([m_logkw, k_logkw, rsq, err, rerr, len(ids)])

                # S
                XTrain, XTest = self.split_train_test(XS, ids)
                x = [row[0] for row in XTrain]
                y = [row[1] for row in XTrain]
                m_s, k_s = self.linreg(x, y)
                x = [row[0] for row in XTest]
                y = [row[1] for row in XTest]
                spred = self.linregpred(x, m_s, k_s)
                rsq, err, rerr = self.linregerr(y, spred)
                sres.append([m_s, k_s, rsq, err, rerr, len(ids)])

                # Calculate retention times from predicted logkw and s
                for i in range(len(self.tr_b[0])):
                    XTrain, XTest = self.split_train_test(self.tr_b, ids)
                    # XTrain is negligeable.
                    # XTest is to make the prediction error from tr
                    trpred = []
                    y = [row[i] for row in XTest]
                    for j in range(len(logkwpred)):
                        trpred.append(self.rtpred(logkwpred[j], spred[j], self.tg_b[i], self.init_B_b, self.final_B_b, self.t0_b, self.td_b))
                    rsq, err, rerr = self.linregerr(y, trpred)
                    for j in ids: # each id selectioned gives us a predictability
                        selidserr[j] += rerr
                        selidserr[-1] += 1
                    trres.append([rsq, err, rerr, len(ids), self.tg_b[i], self.init_B_b, self.final_B_b])
            #for i in range(len(selidserr)-1):
            #    selidserr[i] /= selidserr[-1]
        return logkwres, sres, trres, selidserr

    def linreg(self, x, y):
        """
        Do the linear regression:
        y = mx + k
        m = (Sum_i (x_i - x_med)(y_i - y_med)) / (Sum_i (x_i - x_med)^2)
        k = y_med - m*x_med
        """
        x_med = sum(x)/float(len(x))
        y_med = sum(y)/float(len(y))
        n = 0.
        d = 0.
        for i in range(len(x)):
            n += (x[i] - x_med)*(y[i]-y_med)
            d += square(x[i]-x_med)
        m = n/d
        k = y_med - m*x_med
        return m, k

    def linregpred(self, x, m, k):
        """
        Prediction of the y response from x with the relation:
        y = m*x + k
        """
        y = []
        for i in range(len(x)):
            y.append(x[i]*m + k)
        return y

    def linregerr(self, exp, pred):
        """
        Calcualte r squared from experimental v.s. predicted and the error
        """
        exp_med = sum(exp)/float(len(exp))
        rss = 0.
        tss = 0.
        rerr = 0.
        for i in range(len(exp)):
            rss += square(exp[i] - pred[i])
            rerr += square(exp[i] - pred[i])/exp[i]
            tss += square(exp[i] - exp_med)

        # return the rsquared and the average residual error
        return 1. - (rss/tss), sqrt(rss/float(len(exp))), rerr/float(len(exp))
