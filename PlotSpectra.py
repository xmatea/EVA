import matplotlib as plt

def Plot_Spectra(x,y):
    plt.figure(figsize=(16, 7))

    plt.fill_between(x, y, step='mid', color='yellow')
    plt.step(x, y, where='mid', color='black')
    plt.ylim(bottom=0.0)
    plt.xlim(left=0.0)
    plt.xlabel("Energy")
    plt.ylabel("Intensity")
    plt.legend(str(globals.RunNum))
    plt.title("Run Number: " + str(globals.RunNum) + "  " + globals.comment_str)
    plt.rc('font', size=16)

    plt.show()