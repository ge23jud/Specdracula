import numpy as np
from scipy.constants import h, c

class HelperFunctions():

    def wavelength_energy_converter(self, array):
        return h*c/array *1e9 /1.6022 * 1e19 

