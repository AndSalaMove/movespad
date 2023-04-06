"""Model SPAD pixel behaviour"""

import numpy as np
import matplotlib.pyplot as plt
from movespad import params as pm, laser, bkg
from time import time

class Timestamp(object):

    def __init__(self, time, type='v', pdp=pm.PDP) -> None:
        self.time = time
        self.type = type
        self.detected = np.random.uniform() < pdp
        self.alive = True

        assert self.type in ['las', 'bkg', 'ap', 'v']

    def __repr__(self) -> str:
        return f"{self.time:.2E} ({self.type})"
    
    def __eq__(self, other):
        return self.time == other.time
    
    def __lt__(self, other):
        return self.time < other.time
    
    def __gt__(self, other):
        return self.time > other.time



def generate_timestamps(time_array, type, pdp):
    return [Timestamp(val, type, pdp) for val in time_array]


def plot_timestamps(ts, ax, z=0):

    for type in ['las', 'bkg']:
        x = [elem.time for elem in ts if elem.type==type]
        ax.scatter(x, [z]*len(x), color='red' if type=='las' else 'navy', s=3 if type=='bkg' else 12)


class Pixel(object):

    def __init__(self, pdp=pm.PDP) -> None:
        self.area = pm.PIXEL_AREA
        self.pdp = pdp


    def generate_afterpulse(self, timestamps, i, t_dead, ap_prob=pm.AP_PROB):

        if np.random.uniform() < ap_prob:
            t_after = timestamps[i].time + np.random.exponential(scale=t_dead/6)

            timestamps = np.append(timestamps, Timestamp(t_after, 'ap'))

        return np.asarray(sorted(timestamps))


    def process_events(self, laser_times, bkg_times, t_dead, t_thr, t_quench,
                       pdp=pm.PDP, ap_prob=pm.AP_PROB):
        """
        Apply the following procedures to the list of impinging photons
         - PDP (photon detection efficiency)
         - Tdead filter
         - Afterpulsing
        
        :param laser_times: Array of floats
        :param bkg_times: Array of floats
        """

        laser_tps = generate_timestamps(laser_times, 'las', pdp)
        bkg_tps = generate_timestamps(bkg_times, 'bkg', pdp)

        pix_tstamps = np.asarray(
            sorted(np.concatenate((laser_tps, bkg_tps)), key= lambda x: x.time),
            dtype = Timestamp
        )

        pix_tstamps = np.asarray([p for p in pix_tstamps if p.detected])

        absorbed = []

        for i, stamp in enumerate(pix_tstamps):

            pix_tstamps = self.generate_afterpulse(pix_tstamps, i, t_dead)

            if stamp.alive:
                absorbed.append(stamp)

                dead_time = stamp.time + t_dead
                target_time = stamp.time + t_thr
                quench_time = stamp.time + t_quench

                included_photons =  pix_tstamps[(pix_tstamps > Timestamp(stamp.time)) &
                                                (pix_tstamps < Timestamp(dead_time))].tolist() 

                #TODO implementare incremento lineare
                # vedere se posso evitare il ciclo for e andare direttamente all'ultimo
                for j, phot in enumerate(included_photons):

                    if phot.time < quench_time:
                        pix_tstamps[i+j+1].alive = False
                        continue
                    elif quench_time < phot.time < target_time:
                        # non contare il fotone ma allunga il target time
                        pix_tstamps[i+j+1].alive = False
                        old_dead_time = dead_time
                        dead_time = phot.time + t_dead
                        target_time = phot.time + t_thr
                        quench_time = phot.time + t_quench
                        extra_photons = [p for p in pix_tstamps if old_dead_time <= p.time < dead_time]
                        included_photons.extend(extra_photons)
                    else:
                        break
                        #vai al prossimo fotone e riazzera il dead_time    

        return absorbed


    def plot_events_and_spectra(self, times, detected, laser_spec, bkg_spec):

        _, ax = plt.subplots()
        ax.set_title("Single Pixel simulation")
        plot_timestamps(detected, ax, 0.5*max(laser_spec))
        ax.plot(times, laser_spec, color='green', alpha=0.25, label='laser spectrum')
        ax.plot(times, bkg_spec, color='purple', alpha=0.25, label='bkg spectrum')
        ax.legend(loc='upper right')
        plt.show()

