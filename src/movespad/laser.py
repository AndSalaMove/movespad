"""Create emission spectrum of the laser"""

import numpy as np
from movespad import params as pm


def gauss_1d(x: np.ndarray, mu: float, sig: float) -> np.ndarray:
    """Normalized gaussian"""
    return 1 / (sig *np.sqrt(2*pm.PI)) * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def _base_laser_spectrum(times: np.ndarray, sigma, n_reps=1) -> np.ndarray:
    norm_curve = gauss_1d(times, 1e-9, sigma) #mean at 1 ns

    norm_curve = norm_curve * pm.PULSE_ENERGY

    return norm_curve

def full_laser_spectrum(times: np.ndarray, n_peaks=1):
    """
    Returns the normalized power spectrum of the laser.
    See Eq. 9 on the FBK paper

    """

    num = pm.TAU_OPT * pm.RHO_TGT * pm.FF * pm.PIXEL_AREA
    den = pm.PI * pm.F_HASH**2 * np.tan(0.5 * pm.THETA_E_RAD)**2 * (pm.D_LENS**2 + 4*pm.Z**2)

    pdf = num / den * _base_laser_spectrum(times, pm.SIGMA_LASER)

    return pdf


def get_n_photons(times: np.ndarray, spectrum: np.ndarray):
    """Return number of photons generated for each bin.
    Photons are generated according to a Poisson process"""

    bin_width = 50 #TODO understand how to set this parameter
    delta_t = times[bin_width] - times[0]

    n_ph_mean = get_mean_n_ph(spectrum, delta_t, bin_width)
    n_ph = np.asarray([
        np.random.poisson(lmbd) for lmbd in n_ph_mean
    ])

    return n_ph

def get_mean_n_ph(spectrum, delta_t, bin_width) -> np.ndarray:

    tot_energies = np.asarray([s*delta_t for s in spectrum[::bin_width]])
    return tot_energies / pm.E_PH



if __name__ == '__main__':

    import matplotlib.pyplot as plt

    times = np.linspace(0, 5e-9, 5000) #1000 points / ns --> dt = 1 ps
    spectrum = full_laser_spectrum(times, pm.SIGMA_LASER) 

    plt.figure()
    plt.title("Laser power spectrum on the SPAD")
    plt.xlabel("Time [s]")
    plt.ylabel("Normalized power")
    plt.plot(times, spectrum)
    plt.show()

    area_tot = np.trapz(spectrum, times)
    E_ph = pm.H * pm.C / pm.PHOTON_WAVEL

    n_ph_tot = area_tot / E_ph
 
    print(f"Area totale (energia laser): {area_tot}")
    print(f"Energia fotone: {E_ph}")
    print(f"Numero fotoni arrivati: {n_ph_tot}")

    n_ph = get_n_photons(times, spectrum)

    breakpoint()