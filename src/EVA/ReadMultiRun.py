from EVA import globals, loaddata, Normalise

def ReadMultiRun(RunList):

    #print('in ReadMultiRun')
    # keep current loaddata safe
    if globals.Normalise_do_not:
        try:
            tempx_GE1 = globals.x_GE1
            tempy_GE1 = globals.y_GE1
            tempx_GE2 = globals.x_GE2
            tempy_GE2 = globals.y_GE2
            tempx_GE3 = globals.x_GE3
            tempy_GE3 = globals.y_GE3
            tempx_GE4 = globals.x_GE4
            tempy_GE4 = globals.y_GE4
        except:
            print('Ooops')
    elif globals.Normalise_counts:
        try:
            tempx_GE1 = globals.x_GE1_Ncounts
            tempy_GE1 = globals.y_GE1_Ncounts
            tempx_GE2 = globals.x_GE2_Ncounts
            tempy_GE2 = globals.y_GE2_Ncounts
            tempx_GE3 = globals.x_GE3_Ncounts
            tempy_GE3 = globals.y_GE3_Ncounts
            tempx_GE4 = globals.x_GE4_Ncounts
            tempy_GE4 = globals.y_GE4_Ncounts
        except:
            print('Ooops')
    elif globals.Normalise_spill:
        try:
            tempx_GE1 = globals.x_GE1_NEvents
            tempy_GE1 = globals.y_GE1_NEvents
            tempx_GE2 = globals.x_GE2_NEvents
            tempy_GE2 = globals.y_GE2_NEvents
            tempx_GE3 = globals.x_GE3_NEvents
            tempy_GE3 = globals.y_GE3_NEvents
            tempx_GE4 = globals.x_GE4_NEvents
            tempy_GE4 = globals.y_GE4_NEvents
        except:
            print('Ooops')

    # load data
    datax_GE1 = []
    datay_GE1 = []
    datax_GE2 = []
    datay_GE2 = []
    datax_GE3 = []
    datay_GE3 = []
    datax_GE4 = []
    datay_GE4 = []

    lenRunList = len(RunList)

    for i in range(lenRunList):
        #print('i',RunList[i])
        loaddata.loaddata(RunList[i])
        Normalise.Normalise()
        if globals.Normalise_do_not:
            try:
                datax_GE1.append(globals.x_GE1)
                datay_GE1.append(globals.y_GE1)
                datax_GE2.append(globals.x_GE2)
                datay_GE2.append(globals.y_GE2)
                datax_GE3.append(globals.x_GE3)
                datay_GE3.append(globals.y_GE3)
                datax_GE4.append(globals.x_GE4)
                datay_GE4.append(globals.y_GE4)
            except:
                print('Ooops')
        elif globals.Normalise_counts:
            try:
                datax_GE1.append(globals.x_GE1_Ncounts)
                datay_GE1.append(globals.y_GE1_Ncounts)
                datax_GE2.append(globals.x_GE2_Ncounts)
                datay_GE2.append(globals.y_GE2_Ncounts)
                datax_GE3.append(globals.x_GE3_Ncounts)
                datay_GE3.append(globals.y_GE3_Ncounts)
                datax_GE4.append(globals.x_GE4_Ncounts)
                datay_GE4.append(globals.y_GE4_Ncounts)

            except:
                print('Ooops')
        elif globals.Normalise_spill:
            try:
                datax_GE1.append(globals.x_GE1_NEvents)
                datay_GE1.append(globals.y_GE1_NEvents)
                datax_GE2.append(globals.x_GE2_NEvents)
                datay_GE2.append(globals.y_GE2_NEvents)
                datax_GE3.append(globals.x_GE3_NEvents)
                datay_GE3.append(globals.y_GE3_NEvents)
                datax_GE4.append(globals.x_GE4_NEvents)
                datay_GE4.append(globals.y_GE4_NEvents)
            except:
                print('Ooops')

    if globals.Normalise_do_not:
        try:
            globals.x_GE1 = tempx_GE1
            globals.y_GE1 = tempy_GE1
            globals.x_GE2 = tempx_GE2
            globals.y_GE2 = tempy_GE2
            globals.x_GE3 = tempx_GE3
            globals.y_GE3 = tempy_GE3
            globals.x_GE4 = tempx_GE4
            globals.y_GE4 = tempy_GE4
        except:
            print('Ooops')
    elif globals.Normalise_counts:
        try:
            globals.x_GE1_Ncounts = tempx_GE1
            globals.y_GE1_Ncounts = tempy_GE1
            globals.x_GE2_Ncounts = tempx_GE2
            globals.y_GE2_Ncounts = tempy_GE2
            globals.x_GE3_Ncounts = tempx_GE3
            globals.y_GE3_Ncounts = tempy_GE3
            globals.x_GE4_Ncounts = tempx_GE4
            globals.y_GE4_Ncounts = tempy_GE4
        except:
            print('Ooops')
    elif globals.Normalise_spill:
        try:
            globals.x_GE1_NEvents = tempx_GE1
            globals.y_GE1_NEvents = tempy_GE1
            globals.x_GE2_NEvents = tempx_GE2
            globals.y_GE2_NEvents = tempy_GE2
            globals.x_GE3_NEvents = tempx_GE3
            globals.y_GE3_NEvents = tempy_GE3
            globals.x_GE4_NEvents = tempx_GE4
            globals.y_GE4_NEvents = tempy_GE4
        except:
            print('Ooops')


    return datax_GE1, datay_GE1, datax_GE2, datay_GE2, datax_GE3, datay_GE3, datax_GE4, datay_GE4


