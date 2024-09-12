import matplotlib.pyplot as plt
from EVA import globals

fill_color = "yellow"

def How_many_plot():
    """
    Determines how many plots in each plot

    """
    numplots = 0
    if globals.plot_GE1:
        numplots += 1
    if globals.plot_GE2:
        numplots += 1
    if globals.plot_GE3:
        numplots += 1
    if globals.plot_GE4:
        numplots += 1
    return numplots

def Plot_Peak_Location(fig,axs,plt,peaks,x,i):
    """
    Plots the location of the peaks
    """

    height = peaks[1]['peak_heights']
    peak_pos = x[peaks[0]]
    axs[i].scatter(peak_pos, height, color='r', s=20, marker='X', label='peaks')

def Plot_Spectra3(x1,y1,x2,y2,x3,y3,x4,y4,title_lab):
    #plots spectra as defined by the plot spectra
    numplots=How_many_plot()
    print('numplots', numplots)
    print(globals.Normalise_spill, globals.Normalise_counts)
    print(x1)

    if numplots > 1:
        #print('more than one plot')
        fig, axs = plt.subplots(nrows=numplots, figsize=(16,7))

    else:
        #annoying matplotlib fix for one figure in a subplot
        print('only one plot')
        fig, temp = plt.subplots(nrows=1, figsize=(16, 7), squeeze=False)

        axs = [temp[0][0]]

    fig.suptitle("Run Number: " + str(globals.RunNum) + "  " + globals.comment_str)
    fig.supxlabel("Energy (keV)")

    # sets the correct labels
    if globals.Normalise_do_not:
        fig.supylabel("Intensity")
    elif globals.Normalise_counts:
        fig.supylabel("Intensity Normalised to Counts (10^5)")
    elif globals.Normalise_spill:
        fig.supylabel("Intensity Normalised to Spills (10^5)")

    i = 0
    print('i=', i)
    if globals.plot_GE1:
        print('1', i)
        axs[i].fill_between(x1, y1, step='mid', color=fill_color)
        axs[i].step(x1, y1, where='mid', color='black')
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('2099')
        i += 1
        print('here plot GE1')

    if globals.plot_GE2:
        #print('2',i)
        axs[i].fill_between(x2, y2,step='mid',color=fill_color)
        axs[i].step(x2,y2,where='mid',color='black')
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('3099')
        i += 1
    if globals.plot_GE3:
        #print('3',i)
        axs[i].fill_between(x3, y3,step='mid',color=fill_color)
        axs[i].step(x3,y3,where='mid',color='black')
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('4099')
        i += 1

    if globals.plot_GE4:
        #print('4',i)
        axs[i].fill_between(x4, y4,step='mid',color=fill_color)
        axs[i].step(x4,y4,where='mid',color='black')
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('5099')
        i += 1

    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.45, wspace=0.23)
    #fig.tight_layout()
    return fig, axs

'''def Plot_Spectra2():
    numplots=How_many_plot()
    print('numplot', numplots)

    fig, axs = plt.subplots(numplots,figsize=(16,7))

    fig.suptitle("Run Number: " + str(globals.RunNum) + "  " + globals.comment_str)
    fig.supxlabel("Energy (keV)")
    fig.supylabel("Intensity")
    i=0
    
    if globals.plot_GE1:
        axs[i].fill_between(globals.x_GE1, globals.y_GE1,step='mid',color='yellow')
        axs[i].step(globals.x_GE1,globals.y_GE1,where='mid',color='black')
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('2099')
        i+=1
    if globals.plot_GE2:
        axs[i].fill_between(globals.x_GE2, globals.y_GE2,step='mid',color='yellow')
        axs[i].step(globals.x_GE2,globals.y_GE2,where='mid',color='black')
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('3099')
        i+=1
    if globals.plot_GE3:
        axs[i].fill_between(globals.x_GE3, globals.y_GE3,step='mid',color='yellow')
        axs[i].step(globals.x_GE3,globals.y_GE3,where='mid',color='black')
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('4099')
        i+=1
    if globals.plot_GE4:
        axs[i].fill_between(globals.x_GE4, globals.y_GE4,step='mid',color='yellow')
        axs[i].step(globals.x_GE4,globals.y_GE4,where='mid',color='black')
        axs[i].set_ylim(0.0)
        axs[i].set_xlim(0.0)
        axs[i].set_title('5099')
        i+=1

    plt.rc('font',size=16)
    plt.tight_layout()

    plt.show()




def Plot_Spectra(self,x,y):

    print('here')
    fig = plt.figure(figsize=(16, 7))
    print('1')

    plt.fill_between(x, y, step='mid', color='yellow')
    plt.step(x, y, where='mid', color='black')
    plt.ylim(bottom=0.0)
    plt.xlim(left=0.0)
    plt.xlabel("Energy")
    plt.ylabel("Intensity")
    plt.legend(str(globals.RunNum))
    plt.title("Run Number: " + str(globals.RunNum) + "  " + globals.comment_str)
    plt.rc('font', size=16)
    print('here2')

    plt.show()

    def on_click(event):
        if event.button is MouseButton.RIGHT:
            # print(globals.peak_data)
            print('disconnecting callback')
            # plt.disconnect(binding_id)

        if event.button is MouseButton.LEFT:
            x, y = event.x, event.y
            if event.inaxes:
                ax = event.inaxes  # the axes instance
                default_peaks = [event.x]
                default_sigma = [0.45] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                res = getmatch.get_matches(input_data)

                temp = res[0]
                i = 0
                print(len(res[0]))
                self.table_clickpeaks.setRowCount(len(res[0]))
                for match in temp:
                    row = [match['peak_centre'], match['energy'], match['element'],
                           match['transition'], match['error'], match['diff']]

                    self.table_clickpeaks.setItem(i, 0, QTableWidgetItem(row[2]))
                    self.table_clickpeaks.setItem(i, 1, QTableWidgetItem(row[3]))
                    i += 1

                self.table_clickpeaks.setRowCount(i)

                self.show()
                '''
