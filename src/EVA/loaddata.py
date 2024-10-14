import numpy as np
from EVA import Normalise, Energy_Corrections, loadcomment
from EVA.app import get_config
from EVA.data_structures import Dataset, Run

channels = {
    "GE1": "2099",
    "GE2": "3099",
    "GE3": "4099",
    "GE4": "5099"
}

def load_run(run_num):
    """
    Loads the specified run by searching for the run in the working directory.
    Creates Datasets to store the data from each channel (detector).
    Calls loadcomment() to get run info and stores metadata and lists of Datasets (for each detector) in a Run object.
    Calls normalise() and energy_correction() to normalise the data and stores the normalised data under run.data.
    Returns the loaded Run object and error flags.
    """
    config = get_config()
    working_directory = config["general"]["working_directory"]

    # Load metadata from comment
    comment_data, comment_flag = loadcomment.loadcomment(run_num)

    raw = []
    detectors = []

    none_loaded_flag = 1

    for detector, channel in channels.items():
        filename = f"{working_directory}/ral0{run_num}.rooth{channel}.dat"
        print("searching for", filename)
        try:
            xdata, ydata = np.loadtxt(filename, delimiter=" ", unpack=True)
            dataset = Dataset(detector=detector, run_number=run_num, x=xdata, y=ydata)
            raw.append(dataset)
            detectors.append(detectors)
            none_loaded_flag = 0

        except FileNotFoundError:
            print(f'{channel} file not found')
            # Append empty arrays to dataset if data file is not found for the given detector
            raw.append(Dataset(detector=detector, run_number=run_num, x=np.array([]), y=np.array([])))

    if none_loaded_flag:
        return [1], None # Return None now if all data failed to load

    # Add everything into a Run object
    run = Run(raw, loaded_detectors=detectors, run_num=run_num, start_time=comment_data[0], end_time=comment_data[1],
              events_str=comment_data[2], comment=comment_data[3])

    # Apply energy calibration and normalise
    print('Going to Energy correction')
    run.raw_e_corr = Energy_Corrections.Energy_Corrections(run.raw)

    # Apply normalisation
    print('Going to Normalisation')
    norm_data, norm_flag = Normalise.normalise(run.raw_e_corr, run.events_str, config["general"]["normalisation"])
    run.data = norm_data

    return [none_loaded_flag, comment_flag, norm_flag], run
