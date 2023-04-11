import numpy as np

# UNITS 
# TIME: s
# SPACE: m
# POWER: W  

PI = np.pi
H = 6.62607015e-34 # in SI units 
C = 299792458      # in SI units

FF = .99265
TAU_OPT = .66
RHO_TGT = .75
F_LENS = .006
D_LENS = .005
F_HASH = F_LENS / D_LENS

THETA_E_DEG = 1.7
THETA_E_RAD = THETA_E_DEG * PI / 180
Z = .8 #m

SIGMA_LASER = 250e-12 / 2.355 # 4e-9 / 2.355
PULSE_ENERGY = 6.2e-11 #4e-8  
PULSE_DISTANCE = 1.35e-6

PIXEL_AREA = 3600e-12
PDP = .2 #photon detection probability
T_DEAD = 7e-9

AP_PROB = 0.01 #after pulsing integrated probability

PHOTON_WAVEL = 405e-9
E_PH = H * C / PHOTON_WAVEL # photon energy

BKG_POWER = 3 # 10.5 W /m2, uscita da un conto fatto con SFdA
DCR = 6800 #Hz, Preso dal paper FBK

XTALK_PROBS = {
    'u': 3.5e-2, #"upper"
    'ur':1.7e-2 # "upper right"
}