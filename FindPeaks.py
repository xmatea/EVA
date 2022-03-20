from scipy.signal import find_peaks
from scipy.signal import find_peaks_cwt

import numpy as np
import matplotlib.pyplot as plt
import globals

def FindPeaks(x,y,h,t,d):
    print('here in Findpeaks')
    peaks = find_peaks(y,height=h,threshold = t, distance = d)
    print(peaks)
    height = peaks[1]['peak_heights']
    print(height)
    print(len(height))
    peak_pos = x[peaks[0]]

    print(peak_pos)
    print(len(peak_pos))
    figx = plt.figure()
    print('hello')
    axx = figx.subplots()
    print('ahh')
    axx.plot(x,y)
    print('hmmm')
    axx.scatter(peak_pos,height, color = 'r', s = 40, marker = 'X', label = 'peaks')
    print('scatter')
    plt.show()
    print('returning')
    return peaks, peak_pos

def FindPeaksCwt(x,y,h,t,d):
    print('here in Findpeaks')
    #peaks = find_peaks(y,height=h,threshold = t, distance = d)
    peaks = find_peaks_cwt(y,[5])
    print(peaks)
    #height = peaks[1]['peak_heights']
    height = y[peaks]
    print(height)
    print(len(height))
    #peak_pos = x[peaks[0]]
    peak_pos = x[peaks]

    print(peak_pos)
    print(len(peak_pos))
    figx = plt.figure()
    print('hello')
    axx = figx.subplots()
    print('ahh')
    axx.plot(x,y)
    print('hmmm')
    axx.scatter(peak_pos,height, color = 'r', s = 40, marker = 'X', label = 'peaks')
    print('scatter')
    plt.show()
    print('returning')
    return peaks, peak_pos
