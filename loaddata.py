import array as arr

import globals
import numpy as np


def loaddata(RunNum):
    print('loading data ', RunNum)
    print('Working dir', globals.workingdirectory)
    flag = 1
    filename_det = [globals.workingdirectory + '/ral0' + str(RunNum) + '.rooth2099.dat',
                        globals.workingdirectory + '/ral0' + str(RunNum) + '.rooth3099.dat',
                        globals.workingdirectory + '/ral0' + str(RunNum) + '.rooth4099.dat',
                        globals.workingdirectory + '/ral0' + str(RunNum) + '.rooth5099.dat']
    print(filename_det)
    print(filename_det[0])

    try:
        globals.dataset_GE1 = np.loadtxt(filename_det[0], delimiter=" ")
        print('here1')

        print('here2')
        globals.x_GE1, globals.y_GE1 = np.loadtxt(filename_det[0], delimiter=" ", unpack=True)
        print('here3')
        print(globals.x_GE1)
        globals.flag_d_GE1 = 1
        print('here4')
        print(globals.y_GE1)

    except IOError:
        globals.flag_d_GE1 = 0
        print('2099 file not found')

    try:
        globals.dataset_GE2 = np.loadtxt(filename_det[1], delimiter=" ")
        globals.flag_d_GE2 = 1
    except IOError:
        globals.flag_d_GE2 = 0
        print('3099 file not found')

    try:
        globals.dataset_GE3 = np.loadtxt(filename_det[2], delimiter=" ")
        globals.flag_d_GE3 = 1
    except IOError:
        globals.flag_d_GE3 = 0
        print('4099 file not found')

    try:
        globals.dataset_GE4 = np.loadtxt(filename_det[3], delimiter=" ")
        globals.flag_d_GE4 = 1
    except IOError:
        globals.flag_d_GE4 = 0
        print('5099 file not found')

    return flag

    #

    # Load data and store in globals
