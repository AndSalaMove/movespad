import PySimpleGUI as sg
import os, pathlib
from movespad import main, pre_output


def gui():

    sg.set_options(font=("Helvetica", 12))

    sg.theme("DarkBlue15")
    layout = [

        [sg.T("MOVE-X LIDAR SIMULATION", justification='center', size=(80,1), font=("Helvetica", 14, "bold"))],

        [sg.T("Laser specifications", justification='center', size=(40,1), font=("Helvetica", 12, "bold")),
         sg.T("Pixel specifications", justification='center', size=(40,1), font=("Helvetica", 12, "bold"))],

        [sg.T("Power per Pixel (W)", size=(28,1), justification='right'), sg.I(key='pixel_power', default_text='2', size=(10,1)),
         sg.T("SPADs per side", size=(28, 1), justification='right'), sg.I(key='pixel_size', default_text='3', size=(10,1))],
        [sg.T("Power Budget (W)", size=(28,1), justification='right'), sg.I(key='power_budget', default_text='18', size=(10,1)), 
         sg.T("Physical Matrix (LxH)", size=(28,1), justification='right'), sg.I(key='h_matrix', default_text='64', size=(5,1)), sg.T("x"), sg.I(key='v_matrix', default_text='64', size=(4,1))],
        [sg.T("Sigma (ns)", size=(28,1), justification='right'),     sg.I(key='laser_sigma', default_text='1.9108', size=(10, 1)),
         sg.T("Fill factor", size=(28,1), justification='right'), sg.I(key='ff', default_text='0.98', size=(10,1))],
        [sg.T("Pulse distance (us)", size=(28,1), justification='right'), sg.I(key='pulse_distance', default_text='1.5', size=(10,1)),
         sg.T("SPAD size (um)", size=(28,1), justification='right'), sg.I(key='spad_size', default_text="10.17", size=(10,1))],
        [sg.T("Beam divergence (mrad)", size=(28,1), justification="right"), sg.I(key='theta_h', size=(4,1), default_text="1.5"),
         sg.T("x") ,sg.I(key='theta_v', size=(4,1), default_text="1.5"), sg.T("PDP", justification='right', size=(26,1)),
         sg.I(key='pdp', default_text="0.2", size=(10,1))],
        [sg.T("Illumination mode", size=(28,1), justification='right'), sg.Combo(['Flash', 'Scanning'], key='illum_mode', size=(8,1)), 
         sg.T("T dead (ns)", size=(28,1), justification='right'), sg.I(key="t_dead", default_text="7", size=(10,1)) ],
        [sg.T("", size=(39,1)), sg.T("Coincidence number", size=(28,1), justification='right'), sg.I(key="coinc_thr", default_text="6", size=(10,1))],
        [sg.T("", size=(39,1)), sg.T("Spad sigma (ps)", size=(28,1), justification='right'), sg.I(key="spad_j", default_text="72", size=(10,1))],
        [sg.T("FOV (deg)", size=(28,1), justification='right'), sg.I(key='fov_x', default_text='30', size=(4,1)), sg.I(key='fov_y', default_text='30', size=(4,1)),
            sg.T("After pulsing probability", size=(28,1), justification='right'), sg.I(key="after_pulsing", default_text="0.014", size=(10,1))],
        [sg.T("Resolution (cm)", size=(28,1), justification='right'), sg.I(key='res_x', default_text='15', size=(4,1)), sg.I(key='res_y', default_text='15', size=(4,1)),
         sg.T("Crosstalk Probability (L,D)", size=(28,1), justification='right'), sg.I(key='xtalk_r', default_text='0.034', size=(5,1)), sg.I(key='xtalk_d', default_text='0.017', size=(4,1))],
        [sg.T("", size=(39,1)), sg.T("Dark Count Rate (cps)", size=(28,1), justification='right'), sg.I(key="dcr", default_text="6800", size=(10,1))],
        [sg.T("")],

        [sg.T("Optics", justification='center', size=(40,1), font=("Helvetica", 12, "bold")),
         sg.T("Physical parameters", justification='center', size=(40,1), font=("Helvetica", 12, "bold"))],

        [sg.T("Focal length (mm)", size=(28,1), justification='right'),  sg.I(key='f_lens', default_text='20', size=(10,1)),
         sg.T("Range (m)", size=(28,1), justification='right'), sg.I(key="range_min", default_text="10", size=(4,1)), sg.I(key="range_max", default_text="200", size=(5,1))],
        [sg.T("Lens diameter (mm)", size=(28,1), justification='right'), sg.I(key='d_lens', default_text='16', size=(10,1)), 
         sg.T("Target Distance (m)", size=(28,1), justification='right'), sg.I(key="z", default_text="180", size=(10,1))],
        [sg.T("Transmittance", size=(28,1), justification='right'),      sg.I(key='tau', default_text='0.90', size=(10,1)), 
         sg.T("Number of pulses", size=(28,1), justification='right'), sg.I(key='n_imp', default_text='30', size=(10,1))],
        [sg.T("Optical Filter Band (nm)", size=(28,1), justification='right'),  sg.I(key='filter_band', default_text='10', size=(10,1)), 
         sg.T("Target reflectivity", size=(28,1), justification='right'), sg.I(key='rho_tgt', default_text='0.2', size=(10,1))],
        [sg.T("Optical Filter Efficiency", size=(28,1), justification='right'),  sg.I(key='filter_efficiency', default_text='0.95', size=(10,1)), 
         sg.T("Bkg irradiance (W/m2/nm)", size=(28,1), justification='right'), sg.I(key="bkg_power", default_text="0.2", size=(10,1))],
        [sg.T("")],

        [sg.T("TDC", justification='center', size=(40,1), font=("Helvetica", 12, "bold"))],

        [sg.T("Measurement Resolution (cm)", size=(28,1), justification='right'), sg.I(key="spatial_resolution", default_text="10", size=(10,1))],
        [sg.T("TDC sigma (ps)", size=(28,1), justification='right'), sg.I(key='tdc_j', default_text='100', size=(10,1)),
            sg.T("", size=(15)), sg.Button('Pre-Output'), sg.Submit(auto_size_button=True), sg.Cancel(auto_size_button=True)],
        [sg.T("N bit (TDCxHIST)", size=(28,1), justification='right'), sg.I(key='n_bit_tdc', default_text='12', size=(5,1)), sg.I(key='n_bit_hist', default_text='5', size=(4,1))],

        # [sg.Text("", size=(40)), sg.Submit(auto_size_button=True), sg.Cancel(auto_size_button=True)]

    ]

    window = sg.Window("LIDAR starter", layout=layout, resizable=True)

    while True:
        event, values = window.read()

        if event is None or event=='Cancel':
            break
        elif event=='Pre-Output':
            outs = pre_output.get_pre_output(params=values)

            layout2 = [

            [sg.T("Pre-Output Values", justification='center', size=(48,1), font=("Helvetica", 12, "bold"))],

            [sg.T("Average hit count", size=(32,1), justification='right'), sg.InputText(outs['hit_counts'], size=(16,1), use_readonly_for_disable=True)],
            [sg.T("[FLASH] Power per pixel (W)", size=(32,1), justification='right'), sg.InputText(outs['flash_ppp'], size=(16,1), use_readonly_for_disable=True)],
            [sg.T("Physical Matrix", size=(32,1), justification='right'), sg.InputText(outs['n_pix_x'], size=(7,1), use_readonly_for_disable=True),sg.InputText(outs['n_pix_y'], size=(7,1), use_readonly_for_disable=True)],
            [sg.T("Nbit_TDC", size=(32,1), justification='right'), sg.InputText(outs['n_bit_tdc'], size=(16,1), use_readonly_for_disable=True)]

            ]   
            window2 = sg.Window('Second Window', location=(400,200)).Layout(layout2)

            event, values = window2.Read()
            window2.Close()

        elif event=='Submit':
            print(f"Executing with new params..." )
            window.close()
            #main.exec ute_main(params=values)
    window.close()

def gui5():
    import matplotlib.pyplot as plt
    import numpy as np
    layout = [
                [sg.Text('Your typed chars appear here:'), sg.Text('', key='_OUTPUT_')],
                [sg.Input(do_not_clear=True, key='_IN_', default_text='abcd')],
                [sg.Button('Show'), sg.Button('Run'), sg.Button('Exit')]
            ]

    window = sg.Window('Window Title').Layout(layout)

    while True:             # Event Loop
        event, values = window.Read()
        print(event, values)
        if event is None or event == 'Exit':
            break
        if event == 'Run':
            print("RUNNING with value", values['_IN_'])
            plt.plot(np.random.normal(size=(100)))
            plt.show()
            window.close()
        if event == 'Show':
            layout2 = [
                [sg.Text('The second window'), sg.Text('', key='_OUTPUT_')],
                [sg.InputText('You can select this text', use_readonly_for_disable=True, disabled=True, key='-IN-')],
                [sg.Button('Show'), sg.Button('Exit')]
                    ]
            window2 = sg.Window('Second Window', location=(400,400)).Layout(layout2)

            event, values = window2.Read()
            window2.Close()
        if event=='Update':
            window.Element('_IN_').Update("New value")

    window.Close()


if __name__ == "__main__":
    gui5()
