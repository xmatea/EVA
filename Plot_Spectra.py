import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import globals

def How_many_plot():
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



def Plot_Spectra2():
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
