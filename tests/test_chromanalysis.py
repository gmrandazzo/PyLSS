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
from pylss.chromanalysis import ChromAnalysis

def test_peak_detection():
    # Create a simple signal with a Gaussian peak
    time = np.linspace(0, 10, 1000)
    # Peak at 5.0, width 0.5
    signal = np.exp(-(time - 5.0)**2 / (2 * 0.1**2))
    
    # Add some noise/baseline
    signal += 0.01
    
    analyzer = ChromAnalysis(time, signal, k=5, h=0.5)
    
    # S1 function should have a maximum at the peak
    # Let's check getPeaks
    # Actually getPeaks returns a list of indices where peak starts/ends or similar
    # Let's see how getPeaks is used in gui/chromanalyzer.py
    # pn = 1
    # peaks = chrom.getPeaks()
    # peaklst = chrom.peaksplit(peaks)
    
    peaks = analyzer.getPeaks()
    assert len(peaks) > 0
    
    # Split peaks
    peaklst = analyzer.peaksplit(peaks)
    assert len(peaklst) == 1
    
    # Check if the peak is centered around 5.0
    peak_times = [p[0] for p in peaklst[0]]
    peak_center = (min(peak_times) + max(peak_times)) / 2.0
    assert peak_center == pytest.approx(5.0, abs=0.1)

def test_integration():
    # Test peak integration
    time = np.linspace(0, 10, 1000)
    dt = time[1] - time[0]
    # Gaussian peak with area = sqrt(2*pi) * sigma
    sigma = 0.1
    signal = np.exp(-(time - 5.0)**2 / (2 * sigma**2))
    
    analyzer = ChromAnalysis(time, signal)
    
    # The integrate method in ChromAnalysis:
    # def integrate(self, y_vals, h):
    area = analyzer.integrate(signal, h=dt)
    
    expected_area = np.sqrt(2 * np.pi) * sigma
    assert area == pytest.approx(expected_area, rel=1e-3)
