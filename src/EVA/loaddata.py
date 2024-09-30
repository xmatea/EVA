import numpy as np
from dataclasses import dataclass
from EVA import globals, Normalise, Energy_Corrections, loadcomment
from EVA.app import get_config

channels = {
    "GE1": "2099",
    "GE2": "3099",
    "GE3": "4099",
    "GE4": "5099"
}

@dataclass
class Dataset:
    """
    The Dataset class holds the data from a single detector and a single run.
    """
    x: np.ndarray
    y: np.ndarray
    detector: str


@dataclass
class Run:
    """
    The Run class holds lists of Datasets from all the detectors from a single run, as well as the run number,
    normalisation status and the comment from a single run.
    """
    raw: list[Dataset]  # List of data from each detector with no normalisation or energy calibration
    detectors: list[str]  # List of detectors present in run
    run_num: int
    start_time: int
    end_time: int
    events: int
    comment: str

    norm_none: list[Dataset] = None  # This holds a copy of the data with no normalisation
    norm_counts: list[Dataset] = None  # This holds a copy of the data normalised by counts
    norm_events: list[Dataset] = None  # This holds a copy of the data normalised by spill events

    data: list[Dataset] = None  # List of data from each detector with default calibration applied
    normalisation: str = "none"  # Which normalisation is applied in 'data'


def loaddata(run_num):
    config = get_config()
    working_directory = config.parser["general"]["working_directory"]

    # Load metadata from comment
    flag, comment_data = loadcomment.loadcomment(run_num)

    if flag:
        print("Failed to load comment")

    raw = []
    norm_none = []
    norm_counts = []
    norm_spill = []
    detectors = []

    for detector, channel in channels.items():
        filename = f"{working_directory}/ral0{run_num}.rooth{channel}.dat"

        try:
            xdata, ydata = np.loadtxt(filename, delimiter=" ", unpack=True)
            dataset = Dataset(xdata, ydata, detector)
            raw.append(dataset)
            detectors.append(detector)

        except FileNotFoundError:
            print(f'{channel} file not found')

    # Return now if no data was found
    if len(detectors) == 0:
        return 1, None

    # Add everything into a Run object
    run = Run(raw, detectors, run_num, start_time=comment_data[0], end_time=comment_data[1], events=comment_data[2],
              comment=comment_data[3])

    # Apply energy calibration and normalise
    print('Going to Energy correction')
    run.norm_none = Energy_Corrections.Energy_Corrections(run.raw)

    print('Going to Efficiency corrections')
    run.norm_counts = Normalise.normalise_counts(run.norm_none)

    run.norm_events = Normalise.normalise_events(run.norm_none)

    # Set run.data equal to default calibration
    if config.parser["normalisation"]["counts"]:
        run.normalisation = "counts"
        run.data = run.norm_counts
    elif config.parser["normalisation"]["events"]:
        run.normalisation = "events"
        run.data = run.norm_events
    else:
        run.normalisation = "none"
        run.data = run.norm_none

    return 0, run
    # Load data and store in globals
