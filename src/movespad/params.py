import numpy as np

# UNITS
# TIME: s
# SPACE: m
# POWER: W

PI = np.pi
H = 6.62607015e-34  # in SI units
C = 299792458      # in SI units

FF = .98
TAU_OPT = .9
RHO_TGT = .2
F_LENS = .020 #m
D_LENS = .016 #m
F_HASH = F_LENS / D_LENS

THETA_H = 1.5e-3 #rad
THETA_V = 1.5e-3 #rad
Z = 200  # m

SIGMA_LASER = 4.5e-9 / 2.355  # 4e-9 / 2.355
PULSE_POWER = 4.5
PULSE_ENERGY = np.sqrt(2*PI)*SIGMA_LASER*PULSE_POWER
PULSE_DISTANCE = 1.5e-6#2*Z/C

PIXEL_SIZE = 3
PIXEL_AREA = (10.17e-6*PIXEL_SIZE)**2
PDP = .2  # photon detection probability
T_DEAD = 7e-9

AP_PROB = 0.014  # afterpulsing integrated probability

PHOTON_WAVEL = 405e-9
E_PH = H * C / PHOTON_WAVEL  # photon energy

BKG_POWER = 0.2 * 10 * 1.17  # irradianza * larghezza filtro * klux
DCR = 6800  # Hz, Preso dal paper FBK
COINCIDENCE_THR = 5

XTALK_PROBS = {
    'r': 3.5e-2 / 4,  # "upper"
    'ur': 1.7e-2 / 4,  # "upper right"
}

N_IMP = 150