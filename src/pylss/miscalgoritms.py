#!/usr/bin/env python
#
# Copyright (C) 2026 Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
    yield r
    r += stop
