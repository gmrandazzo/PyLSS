'''
@package optimizer

optimizer was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
Geneve July 2014

optimizer will implement the Nelder-Mead method.

Reference at:
Numerical Methods in Enginering with Python 3

Jaan Kiusalaas
Cambridge 2013
'''

from numpy import zeros, sum, dot
from math import sqrt

def simplex(fun, xstart, side, tol=1.0e-6, iterations=1000):
    """ Compute the simplex nelde-mead method
    fun: function
	    define the function to optimize
	xstart: list
	    define the starting simplex point and is a list
	side: list
	    define the size increasment by the simplex
	tol: float

	"""
    n = len(xstart) # Nunmber of variables

    x = zeros((n+1, n))
    f = zeros(n+1)

    def argmax(lst):
        """ search argmax in a list"""
        id_amax = 0
        amax = lst[id_amax]
        for i in range(1, len(lst)):
            if lst[i] < amax:
                continue
            else:
                amax = lst[i]
                id_amax = i
        return id_amax

    def argmin(lst):
        """ search argmin in a list """
        id_amin = 0
        amin = lst[id_amin]
        for i in range(1, len(lst)):
            if amin > lst[i]:
                amin = lst[i]
                id_amin = i
            else:
                continue
        return id_amin

    # Generate starting simplex
    x[0] = xstart
    for i in range(1, n+1):
        x[i] = xstart
        x[i][i-1] = xstart[i-1] + side[i-1]
    # Compute values of F at the vertices of the simplex
    for i in range(n+1):
        f[i] = fun(x[i])

    # Main loop
    k = 0
    while k < iterations:
        # Find highest and lowest vertices
        iLo = argmin(f)
        iHi = argmax(f)
        # Compute the move vector d
        d = (-(n+1)*x[iHi] + sum(x, axis=0))/n
        # Check for convergence
        if sqrt(dot(d, d)/n) < tol:
            return x[iLo]

        # Try reflection
        xNew = x[iHi] + 2.0*d
        fNew = fun(xNew)
        if fNew <= f[iLo]:        # Accept reflection
            x[iHi] = xNew
            f[iHi] = fNew
            # Try expanding the reflection
            xNew = x[iHi] + d
            fNew = fun(xNew)
            if fNew <= f[iLo]:    # Accept expansion
                x[iHi] = xNew
                f[iHi] = fNew
        else:
            # Try reflection again
            if fNew <= f[iHi]:    # Accept reflection
                x[iHi] = xNew
                f[iHi] = fNew
            else:
                # Try contraction
                xNew = x[iHi] + 0.5*d
                fNew = fun(xNew)
                if fNew <= f[iHi]: # Accept contraction
                    x[iHi] = xNew
                    f[iHi] = fNew
                else:
                    # Use shrinkage
                    for i in range(len(x)):
                        if i != iLo:
                            x[i] = (x[i] - x[iLo])*0.5
                            f[i] = fun(x[i])
        k += 1
    return x[iLo]
