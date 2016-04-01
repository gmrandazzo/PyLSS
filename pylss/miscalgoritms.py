'''
@package miscalgoritms
miscalgoritms collects different methods and algorithms

miscalgoritms was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
Geneve Apr 2016
'''

def square(val):
    """ return the square of val"""
    return val*val

def drange(start, stop, step):
    """ create a list of float arithmetic progress"""
    r = start
    while r < stop:
        yield r
        r += step
