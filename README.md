# movespad


## Introduction

This repository includes a python package to simulate a SPAD pixel with customisable parameters.
This simulation will be used to understand the capabilities of designing an actual SPAD array.


## Installation and usage

1. Clone the repository via SSH or HTTPS
2. Go inside the `movespad` directory
3. Run `pip install -e .`
4. The `spad-run` command is now installed and ready to go.


## Parameters

A basic user interface appears with the following customisable parameters:

Laser specifications
- **Power per pixel**:
- **Power budget**:
- **Laser sigma**:
- **Laser wavelength**
- **Beam divergence**
- **Illumination mode**:

- **Field Of View**
- **Resolution**
- **Frames per second**

Pixel specifications
- **SPADs per side**: How many SPADs per each side of the pixel
- **Physical matrix**: Dimensions of the total SPAD matrix
- **Fill factor**
- **SPAD size**: Dimension of the single SPAD
- **Photon Detection Probability**
- **T dead**: Time during which a SPAD is shut off after absorbing a photon
- **Coincidence number**: Number of SPADs that need to be simultaneously hit in order to register a count
- **SPAD sigma**
- **Afterpulsing probability**
- **Crosstalk probability**
- **Dark Count Rate**

Optical speficiations
- **Focal length**
- **Lens diameter**
- **Lens transmittance**
- **Optical filter FWMH**: The solar irradiance spectrum (obtained from *pvlib*) is multiplied element-wise with a gaussian centered at the laser wavelength. This is multiplied by a linearized silicon absorption spectrum, and it simulates the total background contribution across the spectrum.


Physical parameters
- **Range**: Minimum and maximum LIDAR range
- **Target distance**: Distance of the simulated object
- **Number of pulses**: Number of laser pulses simulated
- **Target reflectivity**: Environment reflectivity
- **Background intensity**: Background illuminance in kilolux 

TDC specifications
- **Measurement resolution**: Depth resolution
- **TDC sigma**: TDC jitter (gaussian std deviation)
- **N bit (TDC + histogram depth)**: Number of bits to build the histogram
- **Clock frequency**: 
- **Number of pads**: Number of simulataneous readings
- **Multi hit**:

