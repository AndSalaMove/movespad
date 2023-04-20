import PySimpleGUI as sg
import os, pathlib
from movespad import main


def gui():

    sg.set_options(font=("Helvetica", 12))

    sg.theme("DarkBlue15")
    layout = [
        #[sg.Image(img_path, size=(1000, 500))],
        [sg.T("MOVE-X LIDAR SIMULATION", justification='center', size=(60,2), font=("Helvetica", 14, "bold"))],

        [sg.T("Laser specifications", justification='center', size=(30,1), font=("Helvetica", 12, "bold")),
         sg.T("Pixel specifications", justification='center', size=(30,1), font=("Helvetica", 12, "bold"))],

        [sg.T("Peak Power (W)", size=(20,1), justification='right'), sg.I(key='laser_power', default_text='5', size=(10,1)),
         sg.T("SPADs per side", size=(20, 1), justification='right'), sg.I(key='pixel_size', default_text='3', size=(10,1))],
        [sg.T("Sigma (ns)", size=(20,1), justification='right'),     sg.I(key='laser_sigma', default_text='1.9108', size=(10, 1)),
         sg.T("Fill factor", size=(20,1), justification='right'), sg.I(key='fill_factor', default_text='0.99', size=(10,1))],
        [sg.T("Pulse distance (us)", size=(20,1), justification='right'), sg.I(key='pulse_distance', default_text='1.5', size=(10,1)),
         sg.T("SPAD size (um)", size=(20,1), justification='right'), sg.I(key='spad_size', default_text="10.17", size=(10,1))],
        [sg.T("Beam divergence (mrad)", size=(20,1), justification="right"), sg.I(key='theta_h', size=(4,1), default_text="1.5"),
         sg.T("x") ,sg.I(key='theta_v', size=(4,1), default_text="1.5"), sg.T("PDP", justification='right', size=(18,1)),
         sg.I(key='pdp', default_text="0.2", size=(10,1))],
        [sg.T("")],

        [sg.T("Optics", justification='center', size=(30,1), font=("Helvetica", 12, "bold")),
         sg.T("Other" , justification='center', size=(30,1), font=("Helvetica", 12, "bold"))],

        [sg.T("Focal length (mm)", size=(20,1), justification='right'),  sg.I(key='f_lens', default_text='20', size=(10,1)),
        sg.T("Bkg irradiance (W/m2)", size=(20,1), justification='right'), sg.I(key="bkg_power", default_text="0.2", size=(10,1))],
        [sg.T("Lens diameter (mm)", size=(20,1), justification='right'), sg.I(key='d_lens', default_text='16', size=(10,1)),
        sg.T("T dead (ns)", size=(20,1), justification='right'), sg.I(key="t_dead", default_text="7", size=(10,1))],
        [sg.T("Transmittance", size=(20,1), justification='right'),      sg.I(key='tau', default_text='0.90', size=(10,1)),
        sg.T("Coincidence number", size=(20,1), justification='right'), sg.I(key="coinc_thr", default_text="6", size=(10,1))],
        [sg.T("")],

        [sg.T("Physical parameters", justification='center', size=(30,1), font=("Helvetica", 12, "bold")),
         sg.T("Jitters & TDC", justification='center', size=(30,1), font=("Helvetica", 12, "bold"))],
        [sg.T("Range (m)", size=(20,1), justification='right'), sg.I(key="range_min", default_text="10", size=(4,1)), sg.I(key="z", default_text="200", size=(5,1)),
         sg.T("Spad sigma (ps)", size=(20,1), justification='right'), sg.I(key="spad_j", default_text="72", size=(10,1))],
        [sg.T("Number of pulses", size=(20,1), justification='right'), sg.I(key='n_imp', default_text='30', size=(10,1)),
         sg.T("TDC sigma (ps)", size=(20,1), justification='right'), sg.I(key='tdc_j', default_text='100', size=(10,1))],
        [sg.T("Target reflectivity", size=(20,1), justification='right'), sg.I(key='rho_tgt', default_text='0.2', size=(10,1)),
         sg.T("N bit (TDCxHIST)", size=(20,1), justification='right'), sg.I(key='n_bit_tdc', default_text='12', size=(5,1)),
                                                                    sg.I(key='n_bit_hist', default_text='5', size=(4,1))],
        [sg.T("", size=(30,4))],
        [sg.Text("", size=(30)), sg.Submit(auto_size_button=True), sg.Cancel(auto_size_button=True)]

    ]

    window = sg.Window("LIDAR starter", layout=layout, resizable=True)

    event, values = window.read()

    if event=='Cancel':
        window.close()
    elif event=='Submit':
        main.execute_main(params=values)

if __name__ == '__main__':
    gui()