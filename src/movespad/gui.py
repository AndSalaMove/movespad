import PySimpleGUI as sg
import os, pathlib


def gui():


    base_path = pathlib.Path(__file__).parent.parent.parent.absolute()
    img_path = os.path.join(base_path, "img", "movex.png")
    sg.theme("DarkBlue15")
    layout = [
        #[sg.Image(img_path, size=(1000, 500))],
        [sg.T("Laser specifications", justification='center', size=(70,2))],
        [sg.T("Potenza laser (W)", size=(25,1), justification='right'), sg.I(key='laser_power', default_text='60', size=(10,1))],
        [sg.T("Sigma laser  (ns)", size=(25,1), justification='right'), sg.I(key='laser_sigma', default_text='1.9108', size=(10, 1))],

        [sg.T("Pulse distance (us)"), sg.I(key='pulse_distance', default_text='1.35')],
        [sg.T("Optics", justification='center', size=(70,2))],
        [sg.T("Focal length (mm)"), sg.I(key='f_lens', default_text='5')],
        [sg.T("Lens diameter (mm)"), sg.I(key='d_lens', default_text='6')],
        [sg.T("Transmittance"), sg.I(key='tau', default_text='0.90')],

        [sg.T("Pixel specifications", justification='center', size=(35,2)), sg.T("Target specifications", justification='center', size=(35, 2))],
        [sg.T("Pixel size (SPADs per size)", size=(10,1)), sg.I(key='pixel_size', default_text='3', size=(7,1)), sg.T("Reflectivity", size=(10,1)), sg.I(key='rho_tgt', default_text="0.20", size=(7,1))],
        [sg.T("Fill factor"), sg.I(key='fill_factor', default_text='0.99')],
        [sg.Submit(), sg.Cancel()]

    ]

    window = sg.Window("LIDAR starter", layout=layout)

    event, values = window.read()

    if event=='Cancel':
        window.close()
    elif event=='Submit':
        print(values) 

if __name__ == '__main__':
    gui()