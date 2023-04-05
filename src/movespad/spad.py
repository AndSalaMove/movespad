import numpy as np
import matplotlib.pyplot as plt
from movespad import pixel

class SpadArray(object):
    def __init__(self, n=2) -> None:
        self.n = n
        self.array = np.array(
            [[pixel.Pixel(), pixel.Pixel()],
             [pixel.Pixel(), pixel.Pixel()]]
        )
        self.timestamps = np.zeros_like(self.array)


