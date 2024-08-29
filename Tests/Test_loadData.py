import unittest
from EVA import loaddata, globals


class LoadData(unittest.TestCase):
    '''def test_something(self):
        #self.assertEqual(True, False)  # add assertion here
        print('hello')'''

    def test_loaddata(self):
        # print('loadcdata test')
        globals.workingdirectory = './TestData/'
        RunNum = 2630
        loaddata.loaddata(RunNum)
        self.assertEqual(globals.flag_d_GE1, 1, 'didnt load ge1 data')
        self.assertEqual(globals.flag_d_GE2, 1, 'didnt load ge2 data')
        self.assertEqual(globals.flag_d_GE3, 1, 'didnt load ge3 data')
        self.assertEqual(globals.flag_d_GE4, 1, 'didnt load ge4 data')


    def test_loaddata2(self):
        # print('loadcdata test')
        globals.workingdirectory = './TestData/'
        RunNum = 999
        loaddata.loaddata(RunNum)
        self.assertEqual(globals.flag_d_GE1, 0, 'didnt load ge1 data')
        self.assertEqual(globals.flag_d_GE2, 0, 'didnt load ge2 data')
        self.assertEqual(globals.flag_d_GE3, 0, 'didnt load ge3 data')
        self.assertEqual(globals.flag_d_GE4, 0, 'didnt load ge4 data')


    def test_loaddata3(self):
        # print('loadcdata test')
        globals.E_Corr_GE1_apply = False
        globals.E_Corr_GE2_apply = False
        globals.E_Corr_GE3_apply = False
        globals.E_Corr_GE4_apply = False
        globals.workingdirectory = './Testdata/'
        RunNum = 2630
        loaddata.loaddata(RunNum)

        self.assertEqual(globals.x_GE1[100], 99.5, 'didnt load ge1 data')
        self.assertEqual(globals.y_GE1[100], 110.0, 'didnt load ge2 data')
        self.assertEqual(globals.x_GE2[100], 99.5, 'didnt load ge1 data')
        self.assertEqual(globals.y_GE2[100], 63.0, 'didnt load ge2 data')
        self.assertEqual(globals.x_GE3[100], 12.4375, 'didnt load ge1 data')
        self.assertEqual(globals.y_GE3[100], 19.0, 'didnt load ge2 data')
        self.assertEqual(globals.x_GE4[100], 12.4375, 'didnt load ge1 data')
        self.assertEqual(globals.y_GE4[100], 20.0, 'didnt load ge2 data')
