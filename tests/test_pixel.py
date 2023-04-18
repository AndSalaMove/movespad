"""Test for the Pixel class."""

import numpy as np
import random
from movespad import spad, pixel

T_DEAD_TEST = 1


def test_tdead():
    """Test the t dead filter (no afterpulsing)."""
    t_laser = [1, 2, 3.3, 3.9]
    t_bkg = [1.2, 1.5, 3.1, 4.2]

    pix = pixel.Pixel(size=1)
    pix.create_and_split(t_laser, t_bkg, pdp=1.0)
    pix.t_dead_filter(T_DEAD_TEST, pdp=1.0, ap_prob=0)

    assert pix.timestamps[0].timestamps == [spad.Timestamp(1), spad.Timestamp(3.1)]


# def test_afterpulse():
#     """Test the afterpulsing effect"""
#     timestamps = [spad.Timestamp(1), spad.Timestamp(2),spad.Timestamp(3),
#                   spad.Timestamp(4), spad.Timestamp(5)]

#     #np.random.seed(1234)
#     t_laser = [1, 2, 3.3, 3.9]
#     t_bkg = [1.2, 1.5, 3.1, 4.2]
#     pix = pixel.Pixel(size=1)
#     timestamps = pix.generate_afterpulse(timestamps, 0, 1, 1)

#     assert len(timestamps) == 6


# def test_crosstalk():
#     """Test the croostalking function."""

#     t_laser = [1, 2]
#     t_bkg = [1.2, 1.5, 3.1, 4.2]

#     np.random.seed(1235)
#     random.seed(1235)
#     pix = pixel.Pixel(size = 3)
#     pix.create_and_split(t_laser, t_bkg, pdp=1.0)
#     pix.print_timestamps()

#     probs = {
#          'r': 1,
#          'ur': 1
#     }

#     pix.crosstalk(probs)
#     pix.print_timestamps()

#     assert [el.time for el in pix.timestamps[0].timestamps] == []
#     assert [el.time for el in pix.timestamps[1].timestamps] == []
#     assert [el.time for el in pix.timestamps[2].timestamps] == []
#     assert [el.time for el in pix.timestamps[3].timestamps] == [1]


# if __name__ == '__main__':
#       test_crosstalk()
