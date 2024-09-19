import unittest
from EVA import globals, LoadDatabaseFile as ldf

'''from Tests import Test_LoadJason
from Tests import Test_getmatch'''


class MyTestCase(unittest.TestCase):
    '''def test_something(self):
        #self.assertEqual(True, False)  # add assertion here
        print('hello')'''

    def test_loadjason(self):
        ldf.loadDatabaseFile()
        self.assertEqual(len(globals.peak_data), 3, 'Failed  loadjason')

    '''def test_getmatch(self):
        #print('testing get match')
        ldf.loadDatabaseFile()
        default_peaks = [330.9, 296.5, 92.6, 1253.7, 330.7]
        default_sigma = [0.45] * len(default_peaks)
        input_data = list(zip(default_peaks, default_sigma))
        good_res=[[{'element': 'Cu', 'energy': 330.9, 'error': 0, 'peak_centre': 330.9, 'transition': 'L(3d->2p)', 'diff': 0}, {'element': 'Mg', 'energy': 296.5, 'error': 0, 'peak_centre': 296.5, 'transition': 'K(2p->1s)', 'diff': 0}, {'element': 'Fe', 'energy': 92.6, 'error': 0, 'peak_centre': 92.6, 'transition': 'M(4f->3d)', 'diff': 0}, {'element': 'Fe', 'energy': 1253.7, 'error': 0, 'peak_centre': 1253.7, 'transition': 'K(2p1/2->1s1/2)', 'diff': 0}, {'element': 'Se', 'energy': 296.3, 'error': 0.45, 'peak_centre': 296.5, 'transition': 'M(7f->3d)', 'diff': 0.19999999999998863}, {'element': 'Cu', 'energy': 330.9, 'error': 0.45, 'peak_centre': 330.7, 'transition': 'L(3d->2p)', 'diff': 0.19999999999998863}, {'element': 'Mn', 'energy': 331.2, 'error': 0.45, 'peak_centre': 330.9, 'transition': 'L(4d->2p)', 'diff': 0.30000000000001137}, {'element': 'Sn', 'energy': 331.2, 'error': 0.45, 'peak_centre': 330.9, 'transition': 'N(8g->4f)', 'diff': 0.30000000000001137}, {'element': 'Mg', 'energy': 93.0, 'error': 0.45, 'peak_centre': 92.6, 'transition': 'L(7d->2p)', 'diff': 0.4000000000000057}, {'element': 'In', 'energy': 331.3, 'error': 0.45, 'peak_centre': 330.9, 'transition': 'M(4f->3d)', 'diff': 0.4000000000000341}, {'element': 'Ni', 'energy': 93.1, 'error': 0.9, 'peak_centre': 92.6, 'transition': 'N(7g->4f)', 'diff': 0.5}, {'element': 'Mn', 'energy': 331.2, 'error': 0.9, 'peak_centre': 330.7, 'transition': 'L(4d->2p)', 'diff': 0.5}, {'element': 'Sn', 'energy': 331.2, 'error': 0.9, 'peak_centre': 330.7, 'transition': 'N(8g->4f)', 'diff': 0.5}, {'element': 'Ce', 'energy': 331.5, 'error': 0.9, 'peak_centre': 330.9, 'transition': 'N(6g->4f)', 'diff': 0.6000000000000227}, {'element': 'In', 'energy': 331.3, 'error': 0.9, 'peak_centre': 330.7, 'transition': 'M(4f->3d)', 'diff': 0.6000000000000227}, {'element': 'Er', 'energy': 295.8, 'error': 0.9, 'peak_centre': 296.5, 'transition': 'N(5g->4f)', 'diff': 0.6999999999999886}, {'element': 'Na', 'energy': 297.2, 'error': 0.9, 'peak_centre': 296.5, 'transition': 'K(3p->1s)', 'diff': 0.6999999999999886}, {'element': 'Ta', 'energy': 295.8, 'error': 0.9, 'peak_centre': 296.5, 'transition': 'O(7h->5g)', 'diff': 0.6999999999999886}, {'element': 'K', 'energy': 93.3, 'error': 0.9, 'peak_centre': 92.6, 'transition': 'M(7f->3d)', 'diff': 0.7000000000000028}, {'element': 'Hf', 'energy': 331.6, 'error': 0.9, 'peak_centre': 330.9, 'transition': 'N(5g->4f)', 'diff': 0.7000000000000455}, {'element': 'V', 'energy': 331.6, 'error': 0.9, 'peak_centre': 330.9, 'transition': 'L(6d->2p)', 'diff': 0.7000000000000455}, {'element': 'Ce', 'energy': 331.5, 'error': 0.9, 'peak_centre': 330.7, 'transition': 'N(6g->4f)', 'diff': 0.8000000000000114}]]
        res, res1, res2 = getmatch.get_matches(input_data)

        self.assertEqual(res, good_res, 'Failed get_match')
        #print('passed')

    def test_plusonebutto(self):
        print('plus one')

    def test_loadcomment(self):
        #print('loadcomment test')
        globals.workingdirectory='./TestData/'
        RunNum=2630
        flag, rtnstr = loadcomment.loadcomment(RunNum)
        self.assertEqual(flag, 1, 'did return flag')
        self.assertEqual(rtnstr,['Start Time        :  Thu May 3 13:08:56 2018\n',
                                 'End   Time        :  Thu May 3 13:58:33 2018\n',
                                 'Number of Events  : 118466\n',
                                 'Comments : Mu- 40MeV/c Ti 40x40mm ISIS furnace sample holders\n'],
                         'didnt load commnet file')

    def test_loadcomment2(self):
        #print('loadcomment2 test')
        globals.workingdirectory='./TestData/'
        RunNum=999
        flag, rtnstr = loadcomment.loadcomment(RunNum)
        self.assertEqual(flag, 0, 'did return flag')
        self.assertEqual(rtnstr,[" ", " ", " ", " "],
                         'didnt load comment file')

    def test_loadcomment3(self):
        #print('loadcomment3 test')
        globals.workingdirectory='./'
        RunNum=2631
        flag,rtnstr = loadcomment.loadcomment(RunNum)
        self.assertEqual(flag, 0, 'did return flag')
        self.assertEqual(rtnstr,[" ", " ", " ", " "],
                         'didnt load commnet file')

    def test_loaddata(self):
        #print('loadcdata test')
        globals.workingdirectory = './TestData/'
        RunNum = 2630
        loaddata.loaddata(RunNum)
        self.assertEqual(globals.flag_d_GE1, 1,'didnt load ge1 data')
        self.assertEqual(globals.flag_d_GE2, 1,'didnt load ge2 data')
        self.assertEqual(globals.flag_d_GE3, 1,'didnt load ge3 data')
        self.assertEqual(globals.flag_d_GE4, 1,'didnt load ge4 data')

    def test_loaddata2(self):
        #print('loadcdata test')
        globals.workingdirectory = './TestData/'
        RunNum = 999
        loaddata.loaddata(RunNum)
        self.assertEqual(globals.flag_d_GE1, 0,'didnt load ge1 data')
        self.assertEqual(globals.flag_d_GE2, 0,'didnt load ge2 data')
        self.assertEqual(globals.flag_d_GE3, 0,'didnt load ge3 data')
        self.assertEqual(globals.flag_d_GE4, 0,'didnt load ge4 data')

    def test_loaddata3(self):
        #print('loadcdata test')
        globals.E_Corr_GE1_apply = False
        globals.E_Corr_GE2_apply = False
        globals.E_Corr_GE3_apply = False
        globals.E_Corr_GE4_apply = False
        globals.workingdirectory = './Testdata/'
        RunNum = 2630
        loaddata.loaddata(RunNum)

        self.assertEqual(globals.x_GE1[100], 99.5,'didnt load ge1 data')
        self.assertEqual(globals.y_GE1[100], 110.0,'didnt load ge2 data')
        self.assertEqual(globals.x_GE2[100], 99.5 ,'didnt load ge1 data')
        self.assertEqual(globals.y_GE2[100], 63.0,'didnt load ge2 data')
        self.assertEqual(globals.x_GE3[100], 12.4375,'didnt load ge1 data')
        self.assertEqual(globals.y_GE3[100], 19.0,'didnt load ge2 data')
        self.assertEqual(globals.x_GE4[100], 12.4375 ,'didnt load ge1 data')
        self.assertEqual(globals.y_GE4[100], 20.0,'didnt load ge2 data')

    def test_gammaload(self):
        lg.loadgamma()
        length = sum([len(sub_list) for sub_list in globals.Full_Gammas])
        #print('length', length)
        self.assertEqual(length,274570,'load gamma failed')

    def test_gammaload2(self):
        lg.loadgamma()
        self.assertEqual(len(globals.Full_Gammas),119,'load gamma failed')

    def test_saveeffparaGE1(self):
        Eff_Window.Correction_Eff.save_GE_Eff_settings(self,"GE1", 100, 101, 102, 103, 104)

        self.assertEqual(globals.Eff_Corr_GE1_P0,100,'Save Eff Parameters P0 Error')
        self.assertEqual(globals.Eff_Corr_GE1_P1,101,'Save Eff Parameters P1 Error')
        self.assertEqual(globals.Eff_Corr_GE1_P2,102,'Save Eff Parameters P2 Error')
        self.assertEqual(globals.Eff_Corr_GE1_P3,103,'Save Eff Parameters P3 Error')
        self.assertEqual(globals.Eff_Corr_GE1_P4,104,'Save Eff Parameters P4 Error')

    def test_saveeffparaGE2(self):
        Eff_Window.Correction_Eff.save_GE_Eff_settings(self,"GE2", 100, 101, 102, 103, 104)

        self.assertEqual(globals.Eff_Corr_GE2_P0,100,'Save Eff Parameters P0 Error')
        self.assertEqual(globals.Eff_Corr_GE2_P1,101,'Save Eff Parameters P1 Error')
        self.assertEqual(globals.Eff_Corr_GE2_P2,102,'Save Eff Parameters P2 Error')
        self.assertEqual(globals.Eff_Corr_GE2_P3,103,'Save Eff Parameters P3 Error')
        self.assertEqual(globals.Eff_Corr_GE2_P4,104,'Save Eff Parameters P4 Error')

    def test_saveeffparaGE3(self):
        Eff_Window.Correction_Eff.save_GE_Eff_settings(self,"GE3", 100, 101, 102, 103, 104)

        self.assertEqual(globals.Eff_Corr_GE3_P0,100,'Save Eff Parameters P0 Error')
        self.assertEqual(globals.Eff_Corr_GE3_P1,101,'Save Eff Parameters P1 Error')
        self.assertEqual(globals.Eff_Corr_GE3_P2,102,'Save Eff Parameters P2 Error')
        self.assertEqual(globals.Eff_Corr_GE3_P3,103,'Save Eff Parameters P3 Error')
        self.assertEqual(globals.Eff_Corr_GE3_P4,104,'Save Eff Parameters P4 Error')

    def test_saveeffparaGE4(self):
        Eff_Window.Correction_Eff.save_GE_Eff_settings(self,"GE4", 100, 101, 102, 103, 104)

        self.assertEqual(globals.Eff_Corr_GE4_P0,100,'Save Eff Parameters P0 Error')
        self.assertEqual(globals.Eff_Corr_GE4_P1,101,'Save Eff Parameters P1 Error')
        self.assertEqual(globals.Eff_Corr_GE4_P2,102,'Save Eff Parameters P2 Error')
        self.assertEqual(globals.Eff_Corr_GE4_P3,103,'Save Eff Parameters P3 Error')
        self.assertEqual(globals.Eff_Corr_GE4_P4,104,'Save Eff Parameters P4 Error')


    def test_Energy_Correction_GE1(self):
        RunNum = 2630
        loaddata.loaddata(RunNum)
        #print(globals.flag_d_GE1)

        globals.E_Corr_GE1_apply = True
        globals.E_Corr_GE2_apply = False
        globals.E_Corr_GE3_apply = False
        globals.E_Corr_GE4_apply = False

        m = 2.0
        c = 1.0

        expected_result = globals.x_GE1 * m + c
        globals.E_Corr_GE1_gradient = 2.0
        globals.E_Corr_GE1_offset = 1.0
        Energy_Corrections.Energy_Corrections()

        self.assertEqual(globals.x_GE1[100], expected_result[100], 'Error in Energy Corrections')

    def test_Energy_Correction_GE2(self):
        RunNum = 2630
        loaddata.loaddata(RunNum)
        # print(globals.flag_d_GE1)

        globals.E_Corr_GE1_apply = False
        globals.E_Corr_GE2_apply = True
        globals.E_Corr_GE3_apply = False
        globals.E_Corr_GE4_apply = False

        m = 2.13
        c = 1.12

        expected_result = globals.x_GE2 * m + c
        globals.E_Corr_GE2_gradient = 2.13
        globals.E_Corr_GE2_offset = 1.12
        Energy_Corrections.Energy_Corrections()

        self.assertEqual(globals.x_GE2[100], expected_result[100], 'Error in Energy Corrections')

    def test_Energy_Correction_GE3(self):
        RunNum = 2630
        loaddata.loaddata(RunNum)
        # print(globals.flag_d_GE1)

        globals.E_Corr_GE1_apply = False
        globals.E_Corr_GE2_apply = False
        globals.E_Corr_GE3_apply = True
        globals.E_Corr_GE4_apply = False

        m = 2.02
        c = 1.01

        expected_result = globals.x_GE3 * m + c
        globals.E_Corr_GE3_gradient = 2.02
        globals.E_Corr_GE3_offset = 1.01
        Energy_Corrections.Energy_Corrections()

        self.assertEqual(globals.x_GE3[100], expected_result[100], 'Error in Energy Corrections')

    def test_Energy_Correction_GE4(self):
        RunNum = 2630
        loaddata.loaddata(RunNum)
        # print(globals.flag_d_GE1)

        globals.E_Corr_GE1_apply = False
        globals.E_Corr_GE2_apply = False
        globals.E_Corr_GE3_apply = False
        globals.E_Corr_GE4_apply = True

        m = 2.034
        c = 1.034

        expected_result = globals.x_GE4 * m + c
        globals.E_Corr_GE4_gradient = 2.034
        globals.E_Corr_GE4_offset = 1.034
        Energy_Corrections.Energy_Corrections()

        self.assertEqual(globals.x_GE4[100], expected_result[100], 'Error in Energy Corrections')

    def test_Energy_Correction_GEAll(self):
        RunNum = 2630
        loaddata.loaddata(RunNum)
        # print(globals.flag_d_GE1)

        globals.E_Corr_GE1_apply = True
        globals.E_Corr_GE2_apply = True
        globals.E_Corr_GE3_apply = True
        globals.E_Corr_GE4_apply = True

        m = 2.023
        c = 1.023

        expected_result = globals.x_GE1 * m + c
        globals.E_Corr_GE1_gradient = 2.023
        globals.E_Corr_GE1_offset = 1.023
        Energy_Corrections.Energy_Corrections()

        self.assertEqual(globals.x_GE1[100], expected_result[100], 'Error in Energy Corrections')

        m = 2.032
        c = 1.032

        expected_result = globals.x_GE2 * m + c
        globals.E_Corr_GE2_gradient = 2.032
        globals.E_Corr_GE2_offset = 1.032
        Energy_Corrections.Energy_Corrections()

        self.assertEqual(globals.x_GE2[100], expected_result[100], 'Error in Energy Corrections')

        m = 2.052
        c = 1.052

        expected_result = globals.x_GE3 * m + c
        globals.E_Corr_GE3_gradient = 2.052
        globals.E_Corr_GE3_offset = 1.052
        Energy_Corrections.Energy_Corrections()

        self.assertEqual(globals.x_GE3[100], expected_result[100], 'Error in Energy Corrections')

        m = 2.099
        c = 1.099

        expected_result = globals.x_GE4 * m + c
        globals.E_Corr_GE4_gradient = 2.099
        globals.E_Corr_GE4_offset = 1.099
        Energy_Corrections.Energy_Corrections()

        self.assertEqual(globals.x_GE4[100], expected_result[100], 'Error in Energy Corrections')




    def test_gammamatch(self):
        lg.loadgamma()
        res=[{'Element': '140Eu', 'Energy': 20.5, 'diff': 0.0, 'Intensity': ' 0.000E+00', 'lifetime': '        '},
             {'Element': '140Eu', 'Energy': 20.5, 'diff': 0.0, 'Intensity': ' 0.000E+00', 'lifetime': '        '},
             {'Element': '140Eu', 'Energy': 20.5, 'diff': 0.0, 'Intensity': ' 0.000E+00', 'lifetime': '        '}]
        default_peaks = [20.500]
        default_sigma = [0.01] * len(default_peaks)
        input_data = list(zip(default_peaks, default_sigma))
        match=getmatch.getmatchesgammas(input_data)
        #print(res)
        #print(match)
        self.assertEqual(match, res, 'load gamma failed')

    def make_setupsample(self):
        #setting up default layer

        i = 0
        Sample_layer = []
        TotalThickness = 0.0
        sampledensity = 1.0

        for i in range(4):
            if i == 0 :
                sampleName = 'Beamline Window'
                LayerThickness = 0.05
            elif i == 1:
                sampleName = 'Air (compressed)'
                LayerThickness = 0.067
            elif i == 2:
                sampleName = 'Al'
                LayerThickness = 0.05
                sampledensity = 2.7
            else:
                sampleName = 'Cu'
                LayerThickness = 0.5
                sampledensity = 6.7

            if sampleName == 'Beamline Window':
                #LayerThickness = float(self.tab1.table_TRIMsetup.item(i, 1).text())
                TotalThickness = + LayerThickness
                beamwindow = Layer({'H': {'stoich': 8, 'E_d': 10, 'lattice': 3, 'surface': 2
                                          },
                                    'C': {'stoich': 10, 'E_d': 28.0, 'lattice': 3.0,
                                          'surface': 7.41
                                          },
                                    'O': {'stoich': 4, 'E_d': 28.0, 'lattice': 3.0,
                                          'surface': 2.0}},
                                   density=1.4, width=LayerThickness * 1e7, phase=0)
                Sample_layer.append(beamwindow)
                globals.sample_name.append('Beamline Window')

            elif sampleName == 'Air (compressed)':

                #LayerThickness = float(self.tab1.table_TRIMsetup.item(i, 1).text())
                TotalThickness = + LayerThickness

                air = Layer({'C': {'stoich': 1.24e-2, 'E_d': 28.0, 'lattice': 3.0,
                                   'surface': 7.41
                                   },
                             'O': {'stoich': 23.1781, 'E_d': 28.0, 'lattice': 3.0,
                                   'surface': 2.0
                                   },
                             'N': {'stoich': 75.5268, 'E_d': 28.0, 'lattice': 3.0,
                                   'surface': 2.0
                                   },
                             'Ar': {'stoich': 1.2827, 'E_d': 5.0, 'lattice': 1.0,
                                    'surface': 2.0}}, density=1500 * 1.20479e-3, width=LayerThickness * 1e7,
                            # air layer compressed from 150mm to 0.1mm to optimise bins
                            phase=1)
                Sample_layer.append(air)
                globals.sample_name.append('Air (compressed)')
                #print ('done air')
                #print(Sample_layer)
            else:
                #sampledensity = float(self.tab1.table_TRIMsetup.item(i, 2).text())
                #samplethickness = float(self.tab1.table_TRIMsetup.item(i, 1).text())
                TotalThickness = + LayerThickness
                thislayer = Layer.from_formula(sampleName, density=sampledensity, width=LayerThickness * 1e7,
                                               phase=0)

                Sample_layer.append(thislayer)  # 0.016 mm = 160000Athick sample holder
                globals.sample_name.append(sampleName)



        globals.sample_layers = Sample_layer

        return Sample_layer, TotalThickness

    def test_getxpos(self):
        SL, TT = MyTestCase.make_setupsample(self)
        correct_res = [0.0, 0.05, 0.067, 0.05, 0.5]
        res = TRIM_Window.RunSimTRIMSRIM.getxpos(self)
        self.assertEqual(correct_res, res, 'xposlist failed')

    def test_get_comp27(self):
        globals.TRIMRes_x = [[0.00667, 0.01334, 0.02001, 0.02668, 0.03335, 0.04002, 0.04669, 0.05336, 0.06003, 0.0667, 0.07337, 0.08004, 0.08671, 0.09338, 0.10005, 0.10672, 0.11339, 0.12006, 0.12673, 0.1334, 0.14007, 0.14674, 0.15341, 0.16008, 0.16675, 0.17342, 0.18009, 0.18676, 0.19343, 0.2001, 0.20677, 0.21344, 0.22011, 0.22678, 0.23345, 0.24012, 0.24679, 0.25346, 0.26013, 0.2668, 0.27347, 0.28014, 0.28681, 0.29348, 0.30015, 0.30682, 0.31349, 0.32016, 0.32683, 0.3335, 0.34017, 0.34684, 0.35351, 0.36018, 0.36685, 0.37352, 0.38019, 0.38686, 0.39353, 0.4002, 0.40687, 0.41354, 0.42021, 0.42688, 0.43355, 0.44022, 0.44689, 0.45356, 0.46023, 0.4669, 0.47357, 0.48024, 0.48691, 0.49358, 0.50025, 0.50692, 0.51359, 0.52026, 0.52693, 0.5336, 0.54027, 0.54694, 0.55361, 0.56028, 0.56695, 0.57362, 0.58029, 0.58696, 0.59363, 0.6003, 0.60697, 0.61364, 0.62031, 0.62698, 0.63365, 0.64032, 0.64699, 0.65366, 0.66033, 0.667]]

        globals.TRIMRes_y = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.4965, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 22.489, 7.4965, 74.965, 149.925, 97.45, 202.4, 104.95000000000002, 59.97, 22.489, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
        correct_res = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.4965, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 22.489, 7.4965, 74.965, 149.925, 97.45, 202.4, 104.95000000000002, 59.97, 22.489, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]


        SL, TT = MyTestCase.make_setupsample(self)
        xposlist = TRIM_Window.RunSimTRIMSRIM.getxpos(self)
        res = TRIM_Window.RunSimTRIMSRIM.getcomp(self,xposlist,0)
        perlayer = [0.0, 0.0, 0.0, 1.0]

        self.assertEqual(correct_res, res, 'comp failed')

    def test_getperlayer27(self):
        comp = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.4965, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 22.489, 7.4965, 74.965, 149.925, 97.45, 202.4, 104.95000000000002, 59.97, 22.489, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]


        SL, TT = MyTestCase.make_setupsample(self)
        res = TRIM_Window.RunSimTRIMSRIM.getperlayer(self, comp)
        correct_res = [0.0, 0.0, 0.0, 1.0]

        self.assertEqual(correct_res, res, 'comp failed')

    def test_get_comp17(self):
        globals.TRIMRes_x = [[0.00667, 0.01334, 0.02001, 0.02668, 0.03335, 0.04002, 0.04669, 0.05336, 0.06003, 0.0667, 0.07337, 0.08004, 0.08671, 0.09338, 0.10005, 0.10672, 0.11339, 0.12006, 0.12673, 0.1334, 0.14007, 0.14674, 0.15341, 0.16008, 0.16675, 0.17342, 0.18009, 0.18676, 0.19343, 0.2001, 0.20677, 0.21344, 0.22011, 0.22678, 0.23345, 0.24012, 0.24679, 0.25346, 0.26013, 0.2668, 0.27347, 0.28014, 0.28681, 0.29348, 0.30015, 0.30682, 0.31349, 0.32016, 0.32683, 0.3335, 0.34017, 0.34684, 0.35351, 0.36018, 0.36685, 0.37352, 0.38019, 0.38686, 0.39353, 0.4002, 0.40687, 0.41354, 0.42021, 0.42688, 0.43355, 0.44022, 0.44689, 0.45356, 0.46023, 0.4669, 0.47357, 0.48024, 0.48691, 0.49358, 0.50025, 0.50692, 0.51359, 0.52026, 0.52693, 0.5336, 0.54027, 0.54694, 0.55361, 0.56028, 0.56695, 0.57362, 0.58029, 0.58696, 0.59363, 0.6003, 0.60697, 0.61364, 0.62031, 0.62698, 0.63365, 0.64032, 0.64699, 0.65366, 0.66033, 0.667]]

        globals.TRIMRes_y = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.496310000000001, 0.0, 7.496180000000001, 0.0, 14.992372, 14.992500000000001, 82.45853349999999, 232.3843415, 479.7652625, 1214.3907035, 2271.358098, 3215.8880915, 4137.94343, 3530.72735, 3118.4377, 1596.704372, 1176.91095, 472.2630000000001, 344.83145, 44.977500000000006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
        correct_res = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.496310000000001, 0.0, 7.496180000000001, 0.0, 14.992372, 14.992500000000001, 82.45853349999999, 232.3843415, 479.7652625, 1214.3907035, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2271.358098, 3215.8880915, 4137.94343, 3530.72735, 3118.4377, 1596.704372, 1176.91095, 472.2630000000001, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 344.83145, 44.977500000000006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]


        SL, TT = MyTestCase.make_setupsample(self)
        xposlist = TRIM_Window.RunSimTRIMSRIM.getxpos(self)
        res = TRIM_Window.RunSimTRIMSRIM.getcomp(self,xposlist,0)
        perlayer = [0.0, 0.0, 0.0, 1.0]

        self.assertEqual(correct_res, res, 'comp failed')

    def test_getperlayer17(self):
        comp = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.496310000000001, 0.0, 7.496180000000001, 0.0, 14.992372, 14.992500000000001, 82.45853349999999, 232.3843415, 479.7652625, 1214.3907035, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2271.358098, 3215.8880915, 4137.94343, 3530.72735, 3118.4377, 1596.704372, 1176.91095, 472.2630000000001, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 344.83145, 44.977500000000006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]


        SL, TT = MyTestCase.make_setupsample(self)
        res = TRIM_Window.RunSimTRIMSRIM.getperlayer(self, comp)
        correct_res = [0.0, 0.09351550292332715, 0.8887368815249342, 0.01774761555173874]

        self.assertEqual(correct_res, res, 'comp failed')

    def test_iondef(self):

        res = TRIM_Window.RunSimTRIMSRIM.iondef(27)
        correct_res = Ion('H', 3.395245806628296*1e6, 0.11342820665593129)
        self.assertEqual(correct_res, res, 'iondef failed')'''

