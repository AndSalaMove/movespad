import numpy as np
import matplotlib.pyplot as plt
from movespad import spad, params as pm


class Pixel():
    def __init__(self, size: int):
        self.size = size
        self.timestamps =  [[] for _ in range(self.size**2)]
        self.spads = [[spad.Spad(), spad.Spad()], [spad.Spad(), spad.Spad()]]

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

           #TODO ripristinare array
            x= np.random.randint(0, self.size**2)
            self.timestamps[int(x)].append(pix)


    def process_events(self, t_dead, pdp, ap_prob):
        """Apply t dead filter and afterpulsing
        to all SPADs in the pixel."""

        spd = spad.Spad()
        
        for i in range(len(self.timestamps)):
            self.timestamps[i] = spd.process_events(self.timestamps[i], t_dead, pdp, ap_prob)

        #applicare coincidenze

    def plot_events(self, times, las_spec):

        plt.figure()
        plt.title("Events on each SPAD")

        plt.plot(times, las_spec/np.max(las_spec), color='green', alpha=0.5)
        for i in range(len(self.timestamps)):
            bkg = [elem.time for elem in self.timestamps[i] if elem.type=='bkg']
            las = [elem.time for elem in self.timestamps[i] if elem.type=='las']
            plt.scatter(bkg, [.25 * i] * len(bkg), color='navy', s=3)
            plt.scatter(las, [.25 * i] * len(las), color='red', s=8)

        plt.xlabel("Time")
        plt.show()