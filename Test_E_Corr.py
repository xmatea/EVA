import unittest

import globals

import loaddata

import Energy_Corrections


class MyTestCase(unittest.TestCase):

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


