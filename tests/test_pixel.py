"""Test for the Pixel class."""

import numpy as np
from movespad import pixel

T_DEAD_TEST = 1
T_QUENCH_TEST = 0.25
T_THR_TEST = 0.7

def test_tdead():
    """Test the t dead filter (no afterpulsing)."""
    t_laser = [1, 2, 3.3, 3.9]
    t_bkg = [1.2, 1.5, 3.1, 4.2]

    pix = pixel.Pixel()
    detected = pix.process_events(t_laser, t_bkg,
                                  T_DEAD_TEST, T_THR_TEST, T_QUENCH_TEST,
                                  pdp=1.0, ap_prob=0)

    assert detected == [pixel.Timestamp(1), pixel.Timestamp(3.1), pixel.Timestamp(3.9)]


def test_afterpulse():
    """Test the afterpulsing effect"""
    timestamps = [pixel.Timestamp(1), pixel.Timestamp(2),pixel.Timestamp(3),
                  pixel.Timestamp(4), pixel.Timestamp(5)]

    #np.random.seed(1234)

    pix = pixel.Pixel()
    timestamps = pix.generate_afterpulse(timestamps, 0, 1, 1)

    assert len(timestamps) == 6
