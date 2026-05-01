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

import pytest
import numpy as np
from pylss.optimizer import simplex

def test_simplex_quadratic():
    # Test optimizer with a simple quadratic function: f(x, y) = (x-2)^2 + (y-3)^2
    def quadratic(x):
        return (x[0] - 2.0)**2 + (x[1] - 3.0)**2
    
    xstart = [0.0, 0.0]
    side = [0.1, 0.1]
    
    result = simplex(quadratic, xstart, side, tol=1.0e-10)
    
    assert result[0] == pytest.approx(2.0, abs=1e-6)
    assert result[1] == pytest.approx(3.0, abs=1e-6)

def test_simplex_rosenbrock():
    # Test optimizer with Rosenbrock function
    def rosenbrock(x):
        return (1.0 - x[0])**2 + 100.0 * (x[1] - x[0]**2)**2
    
    xstart = [0.0, 0.0]
    side = [0.1, 0.1]
    
    result = simplex(rosenbrock, xstart, side, tol=1.0e-10, iterations=5000)
    
    assert result[0] == pytest.approx(1.0, abs=1e-4)
    assert result[1] == pytest.approx(1.0, abs=1e-4)
