"""Test for the Pixel class."""

import numpy as np
from movespad import spad

T_DEAD_TEST = 1


def test_tdead():
    """Test the t dead filter (no afterpulsing)."""
    t_laser = [1, 2, 3.3, 3.9]
    t_bkg = [1.2, 1.5, 3.1, 4.2]

    spa = spad.Spad()
    detected = spa.process_events(t_laser, t_bkg,
                                  T_DEAD_TEST, pdp=1.0, ap_prob=0)

    assert detected == [spad.Timestamp(1), spad.Timestamp(3.1)]


def test_afterpulse():
    """Test the afterpulsing effect"""
    timestamps = [spad.Timestamp(1), spad.Timestamp(2),spad.Timestamp(3),
                  spad.Timestamp(4), spad.Timestamp(5)]

    #np.random.seed(1234)

    spa = spad.Spad()
    timestamps = spa.generate_afterpulse(timestamps, 0, 1, 1)

    assert len(timestamps) == 6
