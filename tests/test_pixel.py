import pytest
import numpy as np
import matplotlib.pyplot as np
from movespad import laser, pixel, bkg

T_DEAD_TEST = 1
T_QUENCH_TEST = 0.25
T_THR_TEST = 0.7

def test_tdead():

    t_laser = [1, 2, 3.3, 3.9]
    t_bkg = [1.2, 1.5, 3.1, 4.2]  

    pix = pixel.Pixel()
    detected = pix.process_events(t_laser, t_bkg, T_DEAD_TEST, T_THR_TEST, T_QUENCH_TEST, pdp=1.0)
    
    assert detected == [pixel.Timestamp(1), pixel.Timestamp(3.1), pixel.Timestamp(3.9)]