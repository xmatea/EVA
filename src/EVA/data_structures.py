from dataclasses import dataclass
from enum import Enum

import numpy as np
from copy import deepcopy
from pandas.core.apply import normalize_keyword_aggregation

from EVA.Energy_Corrections import lincorr
from EVA.Normalise import normalise_events, normalise_counts

# Useful Enum class for binding array indices and detector names
class Detector(Enum):
    GE1 = 0
    GE2 = 1
    GE3 = 2
    GE4 = 3
    GE5 = 4
    GE6 = 5
    GE7 = 6
    GE8 = 7

@dataclass
class Dataset:
    """
    The 'Dataset' class holds the data from a single detector for a single run.
    It holds the x and y data as numpy arrays.
    It also holds the run number and detector the dataset came from.
    """
    detector: str
    run_number: str
    x: np.ndarray
    y: np.ndarray

class Run:
    """
    The 'Run' class holds lists of 'Datasets' from all the detectors from a single run, as well as the run number,
    normalisation status and the comment from a single run.

    'detectors' is a list of names of the detectors in the Dataset lists. ex: ["GE1", "GE3"].

    'raw' contains a list of Datasets, one Dataset for each detector, with no energy calibration or normalisation
    applied - read from the .dat files as-is. The order of the Datasets in the list corresponds to the order specified
    in 'detectors'.

    'raw_e_corr' is a copy of raw but with the energy calibration applied as specified by config.ini. If no energy
    calibration is specified for any detectors in the config, it is just a copy of 'raw'.

    'data' contains a list of Datasets with the energy calibration and normalisation as specified in config.ini.
    This is the main data to be used for plotting and such.
    """
    def __init__(self, raw : list[Dataset], loaded_detectors : list[str], run_num: str, start_time: str, end_time: str,
                 events_str: str, comment: str):

        # Main data containers
        self.raw = raw # raw, unprocessed data as read from file - is NOT to be changed
        self.data = deepcopy(raw) # deepcopy ensures that raw and data do not point to the same memory address and thus
        # any changes to data will not change raw

        # Basic run info
        self.loaded_detectors = loaded_detectors
        self.run_num = run_num

        # Normalisation and energy correction info (initial read from default.ini)
        self.normalisation = None
        self.normalise_which = []
        self.e_corr_params = None
        self.e_corr_which = []

        # Metadata from comment file (may not be available)
        self.start_time = start_time
        self.end_time = end_time
        self.events_str = events_str
        self.comment = comment


    def set_normalisation(self, normalisation, normalise_which=None):
        if normalise_which is None:
            normalise_which = self.normalise_which

        if normalisation == "counts":
            for i, dataset in enumerate(self.raw):

                # Apply normalisation to specified datasets
                if dataset.detector in normalise_which:
                    self.data[i].y = normalise_counts(dataset.y)
                else:
                    self.data[i].y = self.raw[i].y

            # Update the normalisation status
            self.normalisation = normalisation
            self.normalise_which = normalise_which
            return 0

        if normalisation == "events":
            try:
                spills = int(self.events_str[19:])
                for i, dataset in enumerate(self.raw):

                    # Apply normalisation to specified datasets
                    if dataset.detector in normalise_which:
                        self.data[i].y = normalise_events(dataset.y, spills)
                    else:
                        self.data[i].y = self.raw[i].y

                # Update the normalisation status
                self.normalisation = normalisation
                self.normalise_which = normalise_which
                return 0

            except ValueError:
                # If spills data is not available, revert normalisation to none
                for i, dataset in enumerate(self.raw):
                    self.data[i].y = self.raw[i].y

                # set normalisation status to "none"
                self.normalisation = "none"
                self.normalise_which = self.loaded_detectors
                return 1

        elif normalisation == "none":
            for i, dataset in enumerate(self.raw):
                self.data[i].y = self.raw[i].y

            self.normalisation = normalisation
            self.normalise_which = self.loaded_detectors
            return 0

        else:
            raise KeyError # normalisation type specified in config doesn't exist

    def set_energy_correction(self, e_corr_params, e_corr_which=None):
        if e_corr_which is None:
            e_corr_which = self.e_corr_which

        # Iterate through each Dataset in the run and apply energy correction if the detector is in e_corr_which
        for i, dataset in enumerate(self.raw):
            detector = dataset.detector

            if detector in e_corr_which:
                gradient = e_corr_params[i][0]
                offset = e_corr_params[i][1]

                self.data[i].x = self.raw[i].x * gradient + offset # store energy correction in data

        self.e_corr_which = e_corr_which
        self.e_corr_params = e_corr_params

    def is_empty(self) -> bool:
        # Returns a boolean indicating whether any data was loaded or not
        return all([dataset.x.size == 0 for dataset in self.raw])

    def get_nonzero_data(self) -> list[Dataset]:
        # Returns only the loaded datasets (without empty arrays for missing detectors)
        return [dataset for dataset in self.data if dataset.x.size != 0]