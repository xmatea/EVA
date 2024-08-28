#import array as arr
import globals
import numpy as np
import Normalise
import Energy_Corrections

def loaddata(RunNum):
    #print('loading data ', RunNum)
    #print('Working dir', globals.workingdirectory)
    flag = 1
    filename_det = [globals.workingdirectory + '/ral0' + str(RunNum) + '.rooth2099.dat',
                        globals.workingdirectory + '/ral0' + str(RunNum) + '.rooth3099.dat',
                        globals.workingdirectory + '/ral0' + str(RunNum) + '.rooth4099.dat',
                        globals.workingdirectory + '/ral0' + str(RunNum) + '.rooth5099.dat']
    #print(filename_det)
    #print(filename_det[0])

    try:
        globals.dataset_GE1 = np.loadtxt(filename_det[0], delimiter=" ")
        globals.x_GE1, globals.y_GE1 = np.loadtxt(filename_det[0], delimiter=" ", unpack=True)
        globals.flag_d_GE1 = 1

    except IOError:
        globals.flag_d_GE1 = 0
        print('2099 file not found')

    try:
        globals.dataset_GE2 = np.loadtxt(filename_det[1], delimiter=" ")
        globals.x_GE2, globals.y_GE2 = np.loadtxt(filename_det[1], delimiter=" ", unpack=True)
        #print(globals.x_GE2[100],' ',globals.y_GE2[100])
        globals.flag_d_GE2 = 1
    except IOError:
        globals.flag_d_GE2 = 0
        print('3099 file not found')

    try:
        globals.dataset_GE3 = np.loadtxt(filename_det[2], delimiter=" ")
        globals.x_GE3, globals.y_GE3 = np.loadtxt(filename_det[2], delimiter=" ", unpack=True)
        #print(globals.x_GE3[100],' ',globals.y_GE3[100])
        globals.flag_d_GE3 = 1
    except IOError:
        globals.flag_d_GE3 = 0
        print('4099 file not found')

    try:
        globals.dataset_GE4 = np.loadtxt(filename_det[3], delimiter=" ")
        globals.x_GE4, globals.y_GE4 = np.loadtxt(filename_det[3], delimiter=" ", unpack=True)
        #print(globals.x_GE4[100],' ',globals.y_GE4[100])
        globals.flag_d_GE1 = 1

        globals.flag_d_GE4 = 1
    except IOError:
        globals.flag_d_GE4 = 0
        print('5099 file not found')


    print('Going to Energy correction')

    Energy_Corrections.Energy_Corrections()

    print('going to Normalise')

    Normalise.Normalise()


    print('Going to Efficiency corrections')

    return flag

    #

    # Load data and store in globals
