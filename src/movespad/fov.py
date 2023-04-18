"""Module to calculate scanning strategy, fov, ..."""

import numpy as np
import movespad.params as pm


def optimizer():

    #INPUT PARAMS

    #FOV_x /2 = arctan(L_x / 2f)
    # L_x / 2f = tg(FOV_x /2)

    FOV = (400, 200)
    RES = (0.1, 0.1) #al range piu lungo
    RANGE = (10, 200)
    n_pix = (128, 128)
    n_pix_total = n_pix[0] * n_pix[1]
    t_pulse = 2*RANGE[1]/pm.C
    laser_power_on_pixel = 45

    fps = 10

    n_pix_tot = (FOV[0] / RES[0], FOV[1] / RES[1])
    n_matrices = [np.ceil(a/b) for a,b in zip(n_pix_tot, n_pix)]

    n_mat_tot = n_matrices[0] * n_matrices[1]
    print(f"Number of matrices needed to cover the fov: {n_matrices}")

    t_frame = 1./fps   
    t_per_matrix = t_frame / n_mat_tot

    n_pulses_perframemat = np.floor(t_per_matrix / t_pulse)

    print(f"T pulse: {t_pulse}") #arrotondare in su
    print(f"n pulses per frame per fov portion: {n_pulses_perframemat}") #arrotondare alla decina giu

    # it means that for each pixel, I have n_pulses_perframemat that I can distribute on a
    # smaller pixel portion the laser pulse

    #fare i vari tentativi su come distribuire il laser
    status = {}
    single_pulse_time = 15e-9 #leggermente sovrastimato

    #singolo
    n_shots = n_pix_total
    total_time = n_shots * single_pulse_time
    power_per_pixel = 45
    status['single'] = 'success' if total_time < t_pulse else 'failed'

    # riga
    n_shots = n_pix[0]
    total_time = n_shots * single_pulse_time
    status['row'] = {'status': 'success' if total_time < t_pulse else 'failed',
                      'time_taken': total_time,
                      'power': power_per_pixel * n_pix_total / n_shots}

    # colonna
    n_shots = n_pix[1]
    total_time = n_shots * single_pulse_time
    status['col'] = {'status': 'success' if total_time < t_pulse else 'failed',
                      'time_taken': total_time,
                      'power': power_per_pixel * n_pix_total / n_shots}

    # 4 quadrati
    n_shots = 4
    total_time = n_shots * single_pulse_time
    status['4sq'] = {'status': 'success' if total_time < t_pulse else 'failed',
                      'time_taken': total_time,
                      'power': power_per_pixel * n_pix_total / n_shots}
    # 16 quadrati
    n_shots = 16
    total_time = n_shots * single_pulse_time
    status['16sq'] = {'status': 'success' if total_time < t_pulse else 'failed',
                      'time_taken': total_time,
                      'power': power_per_pixel * n_pix_total / n_shots}

    # 64 quadrati
    n_shots = 64
    total_time = n_shots * single_pulse_time
    status['64sq'] = {'status': 'success' if total_time < t_pulse else 'failed',
                      'time_taken': total_time,
                      'power': power_per_pixel * n_pix_total / n_shots}
    


    from pprint import pprint
    pprint(status)
    #options: 
    #- full laser on the matrix: Ptx decreased by a factor n_pix_tot
    # scanning: less laser pulses per scan, but more laser power


if __name__ == '__main__':
    optimizer()