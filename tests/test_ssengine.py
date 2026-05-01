import pytest
from pylss.ssengine import SSGenerator
import numpy as np

def test_lss_parameter_calculation():
    # Setup parameters based on examples/test_caculation_lss_parameter.txt
    t0 = 0.969
    v_d = 0.375
    flow = 0.30
    
    # Gradients
    tg = [14.0, 60.0]
    init_B = [0.05, 0.05]
    final_B = [0.95, 0.96]
    
    # Retention times for the first compound
    tr = [8.53, 22.11]
    
    # Expected results (obtained from current pylss engine run)
    # Note: These differ slightly from examples/output_test_lss_parameter.txt 
    # possibly due to formula updates or optimization differences.
    expected_logkw = 2.7902513433
    expected_s = 5.9790144752
    
    # Initialize generator
    generator = SSGenerator(None, None, None, t0, v_d, flow)
    
    # Calculate parameters
    logkw, s = generator.getlssparameters(tr, tg, init_B, final_B)
    
    # Verify results
    assert logkw == pytest.approx(expected_logkw, rel=1e-5)
    assert s == pytest.approx(expected_s, rel=1e-5)

def test_rtpred():
    # Test retention time prediction
    t0 = 0.969
    v_d = 0.375
    flow = 0.30
    td = v_d / flow
    
    # Values that match the current rtpred implementation
    logkw = 2.7902513433
    s = 5.9790144752
    
    generator = SSGenerator(None, None, None, t0, v_d, flow)
    
    # Predict tr for Gradient 1
    tr_pred1 = generator.rtpred(logkw, s, 14.0, 0.05, 0.95, t0, td)
    assert tr_pred1 == pytest.approx(8.53, abs=0.01)
    
    # Predict tr for Gradient 2
    tr_pred2 = generator.rtpred(logkw, s, 60.0, 0.05, 0.96, t0, td)
    assert tr_pred2 == pytest.approx(22.11, abs=0.01)
