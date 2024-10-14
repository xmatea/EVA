import numpy as np
from EVA.data_structures import Dataset

def normalise(data, events, normalisation):
    # checks which normalisation is set in config
    if normalisation == "counts":
        data, norm_flag = normalise_counts(data)
    elif normalisation == "events":
        data, norm_flag = normalise_events(data, events)
    else:
        norm_flag = 0 # do nothing if normalisation is not needed

    return data, norm_flag

def normalise_counts(data):
    for dataset in data:
        dataset.y = dataset.y / np.sum(dataset.y) * pow(10, 5)

    return data, 0

def normalise_events(data, events_str):
    if events_str == " ": # default value of events_str if the comment is not loaded
        return data, 1

    spills = int(events_str[19:])

    for dataset in data:
        dataset.y = dataset.y / spills * pow(10, 5)

    return data, 0