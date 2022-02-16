import globals
import numpy as np


# global dataset_GE1, dataset_GE2, dataset_GE3, dataset_GE4


def loaddata(RunNum):
    print('loading data ', RunNum)
    print('Working dir', globals.workingdirectory)
    flag = 0
    try:
        filename_det = [globals.workingdirectory + '/ral0' + str(RunNum) + '.rooth2099.dat',
                        globals.workingdirectory + '/ral0' + str(RunNum) + '.rooth3099.dat',
                        globals.workingdirectory + '/ral0' + str(RunNum) + '.rooth4099.dat',
                        globals.workingdirectory + '/ral0' + str(RunNum) + '.rooth5099.dat']
        print(filename_det)
        print(filename_det[0])

        dataset_GE1 = np.loadtxt(filename_det[0], delimiter=" ")
#        data[0, :, :] = dataset_GE1
#        dataset_GE2 = np.loadtxt(filename_det[1], delimiter=" ")
#        dataset_GE3 = np.loadtxt(filename_det[2], delimiter=" ")
#        dataset_GE4 = np.loadtxt(filename_det[3], delimiter=" ")
        print(dataset_GE1)
    except IOError:
        flag = 1
        print('file not found')
    return flag

    #

    # Load data and store in globals
