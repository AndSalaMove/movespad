import numpy as np
from movespad import laser, bkg, pixel, spad, params as pm


def main():

    time_step = 50e-12
    start, stop = 0, 10e-6
    n_steps = int((stop-start)/time_step)
    times = np.linspace(start, stop, n_steps)
    bw = 1 #points --> 50 ps

    offset = 2* pm.Z / pm.C
    print(offset)

    bkg_spec = bkg.bkg_spectrum(times)
    las_spec = laser.full_laser_spectrum(times, stop, init_offset=offset)

    n_ph_las, t_laser = laser.get_n_photons(times, las_spec, bw)
    n_ph_bkg, t_bkg = bkg.get_n_photons_bkg(times, bkg_spec, bw)

    print(f"Total laser photons: {sum(n_ph_las)}")
    print(f"Total bkg photons: {sum(n_ph_bkg)}")

    pix = pixel.Pixel()

    det = pix.process_events(t_laser, t_bkg, pm.T_DEAD, pm.T_THR, pm.T_QUENCH)
    breakpoint()

    pix.plot_events_and_spectra(times, det, las_spec, bkg_spec)


if __name__ == '__main__':
    main()