import numpy as np
import matplotlib.pyplot as plt
from movespad import laser, pixel, params as pm
from tqdm import trange

def fl(x: str):
    return float(x)


def optimal_laser_power(params):
    """Simulate SPAD action to evaluate
    optimal laser power (6 hits out of 9)"""

    if params['seed']!='':
        np.random.seed(int(params['seed']))
    hit_counts = []

    time_step = 100e-12
    en = np.sqrt(2*pm.PI)*fl(params['laser_sigma'])*1e-9*fl(params['pixel_power'])
    n_imps = 1
    limit = 0.5e-6

    for _ in trange(250, leave=False):
        laser_spec = laser.full_laser_spectrum(
            init_offset= 1e-8,
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
            pulse_distance= limit,
            sigma_laser= fl(params['laser_sigma'])*1e-9,
            pulse_energy=en,
            array_len=None
        )

        start, stop = 0, limit * n_imps
        n_steps = int((stop-start)/time_step)
        times = np.linspace(start, stop, n_steps)

        n_laser, t_laser = laser.get_n_photons(times, laser_spec)
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

    n_pix_x = int(np.ceil(scene_x / (fl(params['res_x'])/100)))
    n_pix_y = int(np.ceil(scene_y / (fl(params['res_y'])/100)))

    n_pix_input = (int(params['h_matrix']), int(params['v_matrix']))


    n_bit_tdc, n_bit_hist = int(params['n_bit_tdc']), int(params['n_bit_hist'])
    n_pads = int(params['n_pads'])

    pre_out['n_pix_x'], pre_out['n_pix_y'] = n_pix_x, n_pix_y

    illum_mode, fps = params['illum_mode'], fl(params['fps'])
    n_sigma_recharge = 8
    imps_per_frame = 0
    laser_sigma = fl(params['laser_sigma'])*1e-9
    pulse_distance = max(2*fl(params['range_max'])*1.05 / pm.C, 8*laser_sigma*n_pix_y)
    pb = fl(params['power_budget'])
    n_pixel = n_pix_x * n_pix_y
    n_pixel_input  = n_pix_input[0] * n_pix_input[1]

    if illum_mode=='Flash':
        
        pulse_distance = max(2*float(params['range_max'])*1.05 / pm.C, n_sigma_recharge*laser_sigma)
        
        pulse_energy = pb / n_pixel * pulse_distance
        pulse_en_input = pb / n_pixel_input * pulse_distance

        power_per_pixel = pulse_energy / (np.sqrt(2*np.pi)*laser_sigma)
        power_per_pixel_input = pulse_en_input / (np.sqrt(2*np.pi)*laser_sigma)


    elif illum_mode=='Scanning':

        print("Scanning mode selected")
        power_per_pixel =  float(params['pixel_power'])
        pulse_energy = power_per_pixel * np.sqrt(2*np.pi) * laser_sigma
        n_pix_per_shot = int(np.floor(n_sigma_recharge * pb / (np.sqrt(2*np.pi) * power_per_pixel)))
    
        # print(f"Number of pixel hit in one shot: {n_pix_per_shot}")

        n_shots = int(np.ceil(n_pixel / n_pix_per_shot))

        pulse_distance = max(2*float(params['range_max'])*1.05 / pm.C, n_shots*n_sigma_recharge*laser_sigma)


    else:
        print("WARNING: You must select an illumination mode.")
        return

    time_per_frame = 1 / fps - (n_pix_x * n_pix_y * n_bit_tdc * n_bit_hist) / (fl(params['clock'])*1e6*n_pads)
    # print(f"1/fps : {1./fps}s - time per frame: {time_per_frame}s")
    imps_per_frame = int(np.floor(time_per_frame/pulse_distance))

    pre_out['imps_per_frame'] = imps_per_frame
    # Power per pixel in case of flash


    power_per_pixel = pb / n_pixel
    ppp_input = pb / n_pixel_input

    flash_power_per_pixel = power_per_pixel * pulse_distance / (np.sqrt(2*pm.PI)*laser_sigma)
    flash_power_per_pixel_input = ppp_input * pulse_distance / (np.sqrt(2*pm.PI)*laser_sigma)

    pre_out['flash_ppp'] = np.round(flash_power_per_pixel, 2)
    pre_out['flash_ppp_input'] = np.round(flash_power_per_pixel_input, 2)

    power_per_pixel =  float(params['pixel_power'])

    if power_per_pixel >pb:
        print(f"ATTENZIONE! Power per pixel maggiore del power budget totale.")
    pulse_energy = power_per_pixel * np.sqrt(2*np.pi) * laser_sigma
    n_pix_per_shot = int(np.floor(8 * pb / (np.sqrt(2*np.pi) * power_per_pixel)))
    
    pre_out['n_pix_per_shot'] = n_pix_per_shot

    # N bits for tdc

    t_max = 2*fl(params['range_max'])/pm.C
    t_min = 2*fl(params['range_min'])/pm.C

    histo_width = t_max - t_min
    bin_width = 0.01*fl(params['spatial_resolution']) / pm.C
    n_bins = np.ceil(histo_width/bin_width)
    n_bit = np.ceil(np.log2(n_bins))

    pre_out['n_bit_tdc'] = n_bit

    return pre_out


if __name__ == '__main__':
    pass