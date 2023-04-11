"""Model single SPAD behaviour"""

import numpy as np
import matplotlib.pyplot as plt
from movespad import params as pm, laser, bkg
from time import time

class Timestamp(object):

    def __init__(self, time, type='v', pdp=pm.PDP) -> None:
        self.time = time
        self.type = type
        rnd = np.random.uniform()
        self.detected = rnd < pdp
        # print(f"Random number: {rnd:.3f}. PDP: {pdp} Detected: {self.detected}")
        self.alive = True

        assert self.type in ['las', 'bkg', 'ap', 'v', 'xt']

    def __repr__(self) -> str:
        return f"{self.time:.2E} ({self.type})"
    
    def __eq__(self, other):
        return self.time == other.time
    
    def __lt__(self, other):
        return self.time < other.time
    
    def __gt__(self, other):
        return self.time > other.time
    
    def set_living(self, state: bool):
        self.alive = state


def generate_timestamps(time_array, type, pdp):
    return [Timestamp(val, type, pdp) for val in time_array]


def plot_timestamps(ts, ax, z=0):
    """Simple timestamp scatterplot."""
    for type in ['las', 'bkg']:
        x = [elem.time for elem in ts if elem.type==type]
        ax.scatter(x, [z]*len(x), color='red' if type=='las' else 'navy', s=3 if type=='bkg' else 12)


def generate_afterpulse(timestamps, i, t_dead, ap_prob=pm.AP_PROB):
    """Generate an afterpulsing photon with a given
    probability and exponential distribution."""
    if np.random.uniform() < ap_prob:
        t_after = timestamps[i].time + np.random.exponential(scale=t_dead/6)
        timestamps = np.append(timestamps, Timestamp(t_after, 'ap'))
    return np.asarray(sorted(timestamps))


class Spad(object):

    def __init__(self, pos: tuple, pdp=pm.PDP) -> None:
        self.pdp = pdp
        self.timestamps = []
        self.position = pos


    @staticmethod
    def process_events(pix_tstamps, t_dead, ap_prob=pm.AP_PROB):
        """
        Apply the following procedures to the list of impinging photons
         - Tdead filter
         - Afterpulsing
        
        :param laser_times: Array of floats
        :param bkg_times: Array of floats
        """

        absorbed = []
        for i, stamp in enumerate(pix_tstamps):

            pix_tstamps = generate_afterpulse(pix_tstamps, i, t_dead, ap_prob)

            if stamp.alive:
                absorbed.append(stamp)

                dead_time = stamp.time + t_dead

                incl_ph =  pix_tstamps[(pix_tstamps > Timestamp(stamp.time)) &
                                       (pix_tstamps < Timestamp(dead_time))].tolist() 

                while incl_ph != []:
                    list(map(lambda x: x.set_living(False), incl_ph))
                    dead_time = incl_ph[-1].time + t_dead

                    incl_ph =  pix_tstamps[(pix_tstamps > Timestamp(incl_ph[-1].time)) &
                                           (pix_tstamps < Timestamp(dead_time))].tolist() 

        return absorbed


    def plot_events_and_spectra(self, times, detected, laser_spec, bkg_spec):

        _, ax = plt.subplots()
        ax.set_title("Single Pixel simulation")
        plot_timestamps(detected, ax, 0.5*max(laser_spec))
        ax.plot(times, laser_spec, color='green', alpha=0.25, label='laser spectrum')
        ax.plot(times, bkg_spec, color='purple', alpha=0.25, label='bkg spectrum')
        ax.legend(loc='upper right')
        plt.show()