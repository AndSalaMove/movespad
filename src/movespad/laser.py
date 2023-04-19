"""Create emission spectrum of the laser"""

import numpy as np
import matplotlib.pyplot as plt
from movespad import params as pm
from tqdm import tqdm, trange


def gauss_1d(arr: np.ndarray, mean: float, sig: float) -> np.ndarray:
    """Normalized gaussian"""
    return 1 / (sig *np.sqrt(2*pm.PI)) * np.exp(-np.power(arr - mean, 2.) / (2 * np.power(sig, 2.)))


def _base_laser_spectrum(times: np.ndarray, mean, sigma) -> np.ndarray:
    """Generate single gaussian"""
    return gauss_1d(times, mean, sigma) * pm.PULSE_ENERGY
 

def full_laser_spectrum(init_offset, time_step, n_imps):
    """
    Returns the normalized power spectrum of the laser.
    See Eq. 9 on the FBK paper

    """

    num = pm.TAU_OPT * pm.RHO_TGT * pm.FF * pm.PIXEL_AREA
    den = pm.PI * pm.F_HASH**2 * np.tan(0.5 * pm.THETA_H)* np.tan(0.5 * pm.THETA_V) * (pm.D_LENS**2 + 4*pm.Z**2)

    base_len =  int(pm.PULSE_DISTANCE / time_step)

    full_spec = []

    for i in trange(n_imps, leave=False):
        mean = init_offset + i * pm.PULSE_DISTANCE 
        base_spec = np.linspace(i*pm.PULSE_DISTANCE, (i+1)*pm.PULSE_DISTANCE, base_len)
        single_gauss = _base_laser_spectrum(base_spec, mean, pm.SIGMA_LASER)

        full_spec.extend(single_gauss)

    pdf = np.asarray(full_spec) * num / den

    return pdf


def get_n_photons(times: np.ndarray, spectrum: np.ndarray, bin_width: int):
    """Return number of photons generated for each bin.
    Photons are generated according to a Poisson process"""

    delta_t = times[bin_width] - times[0]

    n_ph_mean = get_mean_n_ph(spectrum, delta_t, bin_width)

    n_ph = np.asarray([
        np.random.poisson(lmbd) for lmbd in n_ph_mean
    ])

    return n_ph, times[::bin_width][n_ph >= 1]


def get_mean_n_ph(spectrum, delta_t, bin_width) -> np.ndarray:
    """Return expected number of photons for each time bin."""
    tot_energies = np.asarray([s*delta_t for s in spectrum[::bin_width]])
    return tot_energies / pm.E_PH


def plot_spectrum(times, spectrum, ax, label):
    """Plot laser and bkg spectrum"""
    ax.plot(times, spectrum, label=label)


def get_hist_data(times, clock):

    res = [times[0]%clock]

    for i, time in enumerate(times):
        if i==0:
            continue

        if times[i]//clock == times[i-1]//clock:
            continue
        else:
            res.append(time%clock)

    return res


if __name__ == '__main__':

    print(get_hist_data([1,13,14,15,34,36,42], 10)    )