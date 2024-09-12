import matplotlib.pyplot as plt
from EVA import Plot_Spectra
from EVA import globals


def MultiPlot(x1, y1, x2, y2, x3, y3, x4, y4, RunList, offset):
    """plots multiple runs from runlist and with a y-axis offset"""

    numplots= Plot_Spectra.How_many_plot()


    #gets around annoying matplotlib issue of inconsistent return of subplots
    if numplots > 1:
        #print('more than one plot')
        fig, axs = plt.subplots(nrows=numplots, figsize=(16, 7))

    else:
        #annoying matplotlib fix for one figure in a subplot
        print('only one plot')
        fig, temp = plt.subplots(nrows=1, figsize=(16, 7), squeeze=False)

        axs = [temp[0][0]]

    # labels figures
    fig.suptitle("MultiPlot")
    fig.supxlabel("Energy (keV)")

    # sets correct y-axis label
    if globals.Normalise_do_not:
        fig.supylabel("Intensity")
    elif globals.Normalise_counts:
        fig.supylabel("Intensity Normalised to Counts (10^5)")
    elif globals.Normalise_spill:
        fig.supylabel("Intensity Normalised to Spills (10^5)")

    # plots the runs for each detector
    i = 0
    if globals.plot_GE1:
        NoofRuns = len(x1)
        for j in range(NoofRuns):
            axs[i].step(x1[j], y1[j]+j*offset, where='mid', label = str(RunList[j]))
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('2099')
        axs[i].legend()
        i += 1
    if globals.plot_GE2:
        NoofRuns = len(x2)
        for j in range(NoofRuns):
            axs[i].step(x2[j],y2[j]+j*offset,where='mid', label=str(RunList[j]))
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('3099')
        axs[i].legend()
        i += 1
    if globals.plot_GE3:
        NoofRuns = len(x3)
        for j in range(NoofRuns):
           axs[i].step(x3[j],y3[j]+j*offset,where='mid', label=str(RunList[j]))
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('4099')
        axs[i].legend()
        i += 1
    if globals.plot_GE4:
        NoofRuns = len(x4)
        for j in range(NoofRuns):
            axs[i].step(x4[j],y4[j]+j*offset,where='mid', label=str(RunList[j]))
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('5099')
        axs[i].legend()
        i += 1

    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.45, wspace=0.23)
    return fig, axs

