"""Compute solar irradiance spectrum"""

import numpy as np
import pandas as pd
from pvlib import spectrum, solarposition, irradiance, atmosphere
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

from movespad import laser


def get_solar_spectrum(klux: float):
    lat = 45
    lon = 13
    tilt = 75
    azimuth = 180
    pressure = 101300  # sea level, roughly
    water_vapor_content = 0.5  # cm
    tau500 = 0.1
    ozone = 0.31  # atm-cm
    albedo = 0.2

    times = pd.date_range('2022-07-14 10:00', freq='h', periods=1, tz='Etc/GMT+1')
    solpos = solarposition.get_solarposition(times, lat, lon)
    aoi = irradiance.aoi(tilt, azimuth, solpos.apparent_zenith, solpos.azimuth)
    relative_airmass = atmosphere.get_relative_airmass(solpos.apparent_zenith,
                                                       model='kasten1966')

    spectra = spectrum.spectrl2(
        apparent_zenith=solpos.apparent_zenith,
        aoi=aoi,
        surface_tilt=tilt,
        ground_albedo=albedo,
        surface_pressure=pressure,
        relative_airmass=relative_airmass,
        precipitable_water=water_vapor_content,
        ozone=ozone,
        aerosol_turbidity_500nm=tau500,
    )

    lambdas = spectra['wavelength'].reshape(-1) * 1e-9
    irrad = spectra['poa_global'].reshape(-1)

    return lambdas, irrad * klux/100


def bkg_contrib(laser_l, fwhm, klux) -> float:

    # Apply gaussian modulation to the bkg spectrum
    lambdas, spectrum = get_solar_spectrum(klux)

    sigma = fwhm / 2.355
    gauss = laser.gauss_1d(lambdas, laser_l, sigma) * np.sqrt(2*np.pi) * sigma

    w_spec = np.multiply(spectrum, gauss)

    sil_pde = np.asarray([silicon_pde(lm) for lm in lambdas])

    f_spec = 5  * np.multiply(w_spec, sil_pde)

    bkg_pow = np.trapz(f_spec)

    # plt.plot(lambdas, spectrum, label='OG spec')
    # plt.plot(lambdas, gauss, label='Gaussian')
    # plt.plot(lambdas, sil_pde, label='silicon')
    # plt.plot(lambdas, w_spec, label='1 filtered')
    # plt.plot(lambdas, f_spec, label='f filtered')
    # plt.legend()
    # plt.show()

    return bkg_pow


def silicon_pde(lmbd) -> float:

    if 350e-9 < lmbd <=500e-9:
        return 0.3 + (0.65-0.3)/(500e-9 - 400e-9) * (lmbd - 400e-9)
    elif 500e-9 < lmbd <= 600e-9:
        return 0.65
    elif 600e-9 < lmbd <= 1000e-9:
        return 0.65 - 0.45 / 305e-9 * (lmbd - 600e-9)
    else:
        return 0