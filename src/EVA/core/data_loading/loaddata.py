import numpy as np
from EVA.core.data_loading import loadcomment
from EVA.core.data_structures.run import Run
from EVA.core.data_structures.spectrum import Spectrum

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
    Creates Spectra to store the data from each channel (detector).
    Calls loadcomment() to get run info and stores metadata and lists of Spectra (for each detector) in a Run object.
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
            # Store data read from file in a Spectrum object
            xdata, ydata = np.loadtxt(filename, delimiter=" ", unpack=True)
            spectrum = Spectrum(detector=detector, run_number=run_num, x=xdata, y=ydata)

            raw.append(spectrum) # Add Spectrum to list of spectra
            detectors.append(detector) # Add detector name to list of detectors

            none_loaded_flag = 0 # data was found - lowering flag

        except FileNotFoundError:
            # Append empty arrays to spectrum if data file is not found for the given detector.
            # This maintains a consistent detector order in the list
            raw.append(Spectrum(detector=detector, run_number=run_num, x=np.array([]), y=np.array([])))

    # Add everything into a Run object
    run = Run(raw=raw, loaded_detectors=detectors, run_num=str(run_num), start_time=comment_data[0],
              end_time=comment_data[1], events_str=comment_data[2], comment=comment_data[3])

    # Read which normalisation and energy correction to apply from config
    e_corr_which = []
    e_corr_params = []
    for detector in config.to_array(config["general"]["all_detectors"]):
        if config[detector]["use_e_corr"] == "yes":
            e_corr_which.append(detector)
            gradient = float(config[detector]["e_corr_gradient"])
            offset = float(config[detector]["e_corr_offset"])
            e_corr_params.append((gradient, offset))
        else:
            # default energy correction
            e_corr_params.append((1, 0))

    normalisation = config["general"]["normalisation"]
    normalise_which = config["general"]["all_detectors"] # currently normalising all detectors

    # Apply energy calibration
    run.set_energy_correction(e_corr_params, e_corr_which)

    # Apply normalisation and get normalisation status flag
    try:
        run.set_normalisation(normalisation, normalise_which)
        norm_flag = 0
    except ValueError:
        norm_flag = 1

    # Assemble flag dictionary to return error status
    flags = {
        "no_files_found": none_loaded_flag,
        "comment_not_found": comment_flag,
        "norm_by_spills_error": norm_flag
    }

    return run, flags
