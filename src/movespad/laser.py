"""Create emission spectrum of the laser"""

import numpy as np
import matplotlib.pyplot as plt
from movespad import params as pm
from tqdm import tqdm, trange
from scipy import stats


def gauss_1d(arr: np.ndarray, mean: float, sig: float) -> np.ndarray:
    """Normalized gaussian"""
    return 1 / (sig *np.sqrt(2*pm.PI)) * np.exp(-np.power(arr - mean, 2.) / (2 * np.power(sig, 2.)))


def _base_laser_spectrum(times: np.ndarray, mean, sigma, pulse_energy) -> np.ndarray:
    """Generate single gaussian"""
    return gauss_1d(times, mean, sigma) * pulse_energy
 

def full_laser_spectrum(init_offset, time_step, n_imps, tau, rho_tgt,
                        ff, pixel_area, f_lens, d_lens, theta_h, theta_v,
                        z, pulse_distance, sigma_laser, pulse_energy, array_len=None) -> np.ndarray:
    """
    Returns the normalized power spectrum of the laser.
    See Eq. 9 on the FBK paper

    """

    num = tau * rho_tgt * ff * pixel_area
    den = pm.PI * (f_lens/d_lens)**2 * np.tan(0.5 * theta_h)* np.tan(0.5 * theta_v) * (d_lens**2 + 4*z**2)

    base_len =  int(pulse_distance / time_step)

    full_spec = []

    for i in trange(n_imps, leave=False):
        mean = init_offset + i * pulse_distance
        base_spec = np.linspace(i*pulse_distance, (i+1)*pulse_distance, base_len)
        single_gauss = _base_laser_spectrum(base_spec, mean, sigma_laser, pulse_energy)

        full_spec.extend(single_gauss)

    pdf = np.asarray(full_spec) * num / den

    return pdf


def get_n_photons(times: np.ndarray, spectrum: np.ndarray, bin_width: int = 1):
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


def get_hist_data(times: list, clock: float, multi_hit: int) -> list:

    if len(times)==0:
        return

    imp_numbers = [t//clock for t in times]


    res = [times[0]%clock]
    count = 0

    for i, time in enumerate(times):
        if i==0:
            continue

        if times[i]//clock == times[i-1]//clock:
            if count < multi_hit:
                res.append(time%clock)
                count+=1
            else:
                continue
        else:
            count = 0
            res.append(time%clock)
            count += 1

    return res


def histo_avg(bin_centers, counts) ->float:

    return sum(np.multiply(np.asarray(bin_centers), np.asarray(counts)))/sum(counts)


def get_centroids(bins, counts, data, real_value):
    """
    Extract histogram centroids with the following methods:
    1. Bin with highest count ('max')
    2. Histogram mean ('mean')
    3. Mean of first 10% of bins ('10perc')
    4. Mean of gaussian fit ('gaus')
    """

    centr = {}

    bin_c = [0.5*(bins[i]+bins[i+1]) for i in range(len(bins)-1)] 

    centr['mean'] = 0.5 * pm.C * histo_avg(bin_c, counts) - real_value

    centr['max'] = 0.5 * pm.C * bin_c[np.argmax(counts)] - real_value

    sorted_counts, sorted_bins = zip(*sorted(zip(counts, bin_c), reverse=True))
    
    nz_bins = [bc for bc, cn in zip(sorted_bins, sorted_counts) if cn>0]
    nz_counts = [cn for _, cn in zip(sorted_bins, sorted_counts) if cn>0]
    chunk_10 = max(1, int(0.1*len(nz_counts)))

    centr['10perc'] = 0.5 * pm.C * histo_avg(nz_bins[:chunk_10], nz_counts[:chunk_10]) - real_value

    mu, sigma = stats.norm.fit(data)
    best_fit_line = stats.norm.pdf(bins, mu, sigma)
    
    centr['gaus'] = 0.5* pm.C *mu - real_value

    centr['z'] = real_value
 
    return centr, best_fit_line

