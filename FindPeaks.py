from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt
import globals

def FindPeaks(h,t,d):
    print('here')
#    peaks = find_peaks(globals.y_GE1,height=10,threshold = 15, distance = 1)
    peaks = find_peaks(globals.y_GE1,height=h,threshold = t, distance = d)
    print(peaks)
    height = peaks[1]['peak_heights']
    print(height)
    peak_pos = globals.x_GE1[peaks[0]]
    print(peak_pos)
    figx = plt.figure()
    print('hello')
    axx = figx.subplots()
    print('ahh')
    axx.plot(globals.x_GE1,globals.y_GE1)
    print('hmmm')
    axx.scatter(peak_pos,height, color = 'r', s = 10, marker = 'X', label = 'peaks')
    #axx.legend()
    plt.show()
    return peaks,peak_pos