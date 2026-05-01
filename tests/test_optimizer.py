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
