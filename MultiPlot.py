import matplotlib.pyplot as plt
import Plot_Spectra
import globals

def MultiPlot(x1,y1,x2,y2,x3,y3,x4,y4):

    numplots=Plot_Spectra.How_many_plot()
    print('numplot', numplots)
    print(globals.Normalise_spill,globals.Normalise_counts)

    if numplots > 1:
        fig, axs = plt.subplots(nrows=numplots, ncols=1,figsize=(16,7))
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
    i=0
    if globals.plot_GE1:
        #axs[i].fill_between(x1, y1,step='mid',color='yellow')
        NoofRuns = len(x1)
        print('NoofRuns', NoofRuns)
        print('x1', x1[0])
        for j in range(NoofRuns):
            # Error here! need to be able to add multiple plots on same graph.. dinner time now :)
            axs[i].step(x1[j],y1[j],where='mid')
            print('j', j)
            #axs[i].plot(x1[j],y1[j])
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('2099')
        axs[i].legend()
        i+=1
    if globals.plot_GE2:
        axs[i].fill_between(x2, y2,step='mid',color='yellow')
        axs[i].step(x2[0],y2[0],where='mid',color='black')
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('3099')
        i+=1
    if globals.plot_GE3:
        axs[i].fill_between(x3[0], y3[0],step='mid',color='yellow')
        axs[i].step(x3,y3,where='mid',color='black')
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('4099')
        i+=1
    if globals.plot_GE4:
        axs[i].fill_between(x4[0], y4[0],step='mid',color='yellow')
        axs[i].step(x4,y4,where='mid',color='black')
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('5099')
        i+=1

    plt.rc('font',size=16)
    plt.tight_layout()

    plt.show()

    return fig, axs, plt

