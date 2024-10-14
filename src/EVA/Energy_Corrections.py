import numpy as np
from EVA.app import get_config
from EVA.data_structures import Dataset

def Energy_Corrections(data):
    config = get_config()

    # For each dataset in the list, return energy corrected data if energy correction is wanted
    for dataset in data:
        detector = dataset.detector
        if config.parser[detector]["use_energy_correction"]:
            gradient = config.parser[detector]["e_corr_gradient"]
            offset = config.parser[detector]["e_corr_offset"]
            dataset.x = lincorr(dataset.x, gradient, offset)
    return data

def lincorr(x, m, c):
    new_x = x*float(m)+float(c)
    return new_x
