import globals
import numpy as np

def Normalise():
    print('in normalise ', globals.Normalise_counts)
    if globals.Normalise_counts:
        #print('hello')
        globals.x_GE1_Ncounts = globals.x_GE1
        globals.y_GE1_Ncounts = globals.y_GE1/np.sum(globals.y_GE1)*pow(10,5)
        #err_GE1_Ncounts = arr.array('i', [])
        globals.x_GE2_Ncounts = globals.x_GE2
        globals.y_GE2_Ncounts = globals.y_GE2/np.sum(globals.y_GE2)*pow(10,5)
        #err_GE2_Ncounts = arr.array('i', [])
        globals.x_GE3_Ncounts = globals.x_GE3
        globals.y_GE3_Ncounts = globals.y_GE3/np.sum(globals.y_GE3)*pow(10,5)
        #err_GE3_Ncounts = arr.array('i', [])
        globals.x_GE4_Ncounts = globals.x_GE4
        globals.y_GE4_Ncounts = globals.y_GE4/np.sum(globals.y_GE4)*pow(10,5)
        #err_GE4_Ncounts = arr.array('i', [])
        print('bye')

    if globals.Normalise_spill:
        #print('in spills')
        #print(globals.events_str[19:])
        Spills = int(globals.events_str[19:])
        #print(Spills)
        globals.x_GE1_NEvents= globals.x_GE1
        globals.y_GE1_NEvents = globals.y_GE1/Spills*pow(10,5)
        #err_GE1_Ncounts = arr.array('i', [])
        globals.x_GE2_NEvents = globals.x_GE2
        globals.y_GE2_NEvents = globals.y_GE2/Spills*pow(10,5)
        #err_GE2_Ncounts = arr.array('i', [])
        globals.x_GE3_NEvents = globals.x_GE3
        globals.y_GE3_NEvents = globals.y_GE3/Spills*pow(10,5)
        #err_GE3_Ncounts = arr.array('i', [])
        globals.x_GE4_NEvents = globals.x_GE4
        globals.y_GE4_NEvents = globals.y_GE4/Spills*pow(10,5)
        #err_GE4_Ncounts = arr.array('i', [])
        #print('bye')

