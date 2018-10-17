import numpy as np
import matplotlib.pyplot as plt


class Axiom:
    def __init__(self, L, W, pe):
        """
        :param L:   int the # of cols in grid
        :param W:   int the # of rows in grid
        :param pe:  error possibility
        """
        self.length = L
        self.width = W
        self.pe = pe
        self.PolicyValue = np.zeros(W * L)

        self.RewardMarix = np.zeros(W * L)

        # VectorField array indicates the vector field pointing to the goal point.
        self.VectorField = np.zeros(W * L)

        # map the time directions to radians representation, in which 3 represents 2pi and 9 represents pi.
        times = [i for i in range(12)]
        rads = np.roll([(2 * np.pi - (time / 12) * 2 * np.pi) for time in times], 3)

        # create a dictionary to store times and radians info.
        self.time_rads = {k: v for k, v in zip(times, rads)}

        # stay-0, right-3, down-6, left-9, up-12
        self.ValidAction = [0, 3, 6, 9, 12]

        # Counter-Clockwise-0, not rotate-0, Clockwise-1
        self.rots = [-1, 0, 1]

        self.Actions = np.zeros(5*2, 2)







