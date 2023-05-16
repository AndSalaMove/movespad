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