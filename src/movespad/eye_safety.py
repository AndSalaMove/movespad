"""Module to compute eye safety class for the laser."""

import numpy as np
import movespad.params as pm
from pprint import pprint
import argparse




def area_at(distance: float):
    """Laser ellipse area at a distance d"""
    #probably this works only in the far field approx.

    r_x = distance * np.tan(pm.THETA_H / 2)
    r_y = distance * np.tan(pm.THETA_V / 2)
    print(f"Distance: {distance}m")
    print(f"Divergence: {pm.THETA_H} x {pm.THETA_V}")
    print(f"Width: {(2*r_x)*1000:.2f}mm, Height: {(2*r_y)*1000:.2f}mm")
    print(f"Area: {np.pi * r_x * r_y * 1e6:.5f} mm2")
    return np.pi * r_x * r_y


def single_pulse_energy(d):

    pup_area = np.pi * 3.5e-3 ** 2
    en = pm.PULSE_ENERGY * pup_area / area_at(d)
   
    status = 'ok' if en < 514e-9 else 'fail'

    rep_rate = 1. / pm.PULSE_DISTANCE

    power = en * rep_rate
    status_power = 'ok' if power < 1e-3 else 'fail'

    N = pm.PULSE_DISTANCE / 18e-6
    C5 = N ** (-0.25)

    Ninv = 18e-6 * rep_rate
    
    ael = en * Ninv
    status_ael = 'ok' if ael < 497e-9 else 'fail'

    print(f"Distance: {d} - POWER: {pm.PULSE_POWER}")

    return {

        'energy': en,
        'status_energy': status,
        'power': power,
        'status_power': status_power,
        'ael': ael,
        'status_ael': status_ael
    }


if __name__ == '__main__':

    # parser = argparse.ArgumentParser('eye_safety.py')
    # parser.add_argument('-d', type=float, required=True, help='distance')
    
    # args = parser.parse_args()

    # result = single_pulse_energy(args.d)
    # pprint(result)
    area_at(14e-3)