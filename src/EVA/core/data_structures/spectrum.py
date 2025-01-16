from dataclasses import dataclass
import numpy as np

@dataclass
class Spectrum:
    """
    The 'Spectrum' class holds the data from a single detector for a single run.
    It holds the x and y data as numpy arrays.
    It also holds the run number and detector the dataset came from.
    """
    detector: str
    run_number: str
    x: np.ndarray
    y: np.ndarray
