import matplotlib.pyplot as plt
from EVA.core.app import get_app

def Plot_Peak_Location(axs,peaks,x,i):
    """
    Plots the location of the peaks
    """
    height = peaks[1]['peak_heights']
    peak_pos = x[peaks[0]]
    axs[i].scatter(peak_pos, height, color='r', s=20, marker='X', label='peaks')

def plot_spectrum(spectrum, normalisation, **settings):
    title = settings.get("title", f"Run Number: {spectrum.run_number} {spectrum.detector}")
    colour = settings.get("colour", "yellow")

    fig, ax = plt.subplots(1)
    fig.suptitle(title)
    fig.supxlabel("Energy (keV)")

    # sets the correct labels
    if normalisation == "counts":
        fig.supylabel("Intensity Normalised to Counts (10^5)")
    elif normalisation == "events":
        fig.supylabel("Intensity Normalised to Spills (10^5)")
    else:
        fig.supylabel("Intensity")

    ax.fill_between(spectrum.x, spectrum.y, step='mid', color=colour)
    ax.step(spectrum.x, spectrum.y, where='mid', color='black')
    ax.set_ylim(0.0)
    ax.set_xlim(0.0)

    return fig, ax

def plot_run(run, **settings):
    default_adjustments = {
        "top": 0.9,
        "bottom": 0.1,
        "left": 0.1,
        "right": 0.9,
        "hspace": 0.45,
        "wspace": 0.23
    }

    show_detectors = settings.get("show_detectors", run.loaded_detectors)
    title = settings.get("title", f"Run Number: {run.run_num} {run.comment}")
    colour = settings.get("colour", "yellow")
    size = settings.get("size", (16, 7))
    adjustments = settings.get("adjustment_dict", default_adjustments)

    num_plots = len(show_detectors)

    fig, axs = plt.subplots(nrows=num_plots, figsize=size)

    # hack to loop through all axes even if number of subplots == 1
    if num_plots == 1:
        axs = [axs]

    fig.suptitle(title)
    fig.supxlabel("Energy (keV)")

    # sets the correct labels
    if run.normalisation == "counts":
        fig.supylabel("Intensity Normalised to Counts (10^5)")
    elif run.normalisation == "events":
        fig.supylabel("Intensity Normalised to Spills (10^5)")
    else:
        fig.supylabel("Intensity")

    i = 0
    for dataset in run.data:
        if dataset.detector in show_detectors:
            axs[i].fill_between(dataset.x, dataset.y, step='mid', color=colour)
            axs[i].step(dataset.x, dataset.y, where='mid', color='black')
            axs[i].set_ylim(0.0)
            axs[i].set_xlim(0.0)
            axs[i].set_title(dataset.detector)
            i += 1

    # Adjustments
    plt.subplots_adjust(**adjustments)
    return fig, axs