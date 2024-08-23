from scipy.signal import find_peaks
from scipy.signal import find_peaks_cwt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import globals

def meanfilter(data, filter_size=9):
    '''
    Smooths out the data using a mean filter.
    '''
    return np.convolve(data, np.ones(filter_size)/filter_size, mode='same')


def Findpeak_with_bck_removed(x,y):
    print('here in Keiths peak finder')

    spectrum = y

    FSIZE = 20
    NFILTER = 9
    HIGH_CLIP = 25
    PEAK_THRESH = 10

    ## Create smooth backgroud
    rough_base = meanfilter(spectrum, FSIZE)
    for i in range(NFILTER):
        rough_base = meanfilter(rough_base, FSIZE)

    ## Subtract from main signal result smooth1
    smooth1 = spectrum - rough_base

    ## Look for points in smooth1 more than MAX_HEIGHT -> convert to NaN
    cond_high_clip = (smooth1 > HIGH_CLIP)
    clipped = np.where(cond_high_clip, np.nan, spectrum)

    ## Interpolate between dropped points
    interpd = pd.Series(clipped).interpolate().tolist()

    ## Get baseline from the interpd signal
    rough_base = meanfilter(interpd, FSIZE // 2)
    for i in range(NFILTER):
        rough_base = meanfilter(interpd, FSIZE // 2)

    ## Subract rough_base from spectrum to get a backgroud removed signal
    bg_removed = meanfilter(spectrum - rough_base, FSIZE // 10)

    ## Pick peaks on bg removed signal
    peaks = find_peaks(bg_removed, height=PEAK_THRESH)
    print('pos',peaks)
    #print('params',params)
    '''strong_pos, params = find_peaks(bg_removed, height=10)
    peaks = np.zeros(shape=len(spectrum))
    peaks[pos] = 30
    strong_peaks = np.zeros(shape=len(spectrum))
    strong_peaks[strong_pos] = 50'''
    #height = peaks[1]['peak_heights']
    height = y[peaks[0]]
    print(height)
    print(len(height))
    peak_pos = x[peaks[0]]

    print(peak_pos)
    print(len(peak_pos))
    figx = plt.figure()
    print('hello')
    axx = figx.subplots()
    print('ahh')
    axx.plot(x, y)
    print('hmmm')
    axx.scatter(peak_pos, height, color='r', s=40, marker='X', label='peaks')
    print('scatter')
    #plt.show()
    print('returning')
    return peaks, peak_pos

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
    #plt.show()
    print('returning')
    return peaks, peak_pos

def FindPeaksCwt(x,y,h,t,d):
    print('here in Findpeakscwt')
    #peaks = find_peaks(y,height=h,threshold = t, distance = d)
    peaks = find_peaks_cwt(y,[h])
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
    #plt.show()
    print('returning')
    return [peaks], [peak_pos]