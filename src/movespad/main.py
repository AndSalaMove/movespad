import numpy as np
import matplotlib.pyplot as plt
from movespad import laser, bkg, pixel, spad, params as pm


def main():

    offset = 2* pm.Z / pm.C
    time_step = 50e-12
    start, stop = 0, 4e-6
    n_steps = int((stop-start)/time_step)
    times = np.linspace(start, stop, n_steps)
    bw = 1 #points --> 50 ps

    print(offset)

    bkg_spec = bkg.bkg_spectrum(times)
    las_spec = laser.full_laser_spectrum(times, stop, init_offset=offset)

    n_ph_las, t_laser = laser.get_n_photons(times, las_spec, bw)
    n_ph_bkg, t_bkg = bkg.get_n_photons_bkg(times, bkg_spec, bw)

    print(f"Total laser photons: {sum(n_ph_las)}")
    print(f"Total bkg photons: {sum(n_ph_bkg)}")

    pix = pixel.Pixel()

    det = pix.process_events(t_laser, t_bkg, pm.T_DEAD, pm.T_THR, pm.T_QUENCH)
    det_times = [d.time for d in det]
    breakpoint()
    plt.scatter(t_laser, [0]*len(t_laser), color='red', s=5, label='laser')
    plt.scatter(t_bkg, [0]*len(t_bkg), color='navy', s=5, label='bkg')
    plt.scatter(det_times, [1]*len(det_times), color='green', s=5, label='detected')
    plt.ylim(-3,3)
    plt.legend()
    plt.show()


    pix.plot_events_and_spectra(times, det, las_spec, bkg_spec)


if __name__ == '__main__':
    main()