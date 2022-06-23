import matplotlib.pyplot as plt
import Plot_Spectra
import globals

def MultiPlot(x1,y1,x2,y2,x3,y3,x4,y4, RunList, offset):

    numplots=Plot_Spectra.How_many_plot()
    #print('numplot', numplots, offset)
    #print(globals.Normalise_spill,globals.Normalise_counts)

    if numplots > 1:
        fig, axs = plt.subplots(nrows=numplots, ncols=1, figsize=(16,7))
    else:
        fig, temp = plt.subplots(nrows=numplots, ncols=1, figsize=(16, 7), squeeze=False)
        axs = [temp[0][0]]

    fig.suptitle("MultiPlot")
    fig.supxlabel("Energy (keV)")
    if globals.Normalise_do_not:
        fig.supylabel("Intensity")
    elif globals.Normalise_counts:
        fig.supylabel("Intensity Normalised to Counts (10^5)")
    elif globals.Normalise_spill:
        fig.supylabel("Intensity Normalised to Spills (10^5)")
    i = 0
    if globals.plot_GE1:
        #axs[i].fill_between(x1, y1,step='mid',color='yellow')
        NoofRuns = len(x1)
        #print('NoofRuns', NoofRuns)
        #print('x1', x1[0])
        for j in range(NoofRuns):
            axs[i].step(x1[j], y1[j]+j*offset, where='mid', label = str(RunList[j]))
            print('j', j)
            #axs[i].plot(x1[j],y1[j])
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
        #print('NoofRuns', NoofRuns)
        #print('x1', x1[0])
        for j in range(NoofRuns):
           axs[i].step(x3[j],y3[j]+j*offset,where='mid', label=str(RunList[j]))
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('4099')
        axs[i].legend()
        i += 1
    if globals.plot_GE4:
        NoofRuns = len(x4)
        #print('NoofRuns', NoofRuns)
        #print('x1', x1[0])
        for j in range(NoofRuns):
            axs[i].step(x4[j],y4[j]+j*offset,where='mid', label=str(RunList[j]))
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('5099')
        axs[i].legend()
        i += 1

    plt.rc('font',size=16)
    plt.tight_layout()

    plt.show()

    return fig, axs, plt