class LoadJason(unittest.TestCase):
    def test_loadjason(self):
        ldf.loadDatabaseFile()
        self.assertEqual(len(globals.peak_data), 3, 'Failed  loadjason')


if __name__ == '__main__':
    print('hi')
    unittest.main()
    MyTestCase.test_loadjason()
    '''Test_LoadJason.LoadJason.test_loadjason()'''
    '''MyTestCase.test_getmatch()
    MyTestCase.test_loadcomment()
    MyTestCase.test_loadcomment2()
    MyTestCase.test_loadcomment3()
    MyTestCase.test_loaddata()
    MyTestCase.test_loaddata2()
    MyTestCase.test_loaddata3()
    MyTestCase.test_gammaload()
    MyTestCase.test_gammaload2()
    MyTestCase.test_saveeffparaGE1()
    MyTestCase.test_saveeffparaGE2()
    MyTestCase.test_saveeffparaGE3()
    MyTestCase.test_saveeffparaGE4()
    MyTestCase.test_Energy_Correction_GE1()
    MyTestCase.test_Energy_Correction_GE2()
    MyTestCase.test_Energy_Correction_GE3()
    MyTestCase.test_Energy_Correction_GE4()
    MyTestCase.test_Energy_Correction_GEAll()
    MyTestCase.test_getxpos()
    MyTestCase.test_get_comp27()
    MyTestCase.test_getperlayer27()
    MyTestCase.test_get_comp17()
    MyTestCase.test_getperlayer17()
    MyTestCase.test_iondef()'''
    '''Test_LoadJason.LoadJason()
    Test_getmatch.get_match.test_getmatch()'''







