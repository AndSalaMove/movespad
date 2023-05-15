import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
from movespad import main, pre_output

plt.style.use('Solarize_Light2')


def gui():

    sg.set_options(font=("Helvetica", 12))
    sg.theme("DarkBlue15")

    left = [

        [sg.T("Laser specifications", justification='center', size=(40,1), font=("Helvetica", 12, "bold"))],
        [sg.T("Power per Pixel (W)", size=(28,1), justification='right', tooltip='Useful only for Scanning mode'), sg.I(key='pixel_power', default_text='2', size=(10,1))],
        [sg.T("Power Budget (W)", size=(28,1), justification='right'), sg.I(key='power_budget', default_text='18', size=(10,1))],
        [sg.T("Sigma (ns)", size=(28,1), justification='right'),     sg.I(key='laser_sigma', default_text='1.9108', size=(10, 1))],
        [sg.T("Wavelength (nm)", size=(28,1), justification='right'), sg.I(key='wavelength', default_text='905', size=(10,1))],
        [sg.T("Beam divergence (mrad)", size=(28,1), justification="right"), sg.I(key='theta_h', size=(3,1), default_text="1.5"), sg.T("x") ,sg.I(key='theta_v', size=(3,1), default_text="1.5")],
        [sg.T("Frames per second", size=(28,1), justification='right'), sg.I(key="fps", default_text='10', size=(10,1))],
        [sg.T("FOV (deg)", size=(28,1), justification='right'), sg.I(key='fov_x', default_text='30', size=(4,1)), sg.I(key='fov_y', default_text='30', size=(4,1))],
        [sg.T("Resolution (cm)", size=(28,1), justification='right'), sg.I(key='res_x', default_text='15', size=(4,1)), sg.I(key='res_y', default_text='15', size=(4,1))],
        [sg.T("Illumination mode", size=(28,1), justification='right'), sg.Combo(['Flash', 'Scanning'], key='illum_mode', size=(10,1), default_value='Flash')],

        [sg.T("")],
        [sg.T("")],
        [sg.T("")],

        [sg.T("Optics", justification='center', size=(40,1), font=("Helvetica", 12, "bold"))],

        [sg.T("Focal length (mm)", size=(28,1), justification='right'),  sg.I(key='f_lens', default_text='20', size=(10,1))],
        [sg.T("Lens diameter (mm)", size=(28,1), justification='right'), sg.I(key='d_lens', default_text='16', size=(10,1))],
        [sg.T("Transmittance", size=(28,1), justification='right'),      sg.I(key='tau', default_text='0.90', size=(10,1))],
        [sg.T("Optical Filter FWHM (nm)", size=(28,1), justification='right'),  sg.I(key='fwhm_bkg', default_text='10', size=(10,1))],

        [sg.T("")],
        [sg.T("")],

    ]

    center = [
        [sg.T("Pixel specifications", justification='center', size=(40,1), font=("Helvetica", 12, "bold"))],
        [sg.T("SPADs per side", size=(28, 1), justification='right'), sg.I(key='pixel_size', default_text='3', size=(10,1))],
        [sg.T("Physical Matrix (LxH)", size=(28,1), justification='right'), sg.I(key='h_matrix', default_text='64', size=(3,1)), sg.T("x"), sg.I(key='v_matrix', default_text='64', size=(3,1))],
        [sg.T("Fill factor", size=(28,1), justification='right'), sg.I(key='ff', default_text='0.98', size=(10,1))],
        [sg.T("SPAD size (um)", size=(28,1), justification='right'), sg.I(key='spad_size', default_text="10.17", size=(10,1))],
        [sg.T("PDP", justification='right', size=(28,1)), sg.I(key='pdp', default_text="0.2", size=(10,1))],
        [sg.T("T dead (ns)", size=(28,1), justification='right'), sg.I(key="t_dead", default_text="7", size=(10,1))],
        [sg.T("Coincidence number", size=(28,1), justification='right'), sg.I(key="coinc_thr", default_text="6", size=(10,1))],
        [sg.T("Spad sigma (ps)", size=(28,1), justification='right'), sg.I(key="spad_j", default_text="72", size=(10,1))],
        [sg.T("After pulsing probability", size=(28,1), justification='right'), sg.I(key="after_pulsing", default_text="0.014", size=(10,1))],
        [sg.T("Crosstalk Probability (L,D)", size=(28,1), justification='right'), sg.I(key='xtalk_r', default_text='0.03', size=(4,1)), sg.I(key='xtalk_d', default_text='0.01', size=(4,1))],
        [sg.T("Dark Count Rate (cps)", size=(28,1), justification='right'), sg.I(key="dcr", default_text="60800", size=(10,1))],
        [sg.T("")],

        [sg.T("Physical parameters", justification='center', size=(40,1), font=("Helvetica", 12, "bold"))],

        [sg.T("Range (m)", size=(28,1), justification='right'), sg.I(key="range_min", default_text="10", size=(4,1)), sg.I(key="range_max", default_text="200", size=(4,1))],
        [sg.T("Target Distance (m)", size=(28,1), justification='right'), sg.I(key="z", default_text="180", size=(10,1))],
        [sg.T("Number of pulses", size=(28,1), justification='right'), sg.I(key='n_imp', default_text='30', size=(10,1))],
        [sg.T("Target reflectivity", size=(28,1), justification='right'), sg.I(key='rho_tgt', default_text='0.2', size=(10,1))],
        [sg.T("Background klux", size=(28,1), justification='right'), sg.I(key="bkg_klux", default_text="120", size=(10,1))],
        [sg.T("")],
    ]

    right = [
        [sg.T("TDC", justification='center', size=(40,1), font=("Helvetica", 12, "bold"))],
        [sg.T("Measurement Resolution (cm)", size=(28,1), justification='right'), sg.I(key="spatial_resolution", default_text="10", size=(10,1))],
        [sg.T("TDC sigma (ps)", size=(28,1), justification='right'), sg.I(key='tdc_j', default_text='100', size=(10,1))],
        [sg.T("N bit (TDCxHIST)", size=(28,1), justification='right'), sg.I(key='n_bit_tdc', default_text='12', size=(3,1)), sg.T("x"), sg.I(key='n_bit_hist', default_text='5', size=(3,1))],
        [sg.T("Effective N bit", size=(28,1), justification='right'), sg.I(key='n_bit_tdc_pre', default_text='6', size=(3,1)), sg.T("x"), sg.I(key='n_bit_hist_pre', default_text='3', size=(3,1))],
        [sg.T("Clock frequency (MHz)", size=(28,1), justification='right'), sg.I(key='clock', default_text='100', size=(10,1))],
        [sg.T("Number of pads", size=(28,1), justification='right'), sg.I(key='n_pads', default_text='1', size=(10,1))],
        [sg.T("Multi hit", size=(28,1), justification='right'), sg.I(key="multi_hit", default_text="1", size=(10,1))],
        [sg.T("")],
        [sg.T("")],
        [sg.T("")],
        [sg.T("Random seed", size=(28,1), justification='right'),      sg.I(key='seed',    default_text='', size=(10,1))],
        [sg.T("Monte Carlo Runs", size=(28,1), justification='right'), sg.I(key='mc-runs', default_text="0", size=(10,1))],
        [sg.T("")],

        [sg.T("", size=(20,1)), sg.Button('Pre-Output', size=(10,1), button_color=())],
        [sg.T("", size=(20,1)), sg.Submit(size=(10,1))],
        [sg.T("", size=(20,1)), sg.Button('Monte Carlo', size=(10,1), button_color=('gold2', 'black'))],
        [sg.T("", size=(20,1)), sg.Cancel(size=(10,1), button_color=('gainsboro', 'indianred'))],

        [sg.T("")],
    ]
 
    layout = [
 
        [sg.T("MOVE-X LIDAR SIMULATION v1.1.0", justification='center', size=(120,1), font=("Helvetica", 14, "bold"))],
        [sg.T("")],
        [sg.Column(left, pad=(0, 0)), sg.Column(center, pad=(0, 0)), sg.Column(right, pad=(0, 0))],


    ]

    window = sg.Window("LIDAR starter", layout=layout, resizable=True)

    while True:
        event, values = window.read()

        if event is None or event=='Cancel':
            print("Goodbye!")
            break
        elif event=='Pre-Output':
            outs = pre_output.get_pre_output(params=values)

            hitcount_tip = """
            Average number of SPADs hit for a single laser pulse.
            Compare this number with the coincidence threshold and,
            if necessary, change the Power per Pixel parameter.
            """

            matrix_tt = """Matrix dimension given FOV, resolution and maximum range to perform a flash"""
            ppp = """
            Power per pixel assuming flash mode. Obtained by the
            total power budget and number of pixel in input"""

            npix_tt = """
            Number of pixel that can be reached by the laser (assuming Scanning mode)
            with each shot. This count is obtained from the power budget and the power per pixel"""

            nbit = """Number of bits needed by the TDC."""

            layout_2 = [

            [sg.T("Pre-Output Values", justification='center', size=(48,1), font=("Helvetica", 12, "bold"))],
            [sg.T("Average hit count", size=(32,1), justification='right', tooltip=hitcount_tip), sg.InputText(outs['hit_counts'], size=(16,1), use_readonly_for_disable=True)],
            [sg.T("[FLASH] Power per pixel (W)", size=(32,1), justification='right', tooltip=ppp), sg.InputText(outs['flash_ppp'], size=(16,1), use_readonly_for_disable=True)],
            [sg.T("[FLASH] Power per pixel (input matrix, W)", size=(32,1), justification='right', tooltip=ppp), sg.InputText(outs['flash_ppp_input'], size=(16,1), use_readonly_for_disable=True)],
            [sg.T("[SCANNING] N pixel per shot", size=(32,1), justification='right', tooltip=npix_tt), sg.InputText(outs['n_pix_per_shot'], size=(16,1), use_readonly_for_disable=True)],
            [sg.T("Number of pulses per frame", size=(32,1), justification='right'), sg.InputText(outs['imps_per_frame'], size=(16,1), use_readonly_for_disable=True)],
            [sg.T("Flash Matrix", size=(32,1), justification='right', tooltip=matrix_tt), sg.InputText(outs['n_pix_x'], size=(7,1), use_readonly_for_disable=True),sg.InputText(outs['n_pix_y'], size=(7,1), use_readonly_for_disable=True)],
            [sg.T("Nbit_TDC", size=(32,1), justification='right'), sg.InputText(outs['n_bit_tdc'], size=(16,1), use_readonly_for_disable=True)]

            ]
            window2 = sg.Window('Second Window', location=(400,200)).Layout(layout_2)

            event, values = window2.Read()
            window2.Close()

        elif event=='Submit':
            centroids = main.execute_main(params=values, mc=False)
            if 'none' in centroids.keys():
                pass

            else:
                layout_3 = [
                    [sg.T("Highest bin", size=(20,1), justification='right'),         sg.InputText(f"{centroids['max']:.2f} m", size=(16,1), use_readonly_for_disable=True), sg.InputText(f"{centroids['max']+centroids['z']:.2f} m", size=(16,1), use_readonly_for_disable=True)],
                    [sg.T("Histogram average", size=(20,1), justification='right'),   sg.InputText(f"{centroids['mean']:.2f} m", size=(16,1), use_readonly_for_disable=True), sg.InputText(f"{centroids['mean']+centroids['z']:.2f} m", size=(16,1), use_readonly_for_disable=True)],
                    [sg.T("Top 10% average", size=(20,1), justification='right'),     sg.InputText(f"{centroids['10perc']:.2f} m", size=(16,1), use_readonly_for_disable=True), sg.InputText(f"{centroids['10perc']+centroids['z']:.2f} m", size=(16,1), use_readonly_for_disable=True)],
                    [sg.T("Gaussian fit", size=(20,1), justification='right'),        sg.InputText(f"{centroids['gaus']:.2f} m", size=(16,1), use_readonly_for_disable=True), sg.InputText(f"{centroids['gaus']+centroids['z']:.2f} m", size=(16,1), use_readonly_for_disable=True)],
                    [sg.Exit(auto_size_button=True)]
                ]

                window3 = sg.Window(title='Simulation results', layout=layout_3, resizable=True, grab_anywhere=True)
                ev_3, val_3 = window3.read()

                if ev_3=='Exit' or ev_3 is None:
                    window3.close()


        elif event=='Monte Carlo':
            print(f"* Monte Carlo @{values['mc-runs']} *")

            n_runs = int(values['mc-runs'])
            results = {
                'max': [],
                'mean': [],
                '10perc': [],
                'gaus': []
            }


            for run in range(n_runs):
                print(f"*********** RUN {1+run}/{n_runs} ****************")
                centroids = main.execute_main(params=values, mc=True)
                for key in centroids.keys():
                    if key=='z':
                        pass
                    else:

                        results[key].append(centroids[key])

            errors = {key: np.mean(results[key]) for key in results.keys()}
            plt.subplot(2,2,1)
            plt.title(f"Highest bin ({errors['max']:.3f})", fontsize=10)
            plt.hist(results['max'], density=True, bins=30)
            plt.axvline(x = 0, ymin=0, ymax=1,
                        linestyle='dashed', color='crimson')

            plt.subplot(2,2,2)
            plt.title(f"Histogram average ({errors['mean']:.3f})",  fontsize=10)
            plt.hist(results['mean'], density=True, bins=30)
            plt.axvline(x = 0, ymin=0, ymax=1,
                        linestyle='dashed', color='crimson')

            plt.subplot(2,2,3)
            plt.title(f"Top 10% average ({errors['10perc']:.3f})",  fontsize=10)
            plt.hist(results['10perc'], density=True, bins=30)
            plt.axvline(x = 0, ymin=0, ymax=1,
                        linestyle='dashed', color='crimson')

            plt.subplot(2,2,4)
            plt.title(f"Gaussian fit mean ({errors['gaus']:.3f})",  fontsize=10)
            plt.hist(results['gaus'], density=True, bins=30)
            plt.axvline(x = 0, ymin=0, ymax=1,
                        linestyle='dashed', color='crimson')

            plt.show()

    window.close()