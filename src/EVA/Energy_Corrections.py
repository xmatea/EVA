from EVA.app import get_config
from EVA.loaddata import Dataset

def Energy_Corrections(data):
    config = get_config()

    corrected = []
    # For each dataset in the list, return energy corrected data if energy correction is wanted
    for dataset in data:
        detector = dataset.detector
        if config.parser[detector]["use_energy_correction"]:
            gradient = config.parser[detector]["e_corr_gradient"]
            offset = config.parser[detector]["e_corr_offset"]
            xdata = lincorr(dataset.x, gradient, offset)
        else:
            xdata = dataset.x

        # Create new datasets
        corrected.append(Dataset(xdata, dataset.y, detector))

    return corrected


def lincorr(x, m, c):
    new_x = x*float(m)+float(c)

    return new_x
