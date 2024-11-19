import numpy as np
from EVA.classes.loaders import loadcomment
from EVA.classes.data_structures import Dataset, Run

channels = {
    "GE1": "2099",
    "GE2": "3099",
    "GE3": "4099",
    "GE4": "5099",
    "GE5": "",
    "GE6": "",
    "GE7": "",
    "GE8": "",
}

def load_run(run_num, config):
    """
    Loads the specified run by searching for the run in the working directory.
    Creates Datasets to store the data from each channel (detector).
    Calls loadcomment() to get run info and stores metadata and lists of Datasets (for each detector) in a Run object.
    Calls normalise() and energy_correction() to normalise the data and stores the normalised data under run.data.
    Returns the loaded Run object and error flags.
    """
    working_directory = config["general"]["working_directory"]

    # Load metadata from comment
    comment_data, comment_flag = loadcomment.loadcomment(run_num, working_directory)

    raw = []
    detectors = []

    none_loaded_flag = 1

    for detector, channel in channels.items():
        filename = f"{working_directory}/ral0{run_num}.rooth{channel}.dat"
        try:
            # Store data read from file in a Dataset object
            xdata, ydata = np.loadtxt(filename, delimiter=" ", unpack=True)
            dataset = Dataset(detector=detector, run_number=run_num, x=xdata, y=ydata)

            raw.append(dataset) # Add Dataset to list of datasets
            detectors.append(detectors) # Add detector name to list of detectors

            none_loaded_flag = 0 # data was found - lowering flag
            print(f'{detector} file found')

        except FileNotFoundError:
            print(f'{detector} file not found')

            # Append empty arrays to dataset if data file is not found for the given detector.
            # This maintains a consistent detector order in the list
            raw.append(Dataset(detector=detector, run_number=run_num, x=np.array([]), y=np.array([])))

    # Add everything into a Run object
    run = Run(raw=raw, loaded_detectors=detectors, run_num=str(run_num), start_time=comment_data[0],
              end_time=comment_data[1], events_str=comment_data[2], comment=comment_data[3])

    # Read which normalisation and energy correction to apply from config
    e_corr_which = []
    e_corr_params = []
    for detector in config.to_array(config["general"]["all_detectors"]):
        if config[detector]["use_e_corr"] == "yes":
            e_corr_which.append(detector)
            gradient = config[detector]["e_corr_gradient"]
            offset = config[detector]["e_corr_offset"]
            e_corr_params.append((gradient, offset))

    normalisation = config["general"]["normalisation"]
    normalise_which = config["general"]["all_detectors"] # currently normalising all detectors

    # Apply energy calibration
    run.set_energy_correction(e_corr_params, e_corr_which)

    # Apply normalisation and get normalisation status flag
    norm_flag = run.set_normalisation(normalisation, normalise_which)

    # Assemble flag dictionary to return error status
    flags = {
        "no_files_found": none_loaded_flag,
        "comment_not_found": comment_flag,
        "norm_by_spills_error": norm_flag
    }

    return run, flags
