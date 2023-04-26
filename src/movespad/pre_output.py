import numpy as np
import matplotlib.pyplot as plt
from movespad import laser, pixel, params as pm
from tqdm import trange

def fl(x: str):
    return float(x)

def optimal_laser_power(params):
    """Simulate SPAD action to evaluate
    optimal laser power (6 hits out of 9)"""

    hit_counts = []
    pulse_distance = fl(params['pulse_distance'])*1e-6
    time_step = 100e-12
    en = np.sqrt(2*pm.PI)*fl(params['laser_sigma'])*1e-9*fl(params['pixel_power'])
    n_imps = 1
    for _ in trange(250, leave=False):
        laser_spec = laser.full_laser_spectrum(
            init_offset= 2*fl(params['z'])/pm.C,
            time_step= 100e-12,
            n_imps=n_imps,
            tau = fl(params['tau']),
            rho_tgt= fl(params['rho_tgt']),
            ff= fl(params['ff']),
            pixel_area= (fl(params['pixel_size'])*1e-6*fl(params['spad_size']))**2,
            f_lens = fl(params['f_lens'])*1e-3,
            d_lens = fl(params['d_lens'])*1e-3,
            theta_h= fl(params['theta_h'])*1e-3,
            theta_v= fl(params['theta_v'])*1e-3,
            z = fl(params['z']),
            pulse_distance= pulse_distance,
            sigma_laser= fl(params['laser_sigma'])*1e-9,
            pulse_energy=en
        )

        start, stop = 0, pulse_distance * n_imps
        n_steps = int((stop-start)/time_step)
        times = np.linspace(start, stop, n_steps)

        n_laser, t_laser = laser.get_n_photons(times, laser_spec, 1)
        t_bkg = np.array([])
        pix = pixel.Pixel(size=3)
        pix.create_and_split(t_laser, t_bkg, pdp=fl(params['pdp']))

        hit_counts.append(sum([len(spd.timestamps)>0 for spd in pix.timestamps])) 

    return np.mean(hit_counts)

def get_pre_output(params):
    """
    Compute average hit count, flash power per pixel,
    matrix dimension to cover all FOV, N bit for TDC
    """
    pre_out = {}

    # Optimal laser power (6 hits out of 9)
    hit_counts  = optimal_laser_power(params)
    pre_out['hit_counts'] = hit_counts

    # Matrix size
    scene_x = fl(params['range_max']) * np.tan(np.deg2rad(fl(params['fov_x'])) / 2)
    scene_y = fl(params['range_max']) * np.tan(np.deg2rad(fl(params['fov_y'])) / 2)

    n_pix_x = np.ceil(scene_x / (fl(params['res_x'])/100))
    n_pix_y = np.ceil(scene_y / (fl(params['res_y'])/100))

    pre_out['n_pix_x'], pre_out['n_pix_y'] = n_pix_x, n_pix_y


    # Power per pixel in case of flash
    laser_sigma = fl(params['laser_sigma'])*1e-9
    pulse_distance = max(2*fl(params['range_max'])*1.05 / pm.C, 8*laser_sigma*n_pix_y)
    pb = fl(params['power_budget'])
    n_pixel = n_pix_x * n_pix_y

    power_per_pixel = pb / n_pixel
    flash_power_per_pixel = power_per_pixel * pulse_distance / (np.sqrt(2*pm.PI)*laser_sigma)

    pre_out['flash_ppp'] = np.round(flash_power_per_pixel, 2)

    # N bits for tdc

    t_max = 2*fl(params['range_max'])/pm.C
    t_min = 2*fl(params['range_min'])/pm.C

    histo_width = t_max - t_min
    bin_width = min(fl(params['res_x'])/100, fl(params['res_y'])/100) / pm.C
    n_bins = np.ceil(histo_width/bin_width)
    n_bit = np.ceil(np.log2(n_bins))

    pre_out['n_bit_tdc'] = n_bit

    return pre_out


if __name__ == '__main__':
    pass