import numpy as np

# UNITS 
# TIME: s
# SPACE: m
# POWER: W  

PI = np.pi
H = 6.62607015e-34 # in SI units 
C = 299792458      # in SI units

FF = .265
TAU_OPT = .66
RHO_TGT = .75
F_LENS = .006
D_LENS = .005
F_HASH = F_LENS / D_LENS

THETA_E_DEG = 1.7
THETA_E_RAD = THETA_E_DEG * PI / 180
Z = .8 #m  

SIGMA_LASER = 250e-12 / 2.355
PULSE_ENERGY = 6.2e-11
PULSE_DISTANCE = 1.35e-6

PIXEL_AREA = 3600e-12
PDP = .9925 #photon detection probability
T_DEAD = 12.5e-9  
T_QUENCH = 1e-9
T_THR = 3e-9 
AP_PROB = 0.01 #after pulsing integrated probability

PHOTON_WAVEL = 405e-9
E_PH = H * C / PHOTON_WAVEL # photon energy

BKG_POWER = 10.5 # 10.5 W /m2, uscita da un conto fatto con SFdA
DCR = 6800 #Hz, Preso dal paper FBK