"""This module includes all the long tooltips that would otherwise make the code quite messy"""


nbit_hist = """
Dimensione della porzione dell'istogramma completo che viene effettivamente
portato fuori dal chip. Modellizza il fatto che per motivi di memoria
disponibile on-chip in genere vengono portati in uscita degli istogrammi
ridotti se non solo il picco dell'istogramma"""

hit_count = """
Average number of SPADs hit for a single laser pulse.
This number is calculated with a Monte Carlo with 250 runs. 
Compare this number with the coincidence threshold and,
if necessary, change the Power per Pixel parameter.
"""

matrix = """
Matrix size needed to perform a flash (i.e. to illuminate the 
entire FOV with a single laser shot) with the given resolution.
"""

ppp = """
Power per pixel assuming flash mode. Obtained by the
total power budget and number of pixels
"""

npix_tt = """
Number of pixel that can be reached by the laser (assuming Scanning mode)
with each shot. This count is obtained from the power budget and the power per pixel"""

power_per_pixel = """
Peak power on the single pixel. This parameter is considered only
for Scanning mode, because in flash mode the power per pixel is
obtained from the power budget and the number of pixels"""

ill_mode = """
Illumination mode. FLASH = the whole fov is illuminated at once.
SCANNING: the matrix scans a subsection of the fov, and it needs to
be moved to obtain a frame"""

k_pix = """
Number of pixels hit simultaneously by one laser shot.
This parameter is mutually exclusive with the power per pixel,
and it is only use for pre-output calculations.
"""

filtr = """
Width of the gaussian filter for the background.
A gaussian with this FWHM is multiplied by the Silicon absorption
spectrum and the solar irradiance spectrum. The integral of this
triple multiplication gives out the background contribution (after scaling
with the klux factor)"""

n_pulses = """
Number of pulses for the simulation. This parameter sets the
length of the total simulation."""

multi_hit = """
Number of coincidence hits that the device can register. If set to 1,
the multi hit becomes a simpler 'single-hit' architecture."""

n_sig = """
Number of standard deviations that set the distance between two
consecutive laser pulses. Default (8) is a rough estimate"""

seed = """
Random number generator seed. Use this for reproducibility."""

fix_mn = """
This pre-output parameters are calculated by taking into account
the input values for the matrix. The FOV is calculated based on
this value."""

fix_fov = """
This pre-output parameters are calculated by taking into account
the input values for FOV. The matrix size is the one needed to cover
the whole FOV with a single Flash.
"""

scan1 = """
This pre output parameters are relative to a scanning mode, where
the power per pixel parameter is fixed. Hence, the number of pixels hit
by a single laser shot is determined based on the power budget and
the power per pixel."""

scan2 = """
This pre output parameters are relative to a scanning mode, where
thejnumbers of pixel hit per shot is fixed. Hence, the npower per pixel
 is determined based on the power budget and n_pixel_per_shot"""