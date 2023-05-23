import numpy as np
import matplotlib.pyplot as plt
from movespad import laser, pixel, params as pm
from tqdm import trange
from copy import deepcopy

def fl(x: str):
    return float(x)


def optimal_laser_power(params, mode=None):
    """Simulate SPAD action to evaluate
    optimal laser power (6 hits out of 9)"""

    if params['seed']!='':
        np.random.seed(int(params['seed']))
    hit_counts = []

    time_step = 100e-12
    en = np.sqrt(2*pm.PI)*fl(params['laser_sigma'])*1e-9*fl(params['pixel_power'])
    n_imps = 1
    limit = .5e-6

    print(f"Pulse energy: {en}")
    n_las = []

    for _ in trange(250, leave=False):
        laser_spec = laser.full_laser_spectrum(
            init_offset= 1e-8,
            time_step= time_step,
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
            pulse_distance= limit,
            sigma_laser= fl(params['laser_sigma'])*1e-9,
            pulse_energy=en,
            array_len=None
        )

        start, stop = 0, limit * n_imps
        n_steps = int((stop-start)/time_step)
        times = np.linspace(start, stop, n_steps)

        n_laser, t_laser = laser.get_n_photons(times, laser_spec)
        n_las.append(sum(n_laser))
        t_bkg = np.array([])
        pix = pixel.Pixel(size=3)
        pix.create_and_split(t_laser, t_bkg, pdp=fl(params['pdp']))

        hit_counts.append(sum([len(spd.timestamps)>0 for spd in pix.timestamps])) 
    print(f"Average n photons: {np.mean(n_las)}")
    return np.mean(hit_counts)


def get_pre_output(params):

    """
    Compute average hit count, flash power per pixel,
    matrix dimension to cover all FOV, N bit for TDC
    """
    print("")
    f_lens = 0.1 * fl(params['range_max']) * fl(params['spad_size']) * int(params['pixel_size']) / fl(params['res_x'])
    d_lens = f_lens / float(params['f_number'])

    params['f_lens'] = f_lens
    params['d_lens'] = d_lens

    pre_out = {
        'f_lens': f_lens,
        'd_lens': d_lens,
        'flash_mn': get_pre_output_flash_fix_mn(deepcopy(params)),
        'flash_fov': get_pre_output_flash_fix_fov(deepcopy(params)),
        'scanning_k': get_pre_output_scan_fix_k(deepcopy(params)),
        'scanning_Pp': get_pre_output_scan_fix_p(deepcopy(params))
    }

    return pre_out


def get_pre_output_flash_fix_mn(params):
    """Matrix size is fixed (given by input). 
    Calculate the FOV"""

    n_sigma_recharge = int(params['n_sigma_recharge'])
    res_x, res_y = fl(params['res_x'])/100, fl(params['res_y'])/100
    range_max, laser_sigma = fl(params['range_max']), fl(params['laser_sigma'])*1e-9
    n_x, n_y = int(params['h_matrix']), int(params['v_matrix'])
    pb, clock = fl(params['power_budget']), fl(params['clock'])*1e6
    fps, n_pads = int(params['fps']), int(params['n_pads'])
    n_bit_tdc, n_bit_hist = int(params['n_bit_tdc_pre']), int(params['n_bit_hist_pre'])

    fov_x, fov_y = np.rad2deg(2*np.arctan(n_x * res_x / range_max)), np.rad2deg(2*np.arctan(n_y * res_y / range_max))
    fov_x, fov_y = np.round(fov_x, 2), np.round(fov_y, 2)
    pulse_distance = max(2*range_max*1.05 / pm.C, n_sigma_recharge*laser_sigma)
    power_per_pixel = pb / (n_x * n_y)
    flash_power_per_pixel = power_per_pixel * pulse_distance / (np.sqrt(2*pm.PI)*laser_sigma)
    laser_peak_power = flash_power_per_pixel * n_x * n_y

    time_per_frame = 1 / fps - (n_x * n_y * n_bit_tdc * n_bit_hist) / (clock*n_pads)
    imps_per_frame = int(np.floor(time_per_frame/pulse_distance))

    params['pixel_power'] = flash_power_per_pixel
    # print(f"Flash (fix matrix) - Power per pixel {params['pixel_power']:.2f}")
    hit_count = optimal_laser_power(params)

    pre_outs = {
        'fov': (fov_x, fov_y),
        'matrix_size': (n_x, n_y),
        'Pp': flash_power_per_pixel,
        'tot_peak': laser_peak_power,
        'n_imps': imps_per_frame,
        'hit_count' : hit_count
    }

    return pre_outs


