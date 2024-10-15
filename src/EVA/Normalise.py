import numpy as np
from EVA.data_structures import Dataset
from EVA.app import get_config

# Apply normalisation and update config if necessary
def normalise(normalisation, data, events=None):
    config = get_config()

    # checks which normalisation is set in config and applies accordingly
    if normalisation == "counts":
        data, norm_flag = normalise_counts(data)

        # only update config if normalisation was successful
        if not norm_flag:
            config["general"]["normalisation"] = "counts"
        else:
            config["general"]["normalisation"] = "none"

    elif normalisation == "events":
        data, norm_flag = normalise_events(data, events)

        # only update config if normalisation was successful
        if not norm_flag:
            config["general"]["normalisation"] = "events"
        else:
            config["general"]["normalisation"] = "none"

    else:
        norm_flag = 0 # do nothing if normalisation is not needed
        config["general"]["normalisation"] = "none"

    return data, norm_flag

# Normalisation by 100000 counts
def normalise_counts(data):
    for dataset in data:
        dataset.y = dataset.y / np.sum(dataset.y) * pow(10, 5)

    return data, 0

# Normalisation by events - returns data unchanged and raises flag if data events comment is empty
def normalise_events(data, events_str):
    if events_str == " ": # default value of events_str if the comment is not loaded
        return data, 1

    spills = int(events_str[19:])

    for dataset in data:
        dataset.y = dataset.y / spills * pow(10, 5)

    return data, 0