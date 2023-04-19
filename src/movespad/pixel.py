import numpy as np
import random
import matplotlib.pyplot as plt
from itertools import product
from movespad import spad, params as pm
from tqdm import tqdm, trange


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


    def _pbc(self, index):
        """Base function for pbc"""
        while index<0 or index>=self.size:
            if index < 0:
                 index += self.size
            elif index >= self.size:
                index -= self.size
        return index


    def pbc(self, pos: tuple):
        """ 
        Return (i,j) position scaled with Periodic Boundary Conditions
        """
        return (self._pbc(pos[0]), self._pbc(pos[1]))


    def get_neighbours(self, pos):
        """Calculate neighbour spad in a pixel (with Periodic Boundary Coindition)"""

        direct = [self.pbc((pos[0]-1, pos[1])),  self.pbc((pos[0]+1, pos[1])),
                  self.pbc((pos[0],   pos[1]+1)), self.pbc((pos[0],   pos[1]-1))]

        diagonal = [self.pbc((pos[0]-1, pos[1]-1)),   self.pbc((pos[0]+1, pos[1]-1)),
                    self.pbc((pos[0]-1,  pos[1]+1)), self.pbc((pos[0]+1,   pos[1]+1))]


        return {
            'direct' : direct,
            'diagonal' : diagonal
        }


    def crosstalk(self, xtalk_probs):
        """Model optical crosstalk among neighbouring SPADs.
        Input: List of timestamps after PDP
        Output: List of timestamps ready for t dead filtering"""

        for spd in tqdm(self.timestamps, leave=False):
            neigh = self.get_neighbours(spd.position)
            for photon in spd.timestamps:

                for dir_neigh in neigh['direct']:

                    rnd = np.random.uniform()
                    if rnd < xtalk_probs['r']:

                        neigh_ix = [i for i,s in enumerate(self.timestamps)
                                    if s.position==dir_neigh][0]
                        self.timestamps[neigh_ix].timestamps = sorted(
                        np.append(self.timestamps[neigh_ix].timestamps,
                        spad.Timestamp(photon.time, photon.type))
                    )
                        
                for dia_neigh in neigh['diagonal']:

                    rnd = np.random.uniform()
                    if rnd < xtalk_probs['ur']:

                        neigh_ix = [i for i,s in enumerate(self.timestamps)
                                    if s.position==dia_neigh][0]
                        self.timestamps[neigh_ix].timestamps = sorted(
                        np.append(self.timestamps[neigh_ix].timestamps,
                        spad.Timestamp(photon.time, photon.type))
                    )


    def t_dead_filter(self, t_dead, pdp, ap_prob):
        """Apply t dead filter and afterpulsing
        to all SPADs in the pixel."""
        
        for i in trange(len(self.timestamps), leave=False):
            self.timestamps[i].timestamps = spad.Spad.process_events(
                self.timestamps[i].timestamps, t_dead, ap_prob)


    def coincidence(self, thr=3, window=1e-9):

        final = []

        all_photons = []
        for kst in self.timestamps:
            all_photons.extend(kst.timestamps)

        all_photons = sorted(all_photons, key=lambda x: x.time)

        for pht in tqdm(all_photons, leave=False):

            counts = [
                len([elem for elem in lst.timestamps if pht.time <= elem.time <= pht.time+window])
                    for lst in self.timestamps
            ]
            #breakpoint()
            if sum(counts) >= thr:
                if len(final)==0:
                    final.append(spad.Timestamp(pht.time, type='v'))
                    #print(f"First coincidence: {pht.time} (count = {sum(counts)})")

                elif pht.time - final[-1].time > window:
                    final.append(spad.Timestamp(pht.time, type='v'))
                    #print(f"Added coincidence: {pht.time} (count = {sum(counts)})")
                    pass
                else:
                    #print(f"Coincidence found for {pht.time} (count = {sum(counts)}) but too close to previous one")
                    pass
            else:
                #print(f"No coincidence found for {pht.time} (count = {sum(counts)})")
                pass

        return final


    def plot_events(self, times, las_spec, survived=None, v_lines=None):

        plt.figure()
        plt.title("Events on each SPAD")

        centers = np.asarray([2*pm.Z/pm.C + n * pm.PULSE_DISTANCE for n in range(pm.N_IMP)])
        left = centers - 1.5 * pm.SIGMA_LASER
        right = centers + 1.5 * pm.SIGMA_LASER

        sv = [s.time for s in survived]

        # for j in range(len(sv)):
        #     plt.axvline(sv[j] - 1.5*pm.SIGMA_LASER, linestyle='dotted', color='firebrick')
        #     plt.axvline(sv[j] + 1.5*pm.SIGMA_LASER, linestyle='dotted', color='firebrick')

        # for i in range(len(centers)):
        #     plt.axvline(left[i], linestyle='dotted', color='black')
        #     plt.axvline(right[i], linestyle='dotted', color='black')

        plt.plot(times, las_spec/np.max(las_spec), color='green', alpha=0.5)
        for i in range(len(self.timestamps)):
            bkg = [elem.time for elem in self.timestamps[i].timestamps if elem.type=='bkg']
            las = [elem.time for elem in self.timestamps[i].timestamps if elem.type=='las']
            xt = [elem.time for elem in self.timestamps[i].timestamps if elem.type=='xt']
            plt.scatter(bkg, [.1 * (i+1)] * len(bkg), color='navy', s=3)
            plt.scatter(las, [.1 * (i+1)] * len(las), color='red', s=10)
            plt.scatter(xt,  [.1 *  (i+1)] * len(xt), color='greenyellow', s=5)

        if survived:
            sv = [elem.time for elem in survived]
            plt.scatter(sv, [0]*len(sv), color='darkviolet', s=12)

        if v_lines:
            for line in v_lines:
                plt.axvline(x = line, linestyle='dashed', alpha=0.5, color='lightsteelblue')
        plt.xlabel("Time")
        plt.show()


    def print_timestamps(self,):

        for ts in self.timestamps:
            print(ts.timestamps)