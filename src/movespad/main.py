import numpy as np
import matplotlib.pyplot as plt
from time import time
import timeit
from movespad import laser, bkg, spad, params as pm, pixel
from movespad import spad


def main():


    offset = 2* pm.Z / pm.C
    time_step = 50e-12
    start, stop = 0, 4e-6
    n_steps = int((stop-start)/time_step)
    times = np.linspace(start, stop, n_steps)
    bw = 1 #points --> 50 ps

    bkg_spec = bkg.bkg_spectrum(times)
    las_spec = laser.full_laser_spectrum(times, stop, init_offset=offset)

    n_ph_las, t_laser = laser.get_n_photons(times, las_spec, bw)
    n_ph_bkg, t_bkg = bkg.get_n_photons_bkg(times, bkg_spec, bw)

    # print(f"Total laser photons: {sum(n_ph_las)}")
    # print(f"Total bkg photons: {sum(n_ph_bkg)}")

    pix = pixel.Pixel(size = 2)
    pix.create_and_split(t_laser, t_bkg, pm.PDP)
    pix.crosstalk(pm.XTALK_PROBS)
    pix.process_events(pm.T_DEAD, pm.PDP, pm.AP_PROB)

    print(f"Photon count: {[len(ts.timestamps) for ts in pix.timestamps]}")
    print(f"Laser count: {[len([elem for elem in ts.timestamps if elem.type=='las']) for ts in pix.timestamps]}")
    pix.plot_events(times, las_spec)


if __name__ == '__main__':
    main()