def get_pre_output_flash_fix_fov(params):
    """FOV_x, FOV_y are fixed. Calculate flash matrix size
    and everything that follows."""

    n_sigma_recharge = int(params['n_sigma_recharge'])
    res_x, res_y = fl(params['res_x'])/100, fl(params['res_y'])/100
    range_max, laser_sigma = fl(params['range_max']), fl(params['laser_sigma'])*1e-9
    fov_x, fov_y = float(params['fov_x']), float(params['fov_y'])
    pb, clock = fl(params['power_budget']), fl(params['clock'])*1e6
    fps, n_pads = int(params['fps']), int(params['n_pads'])
    n_bit_tdc, n_bit_hist = int(params['n_bit_tdc_pre']), int(params['n_bit_hist_pre'])

    n_x = int(np.ceil((range_max * np.tan(np.deg2rad(0.5*fov_x)) / res_x)))
    n_y = int(np.ceil((range_max * np.tan(np.deg2rad(0.5*fov_y)) / res_y)))


    pulse_distance = max(2*range_max*1.05 / pm.C, n_sigma_recharge*laser_sigma)
    power_per_pixel = pb / (n_x * n_y)
    flash_power_per_pixel = power_per_pixel * pulse_distance / (np.sqrt(2*pm.PI)*laser_sigma)
    laser_peak_power = flash_power_per_pixel * n_x * n_y

    time_per_frame = 1 / fps - (n_x * n_y * n_bit_tdc * n_bit_hist) / (clock*n_pads)
    imps_per_frame = int(np.floor(time_per_frame/pulse_distance))

    params['pixel_power'] = flash_power_per_pixel
    # print(f"Flash (fix FOV) - Power per pixel {params['pixel_power']:.2f}")
    hit_count = optimal_laser_power(params)

    pre_outs = {
        'fov': (fov_x, fov_y),
        'matrix_size': (n_x, n_y),
        'Pp': flash_power_per_pixel,
        'tot_peak': laser_peak_power,
        'n_imps': imps_per_frame,
        'hit_count' : hit_count
    }

    return pre_outs


