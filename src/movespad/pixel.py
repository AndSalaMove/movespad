import numpy as np
import random
import matplotlib.pyplot as plt
from itertools import product
from movespad import spad, params as pm


class Pixel():

    def __init__(self, size: int):
        self.size = size
        self.timestamps =  [spad.Spad(pos = comb) for comb in product(range(self.size), repeat=2)]


    def create_and_split(self, laser_times, bkg_times, pdp=pm.PDP):
        """Apply the PDP filter and then split
        the impinging photons onto the different SPADs
        on a pixel. (Distribution occurs randomly)

        :param laser_times: Array of floats
        :param bkg_times: Array of floats
        :param pdp: photon detection probabilty, defaults to pm.PDP
        """

        laser_tps = spad.generate_timestamps(laser_times, 'las', pdp)
        bkg_tps = spad.generate_timestamps(bkg_times, 'bkg', pdp)

        pix_tstamps = np.asarray(
            sorted(np.concatenate((laser_tps, bkg_tps)), key= lambda x: x.time),
            dtype = spad.Timestamp
        )

        pix_tstamps = np.asarray([p for p in pix_tstamps if p.detected])

        for pix in pix_tstamps:

            index = np.random.randint(0, self.size**2)
            self.timestamps[index].timestamps.append(pix)


    def get_neighbours(self, pos):

        direct = [(pos[0]-1, pos[1]),   (pos[0]+1, pos[1]),
                  (pos[0],   pos[1]+1), (pos[0],   pos[1]-1)]

        direct = [d for d in direct if all(0 <= elem < self.size for elem in d)]

        diagonal = [(pos[0]-1, pos[1]-1),   (pos[0]+1, pos[1]-1),
                  (pos[0]-1,   pos[1]+1), (pos[0]+1,   pos[1]+1)]
        
        diagonal  = [d for d in diagonal if all(0 <= elem < self.size for elem in d)]

        return {
            'direct' : direct,
            'diagonal' : diagonal
        }


    def crosstalk(self, xtalk_probs):
        """Model optical crosstalk among neighbouring SPADs.
        Input: List of timestamps after PDP
        Output: List of timestamps ready for t dead filtering"""

        for s, spd in enumerate(self.timestamps):
            neigh = self.get_neighbours(spd.position)
            for photon in spd.timestamps:

                rnd = np.random.uniform()
                if rnd < xtalk_probs['u']:

                    neigh_pos = random.choice(neigh['direct'])
                    neigh_ix = [i for i,s in enumerate(self.timestamps)
                                    if s.position==neigh_pos][0]
                    self.timestamps[neigh_ix].timestamps = sorted(
                        np.append(self.timestamps[neigh_ix].timestamps,
                        spad.Timestamp(photon.time, photon.type))
                    )

                elif xtalk_probs['u'] < rnd < xtalk_probs['u'] + xtalk_probs['ur']:
                    neigh_pos = random.choice(neigh['diagonal'])
                    neigh_ix = [i for i,s in enumerate(self.timestamps)
                                    if s.position==neigh_pos][0]
                    self.timestamps[neigh_ix].timestamps = sorted(
                        np.append(self.timestamps[neigh_ix].timestamps,
                        spad.Timestamp(photon.time, photon.type))
                    )
 
                else:
                    pass

    def t_dead_filter(self, t_dead, pdp, ap_prob):
        """Apply t dead filter and afterpulsing
        to all SPADs in the pixel."""
        
        for i in range(len(self.timestamps)):
            self.timestamps[i].timestamps = spad.Spad.process_events(
                self.timestamps[i].timestamps, t_dead, ap_prob)

        #applicare coincidenze

    def plot_events(self, times, las_spec):

        plt.figure()
        plt.title("Events on each SPAD")

        plt.plot(times, las_spec/np.max(las_spec), color='green', alpha=0.5)
        for i in range(len(self.timestamps)):
            bkg = [elem.time for elem in self.timestamps[i].timestamps if elem.type=='bkg']
            las = [elem.time for elem in self.timestamps[i].timestamps if elem.type=='las']
            xt = [elem.time for elem in self.timestamps[i].timestamps if elem.type=='xt']
            plt.scatter(bkg, [.25 * i] * len(bkg), color='navy', s=3)
            plt.scatter(las, [.25 * i] * len(las), color='red', s=10)
            plt.scatter(xt, [.25 * i] * len(xt), color='greenyellow', s=5)

        plt.xlabel("Time")
        plt.show()

    def print_timestamps(self,):

        for ts in self.timestamps:
            print(ts.timestamps)