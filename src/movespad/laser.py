"""Create emission spectrum of the laser"""

import numpy as np
import matplotlib.pyplot as plt
from movespad import params as pm


def gauss_1d(x: np.ndarray, mu: float, sig: float) -> np.ndarray:
    """Normalized gaussian"""
    return 1 / (sig *np.sqrt(2*pm.PI)) * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def _base_laser_spectrum(times: np.ndarray, mu, sigma, n_reps=1) -> np.ndarray:
    norm_curve = gauss_1d(times, mu, sigma) #mean at 1 ns

    norm_curve = norm_curve * pm.PULSE_ENERGY

    return norm_curve


def full_laser_spectrum(times: np.ndarray, time_limit: float, init_offset: float):
    """
    Returns the normalized power spectrum of the laser.
    See Eq. 9 on the FBK paper

    """

    num = pm.TAU_OPT * pm.RHO_TGT * pm.FF * pm.PIXEL_AREA
    den = pm.PI * pm.F_HASH**2 * np.tan(0.5 * pm.THETA_E_RAD)**2 * (pm.D_LENS**2 + 4*pm.Z**2)

    spec = np.zeros_like(times)
    current_time = init_offset
    while current_time <= time_limit:
        spec += _base_laser_spectrum(times, current_time, pm.SIGMA_LASER)
        current_time += pm.PULSE_DISTANCE
    
    pdf = num / den * spec

    return pdf


def get_n_photons(times: np.ndarray, spectrum: np.ndarray, bin_width: int):
    """Return number of photons generated for each bin.
    Photons are generated according to a Poisson process"""

    #TODO understand how to set this parameter
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
    
    ax.plot(times, spectrum, label=label)



if __name__ == '__main__':

    import matplotlib.pyplot as plt

    times = np.linspace(0, 5e-9, 5000) #1000 points / ns --> dt = 1 ps
    spectrum = full_laser_spectrum(times)
    bin_width = 50 #* 1ps = 50 ps

    plt.figure()
    plt.title("Laser power spectrum on the SPAD")
    plt.xlabel("Time [s]")
    plt.ylabel("Power")
    plt.plot(times, spectrum)
    plt.show()

    area_tot = np.trapz(spectrum, times)
    E_ph = pm.H * pm.C / pm.PHOTON_WAVEL

    n_ph_tot = area_tot / E_ph
 
    print(f"Area totale (energia laser): {area_tot}")
    print(f"Energia fotone: {E_ph}")
    print(f"Numero fotoni arrivati: {n_ph_tot}")

    n_ph, laser_timestamps = get_n_photons(times, spectrum)