def get_pre_output_scan_fix_k(params):
    """Scanning mode. We fix k, which is the number of pixels
    that can be hit with a single shot"""

    n_sigma_recharge = int(params['n_sigma_recharge'])
    fov_x, fov_y = fl(params['fov_x']), fl(params['fov_y'])
    res_x, res_y = fl(params['res_x'])/100, fl(params['res_y'])/100
    range_max, laser_sigma = fl(params['range_max']), fl(params['laser_sigma'])*1e-9
    n_x, n_y = fl(params['h_matrix']), fl(params['v_matrix'])
    pb, clock = fl(params['power_budget']), fl(params['clock'])*1e6
    fps, n_pads = int(params['fps']), int(params['n_pads'])
    n_bit_tdc, n_bit_hist = int(params['n_bit_tdc_pre']), int(params['n_bit_hist_pre'])
    k_pix = int(params['k_pix'])

    power_per_pixel = n_sigma_recharge * pb / (np.sqrt(2*np.pi) * k_pix)

    n_x_tot = int(np.ceil((range_max * np.tan(np.deg2rad(0.5*fov_x)) / res_x)))
    n_y_tot = int(np.ceil((range_max * np.tan(np.deg2rad(0.5*fov_y)) / res_y)))

    n_matrices = int(np.ceil(n_x_tot/n_x) * np.ceil(n_y_tot/n_y))

    k_pix_per_shot = int(np.floor(n_sigma_recharge * pb / (np.sqrt(2*np.pi) * power_per_pixel)))
    n_shots = int(np.ceil(n_x * n_y / k_pix_per_shot))
    pulse_distance = max(2*float(params['range_max'])*1.05 / pm.C, n_shots*n_sigma_recharge*laser_sigma)
    #print(f"[FIX p]Pulse distance: {pulse_distance:.2E} s - {0.5 * pm.C * pulse_distance :.3f} m")
    clock = fl(params['clock'])*1e6

    time_per_frame = 1 /(n_matrices *  fps) - (n_x * n_y * n_bit_tdc * n_bit_hist) / (clock*n_pads)
    imps_per_frame = int(np.floor(time_per_frame/pulse_distance))

    params['pixel_power'] = power_per_pixel
    # print(f"Scanning (fix k) - Power per pixel {params['pixel_power']:.2f}")
    hit_count = optimal_laser_power(params)

    pre_outs = {

        'n_pix_per_shot': k_pix_per_shot,
        'power_per_pixel' : power_per_pixel,
        'n_matrices': n_matrices,
        'n_shots': n_shots,
        'tot_peak': k_pix_per_shot * power_per_pixel,
        'hit_count': hit_count,
        'n_imps': imps_per_frame
    }

    return pre_outs


def get_pre_output_scan_fix_p(params):
    """Scanning mode. We fix the power per pixel and the power budget,
    thus calculating the number of pixel that can be covered with one shot
    """

    n_sigma_recharge = int(params['n_sigma_recharge'])
    fov_x, fov_y = fl(params['fov_x']), fl(params['fov_y'])
    res_x, res_y = fl(params['res_x'])/100, fl(params['res_y'])/100
    range_max, laser_sigma = fl(params['range_max']), fl(params['laser_sigma'])*1e-9
    n_x, n_y = fl(params['h_matrix']), fl(params['v_matrix'])
    pb, clock = fl(params['power_budget']), fl(params['clock'])*1e6
    fps, n_pads = int(params['fps']), int(params['n_pads'])
    n_bit_tdc, n_bit_hist = int(params['n_bit_tdc_pre']), int(params['n_bit_hist_pre'])

    # calcolare quante volte il 64x64 ci sta nel 358x358
    n_x_tot = int(np.ceil((range_max * np.tan(np.deg2rad(0.5*fov_x)) / res_x)))
    n_y_tot = int(np.ceil((range_max * np.tan(np.deg2rad(0.5*fov_y)) / res_y)))

    n_matrices = int(np.ceil(n_x_tot/n_x) * np.ceil(n_y_tot/n_y))

    power_per_pixel =  float(params['pixel_power'])
    k_pix_per_shot = int(np.floor(n_sigma_recharge * pb / (np.sqrt(2*np.pi) * power_per_pixel)))
    n_shots = int(np.ceil(n_x * n_y / k_pix_per_shot))
    pulse_distance = max(2*float(params['range_max'])*1.05 / pm.C, n_shots*n_sigma_recharge*laser_sigma)

    # print(f"[FIX k]Pulse distance: {pulse_distance:.2E} s - {0.5 * pm.C * pulse_distance :.3f} m")

    clock = fl(params['clock'])*1e6

    time_per_frame = 1 /(n_matrices *  fps) - (n_x * n_y * n_bit_tdc * n_bit_hist) / (clock*n_pads)
    imps_per_frame = int(np.floor(time_per_frame/pulse_distance))
    # print(f"Flash (fix power per pixel) - Power per pixel {params['pixel_power']}")
    hit_count = optimal_laser_power(params)

    pre_outs = {

        'n_pix_per_shot': k_pix_per_shot,
        'power_per_pixel' : power_per_pixel,
        'n_matrices': n_matrices,
        'n_shots': n_shots,
        'tot_peak': k_pix_per_shot * power_per_pixel,
        'hit_count': hit_count,
        'n_imps': imps_per_frame
    }

    return pre_outs