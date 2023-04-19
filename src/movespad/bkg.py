"""Modelling background light impinging on the spad pixels"""

import numpy as np
import matplotlib.pyplot as plt
from movespad import params as pm
import movespad.laser as laser

from tqdm import trange, tqdm


def bkg_spectrum(times: np.ndarray) -> np.ndarray:
    """Generate physical background power spectrum.
    It is a sum of 2 Poisson processes:
    + physical background
    + Dark Count Rate
    """

    pdf = np.ones_like(times)

    num = pm.TAU_OPT * pm.RHO_TGT * pm.FF * pm.PIXEL_AREA * pm.Z**2
    den = pm.F_HASH**2 * (4 * pm.Z**2 + pm.D_LENS**2)

    pdf = num / den * pdf * pm.BKG_POWER
    return pdf


def get_n_photons_bkg(times, bkg_spectrum, bin_width):
    """
    Generate mean values from a Poisson process including
    physical background and Dark Count Rate.
    """
    delta_t = times[bin_width]-times[0]
    
    lam_bkg = laser.get_mean_n_ph(bkg_spectrum, delta_t, bin_width)[0]
    lam_dcr = pm.DCR * delta_t

    n_ph = np.asarray([
        np.random.poisson(lam= lam_bkg+lam_dcr) for _ in times[::bin_width]
    ])

    return n_ph, times[::bin_width][n_ph >= 1]