import numpy as np

def Trimdata(x,y,EMin,EMax):
    #Trim data for fitting
    resmin = np.where(x > EMin)[0]
    resmax = np.where(x > EMax)[0]
    print('res', resmin[0], resmax[0])
    datax = x[resmin[0]:resmax[0]]
    datay = y[resmin[0]:resmax[0]]

    return datax, datay
