import numpy as np


def normalise_counts(data):
    normalised = []
    for dataset in data:

    return dataset.y / np.sum(dataset.y) * pow(10, 5)


def normalise_spill(dataset, events_str):
    spills = int(events_str[19:])
    return dataset.y / spills * pow(10, 5)
