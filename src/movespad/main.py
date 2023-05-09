import numpy as np
import matplotlib.pyplot as plt
from time import time
import timeit
from movespad import laser, bkg, params as pm, pixel
from movespad import spad, solar


def execute_main(
    params: dict,
    mc : bool
):
    if mc:
        plt.clf()

    las_sigma = float(params['laser_sigma'])*10**(-9)
    pixel_size, pdp = int(params['pixel_size']), float(params['pdp'])
    pixel_area, ff = (float(params['spad_size'])*10**(-6)*pixel_size)**2, float(params['ff'])

    theta_h, theta_v = float(params['theta_h'])/1000, float(params['theta_v'])/1000

    f_lens, d_lens = float(params['f_lens'])/1000, float(params['d_lens'])/1000
    tau, bkg_klux = float(params['tau']), float(params['bkg_klux'])
    laser_l, after_p = float(params['wavelength'])*1e-9, float(params['after_pulsing'])

    t_dead, thr = float(params['t_dead'])*10**-9, int(params['coinc_thr'])

    n_imp, z = int(params['n_imp']), float(params['z'])
    rho_tgt, rng_min = float(params['rho_tgt']), float(params['range_min'])

    spad_j, tdc_j = float(params['spad_j'])*10**-12, float(params['tdc_j'])*10**-12
    n_bit_tdc, n_bit_hist  = int(params['n_bit_tdc']), int(params['n_bit_hist'])

    prob_lin, prob_diag = float(params['xtalk_r']), float(params['xtalk_d'])

    illum_mode, fwhm = params['illum_mode'], float(params['fwhm_bkg'])*1e-9

    pb, fps = float(params['power_budget']), float(params['fps'])
    multi_hit, range_max = int(params['multi_hit']), float(params['range_max'])

    n_sigma_recharge = 8
    laser_sigma, dcr = float(params['laser_sigma'])*1e-9, float(params['dcr'])
    n_pixel = float(params['h_matrix'])*float(params['v_matrix'])

    if illum_mode=='Flash':

        print("Flash mode selected")
        pulse_distance = max(2*range_max*1.05 / pm.C, n_sigma_recharge*laser_sigma)

        pulse_energy = pb / n_pixel * pulse_distance
        power_per_pixel = pulse_energy / (np.sqrt(2*np.pi)*laser_sigma)

        imps_per_frame = np.floor(pulse_distance * fps)
    
    elif illum_mode=='Scanning':

        print("Scanning mode selected")
        power_per_pixel =  float(params['pixel_power'])
        pulse_energy = power_per_pixel * np.sqrt(2*np.pi) * laser_sigma
        n_pix_per_shot = int(np.floor(n_sigma_recharge * pb / (np.sqrt(2*np.pi) * power_per_pixel)))
    
        print(f"Number of pixel hit in one shot: {n_pix_per_shot}")

        n_shots = int(np.ceil(n_pixel / n_pix_per_shot))

        pulse_distance = max(2*float(params['range_max'])*1.05 / pm.C, n_shots*n_sigma_recharge*laser_sigma)
        imps_pre_frame = np.floor(pulse_distance * fps)

    else:

        print("You must specify an illumination mode.")
        imps_per_frame = 0
        return


    pulse_distance = np.round(pulse_distance, 10)
    if not mc:
        print(f"Pulse distance: {pulse_distance:.4f} s - {0.5 * pm.C * pulse_distance :.3f} m")
    offset = 2*z / pm.C
    time_step = 100e-12
    start, stop = 0, pulse_distance * n_imp
    n_steps = int((stop-start)/time_step)
    # print(f"n steps: {(stop-start)/time_step} --> {n_steps}")
    times = np.linspace(start, stop, n_steps)
    array_len = len(times)
    if not mc:
        print(f"Len of times: {array_len}")
    bw = 1

    bkg_pow = solar.bkg_contrib(laser_l, fwhm, bkg_klux)

    if not mc:
        print("Creating bkg events...")
    bkg_spec = bkg.bkg_spectrum(times, tau, rho_tgt, ff,
                                pixel_area, z, f_lens, d_lens, bkg_pow)
    if not mc:
        print("Creating laser events...")
    las_spec = laser.full_laser_spectrum(offset, time_step, n_imp, tau, rho_tgt,
                        ff, pixel_area, f_lens, d_lens, theta_h, theta_v,
                        z, pulse_distance, las_sigma, pulse_energy, len(times))

    diff = len(las_spec) - len(times)
    times = np.append(times, np.zeros(shape=(diff,)))

    if not mc:
        print("Extracting number of laser photons...")
    n_ph_las, t_laser = laser.get_n_photons(times, las_spec, bw)
    if not mc:
        print("Extracting number of bkg photons...")
    n_ph_bkg, t_bkg = bkg.get_n_photons_bkg(times, bkg_spec, bw, dcr)

    pix = pixel.Pixel(size = pixel_size)

    pix.create_and_split(t_laser, t_bkg, pdp)
    if not mc:
        print("Generating crosstalk...")
    xtalk_prob = {
        'r': prob_lin,
        'ur': prob_diag
    }
    pix.crosstalk(xtalk_prob)
    if not mc:
        print("Applying t dead filter...")
    pix.t_dead_filter(t_dead, pdp, after_p)

    if not mc:
        print(f"Photon count: {[len(ts.timestamps) for ts in pix.timestamps]}")
    print(f"Laser count: {[len([elem for elem in ts.timestamps if elem.type=='las']) for ts in pix.timestamps]}")

    if not mc:
        print("Applying SPAD jitter...")
    pix.spad_jitter(spad_j)

    if not mc:
        print("Applying coincidence...")
    survived = pix.coincidence(thr=thr, window=3*las_sigma)

    survived = pixel.Pixel.tdc_jitter(tdc_j, survived).tolist()

    if not mc:
        print(f"{len(survived)} events found")
        print("Plotting results:\n**********\n\n")

    if len(survived)==0:
        plt.show()
        return {'none': None}

    tot_n = 2**(n_bit_tdc)
    count_limit = 2**(n_bit_hist)
    t_min = 2*rng_min / pm.C
    bins = np.linspace(t_min, pulse_distance, tot_n)
    hist_data = laser.get_hist_data([s.time for s in survived], pulse_distance, multi_hit)

    t_max = 2*range_max / pm.C
    hist_data = [h for h in hist_data if h<t_max]
    counts, bins = np.histogram(hist_data, bins=bins)

    counts = [min(count_limit, c) for c in counts]
    centroids, bfl = laser.get_centroids(bins, counts, hist_data, real_value=z)
    bfl = np.asarray(bfl) * max(counts)

    if not mc:
        pix.plot_events(times, las_spec, survived)
        fig, ax = plt.subplots()
        ax.stairs(counts, bins)
        secax = ax.secondary_xaxis(location='top', functions=(lambda x: 0.5*x*pm.C , lambda x :  2*x/pm.C))
        secax.set_label("Distance [m]")
    
        plt.title(f"TOF histogram {n_imp} pulses")
        plt.show()

    print(f"Max: {centroids['max']:.2f} - Mean: {centroids['mean']:.2f} - Top10%: {centroids['10perc']:.2f} - Gaus: {centroids['gaus']:.2f}")

    return centroids