import numpy as np
import matplotlib.pyplot as plt
from time import time
import timeit
from movespad import laser, bkg, spad, params as pm, pixel
from movespad import spad


def main():

    offset = 2* pm.Z / pm.C
    time_step = 100e-12
    start, stop = 0, 1.35e-6 * pm.N_IMP
    n_steps = int((stop-start)/time_step)
    times = np.linspace(start, stop, n_steps)
    bw = 1 #points --> 50 ps

    print("Creating bkg events...")
    bkg_spec = bkg.bkg_spectrum(times)
    print("Creating laser events...")
    las_spec, n_pulses = laser.full_laser_spectrum(times, stop, init_offset=offset)
    v_lines = [i*pm.PULSE_DISTANCE for i in range(n_pulses)]

    print("Extracting number of photons...")
    n_ph_las, t_laser = laser.get_n_photons(times, las_spec, bw)
    n_ph_bkg, t_bkg = bkg.get_n_photons_bkg(times, bkg_spec, bw)

    # print(f"Total laser photons: {sum(n_ph_las)}")
    # print(f"Total bkg photons: {sum(n_ph_bkg)}")

    pix = pixel.Pixel(size = pm.PIXEL_SIZE)

    pix.create_and_split(t_laser, t_bkg, pm.PDP)
    print("Generating crosstalk...")
    pix.crosstalk(pm.XTALK_PROBS)
    print("Applying t dead filter...")
    pix.t_dead_filter(pm.T_DEAD, pm.PDP, pm.AP_PROB)

    print(f"Photon count: {[len(ts.timestamps) for ts in pix.timestamps]}")
    print(f"Laser count: {[len([elem for elem in ts.timestamps if elem.type=='las']) for ts in pix.timestamps]}")

    print("Applying coincidence...")
    survived = pix.coincidence(thr=pm.COINCIDENCE_THR, window=3*pm.SIGMA_LASER)
    print("Plotting results:")
    pix.plot_events(times, las_spec, survived, v_lines)

    # hist_data = laser.get_hist_data(survived)

    hist_data = laser.get_hist_data([s.time for s in survived], pm.PULSE_DISTANCE)
    print(survived)
    print(hist_data)

    plt.hist(hist_data, bins=[i*1e-9 for i in range(0,1350)])
    plt.title("TOF histogram")
    plt.show()

if __name__ == '__main__':
    main()