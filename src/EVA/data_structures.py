from dataclasses import dataclass
import numpy as np

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

@dataclass
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
    raw: list[Dataset]
    loaded_detectors: list[str]
    run_num: str
    start_time: str
    end_time: str
    events_str: str
    comment: str

    raw_e_corr: list[Dataset] = None
    data: list[Dataset] = None

    def is_empty(self) -> bool:
        # Returns a boolean indicating whether any data was loaded or not
        return all(dataset.x.size == 0 for dataset in self.raw)

    def get_nonzero_data(self) -> list[Dataset]:
        # Returns only the loaded datasets (without empty arrays for missing detectors)
        return [dataset for dataset in self.data if dataset.x.size != 0]