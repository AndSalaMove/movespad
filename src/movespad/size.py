import movespad.params as pm
import numpy as np


def get_matrix_size(
        pixel_size,
        n_coinc,
        range_max,
        fps,
        fov_x,fov_y,
        res_x, res_y,
        n_rows,
        f_number,
        spad_size,
        sigma_laser
):
    scene_x = range_max * np.tan(fov_x / 2)
    scene_y = range_max * np.tan(fov_y / 2)

    n_pix_x = np.ceil(scene_x / res_x)
    n_pix_y = np.ceil(scene_y / res_y)

    print(f"Dimensione matrice: {(n_pix_x, n_pix_y)}")

    mag = scene_x / (n_pix_x * spad_size * pixel_size)

    focal = range_max / mag
    diam = focal / f_number

    print(f"Focale: {focal} - Diameter: {diam}")

    rep_period = max(2*range_max*1.05 / pm.C, 8*sigma_laser*n_pix_y)
    #n_imp_per_frame = 1 / (fps * rep_period)
    t_gen_frame = n_pix_x * n_pix_y * 16 * 14 / (4*(100e6))
    print("T gen frame", t_gen_frame)
    frame_length = 1 / fps - t_gen_frame
    n_imp_per_frame = np.floor(frame_length / rep_period)

    print(f"Numero di impulsi in un periodo di {rep_period}: {n_imp_per_frame}")




if __name__ == '__main__':
    get_matrix_size(
        pixel_size= 3,
        n_coinc= 6,
        range_max= 200,
        fps = 10,
        fov_x= np.deg2rad(20),  
        fov_y = np.deg2rad(20),
        res_x=0.30,
        res_y=0.30,
        n_rows=1,
        f_number=1.2,
        spad_size=10.17e-6,
        sigma_laser=1.91e-9
    )
