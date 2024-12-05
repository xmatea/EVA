import numpy as np

# Normalisation by 100000 counts
def normalise_counts(ydata):
    return ydata / np.sum(ydata) * pow(10, 5)

# Normalisation by events - returns data unchanged and raises flag if data events comment is empty
def normalise_events(ydata, spills):
    return ydata / spills * pow(10, 5)