import numpy as np

def gaussian(x, mean, sigma, amplitude=1, offset=0):
    return amplitude / sigma / np.sqrt(2 * np.pi) * np.exp(-(x - mean) ** 2 / 2 / sigma ** 2) + offset