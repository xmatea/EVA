import unittest
import LoadDatabaseFile as ldf
import globals
import getmatch
import loadcomment
import loaddata



class MyTestCase(unittest.TestCase):
    def test_something(self):
        #self.assertEqual(True, False)  # add assertion here
        print('hello')

    def test_loadjason(self):
        ldf.loadDatabaseFile()
        self.assertEqual(len(globals.peak_data), 3, 'Failed  loadjason')

    def test_getmatch(self):
        print('testing get match')
        ldf.loadDatabaseFile()
        default_peaks = [330.9, 296.5, 92.6, 1253.7, 330.7]
        default_sigma = [0.45] * len(default_peaks)
        input_data = list(zip(default_peaks, default_sigma))
        good_res=[[{'element': 'Cu', 'energy': 330.9, 'error': 0, 'peak_centre': 330.9, 'transition': 'L(3d->2p)', 'diff': 0}, {'element': 'Mg', 'energy': 296.5, 'error': 0, 'peak_centre': 296.5, 'transition': 'K(2p->1s)', 'diff': 0}, {'element': 'Fe', 'energy': 92.6, 'error': 0, 'peak_centre': 92.6, 'transition': 'M(4f->3d)', 'diff': 0}, {'element': 'Fe', 'energy': 1253.7, 'error': 0, 'peak_centre': 1253.7, 'transition': 'K(2p1/2->1s1/2)', 'diff': 0}, {'element': 'Se', 'energy': 296.3, 'error': 0.45, 'peak_centre': 296.5, 'transition': 'M(7f->3d)', 'diff': 0.19999999999998863}, {'element': 'Cu', 'energy': 330.9, 'error': 0.45, 'peak_centre': 330.7, 'transition': 'L(3d->2p)', 'diff': 0.19999999999998863}, {'element': 'Mn', 'energy': 331.2, 'error': 0.45, 'peak_centre': 330.9, 'transition': 'L(4d->2p)', 'diff': 0.30000000000001137}, {'element': 'Sn', 'energy': 331.2, 'error': 0.45, 'peak_centre': 330.9, 'transition': 'N(8g->4f)', 'diff': 0.30000000000001137}, {'element': 'Mg', 'energy': 93.0, 'error': 0.45, 'peak_centre': 92.6, 'transition': 'L(7d->2p)', 'diff': 0.4000000000000057}, {'element': 'In', 'energy': 331.3, 'error': 0.45, 'peak_centre': 330.9, 'transition': 'M(4f->3d)', 'diff': 0.4000000000000341}, {'element': 'Ni', 'energy': 93.1, 'error': 0.9, 'peak_centre': 92.6, 'transition': 'N(7g->4f)', 'diff': 0.5}, {'element': 'Mn', 'energy': 331.2, 'error': 0.9, 'peak_centre': 330.7, 'transition': 'L(4d->2p)', 'diff': 0.5}, {'element': 'Sn', 'energy': 331.2, 'error': 0.9, 'peak_centre': 330.7, 'transition': 'N(8g->4f)', 'diff': 0.5}, {'element': 'Ce', 'energy': 331.5, 'error': 0.9, 'peak_centre': 330.9, 'transition': 'N(6g->4f)', 'diff': 0.6000000000000227}, {'element': 'In', 'energy': 331.3, 'error': 0.9, 'peak_centre': 330.7, 'transition': 'M(4f->3d)', 'diff': 0.6000000000000227}, {'element': 'Er', 'energy': 295.8, 'error': 0.9, 'peak_centre': 296.5, 'transition': 'N(5g->4f)', 'diff': 0.6999999999999886}, {'element': 'Na', 'energy': 297.2, 'error': 0.9, 'peak_centre': 296.5, 'transition': 'K(3p->1s)', 'diff': 0.6999999999999886}, {'element': 'Ta', 'energy': 295.8, 'error': 0.9, 'peak_centre': 296.5, 'transition': 'O(7h->5g)', 'diff': 0.6999999999999886}, {'element': 'K', 'energy': 93.3, 'error': 0.9, 'peak_centre': 92.6, 'transition': 'M(7f->3d)', 'diff': 0.7000000000000028}, {'element': 'Hf', 'energy': 331.6, 'error': 0.9, 'peak_centre': 330.9, 'transition': 'N(5g->4f)', 'diff': 0.7000000000000455}, {'element': 'V', 'energy': 331.6, 'error': 0.9, 'peak_centre': 330.9, 'transition': 'L(6d->2p)', 'diff': 0.7000000000000455}, {'element': 'Ce', 'energy': 331.5, 'error': 0.9, 'peak_centre': 330.7, 'transition': 'N(6g->4f)', 'diff': 0.8000000000000114}]]

        self.assertEqual(getmatch.get_matches(input_data), good_res, 'Failed get_match')
        print('passed')

    def test_plusonebutto(self):
        print('plus one')

    def test_loadcomment(self):
        print('loadcomment test')
        globals.workingdirectory='.'
        RunNum=2630
        flag,rtnstr = loadcomment.loadcomment(RunNum)
        self.assertEqual(flag, 1, 'did return flag')
        self.assertEqual(rtnstr,['Start Time        :  Thu May 3 13:08:56 2018\n',
                                 'End   Time        :  Thu May 3 13:58:33 2018\n',
                                 'Number of Events  : 118466\n',
                                 'Comments : Mu- 40MeV/c Ti 40x40mm ISIS furnace sample holders\n'],
                         'didnt load commnet file')

    def test_loadcomment2(self):
        print('loadcomment2 test')
        globals.workingdirectory='.'
        RunNum=999
        flag,rtnstr = loadcomment.loadcomment(RunNum)
        self.assertEqual(flag, 0, 'did return flag')
        self.assertEqual(rtnstr,[" ", " ", " ", " "],
                         'didnt load comment file')

    def test_loadcomment3(self):
        print('loadcomment3 test')
        globals.workingdirectory='../..'
        RunNum=2631
        flag,rtnstr = loadcomment.loadcomment(RunNum)
        self.assertEqual(flag, 0, 'did return flag')
        self.assertEqual(rtnstr,[" ", " ", " ", " "],
                         'didnt load commnet file')

    def test_loaddata(self):
        print('loadcdata test')
        globals.workingdirectory = '.'
        RunNum = 2630
        loaddata.loaddata(RunNum)
        self.assertEqual(globals.flag_d_GE1, 1,'didnt load ge1 data')
        self.assertEqual(globals.flag_d_GE2, 1,'didnt load ge2 data')
        self.assertEqual(globals.flag_d_GE3, 1,'didnt load ge3 data')
        self.assertEqual(globals.flag_d_GE4, 1,'didnt load ge4 data')

    def test_loaddata2(self):
        print('loadcdata test')
        globals.workingdirectory = '.'
        RunNum = 999
        loaddata.loaddata(RunNum)
        self.assertEqual(globals.flag_d_GE1, 0,'didnt load ge1 data')
        self.assertEqual(globals.flag_d_GE2, 0,'didnt load ge2 data')
        self.assertEqual(globals.flag_d_GE3, 0,'didnt load ge3 data')
        self.assertEqual(globals.flag_d_GE4, 0,'didnt load ge4 data')

    def test_loaddata3(self):
        print('loadcdata test')
        globals.workingdirectory = '.'
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



if __name__ == '__main__':
    unittest.main()
    MyTestCase.test_loadjason()
    MyTestCase.test_getmatch()
    MyTestCase.test_loadcomment()
    MyTestCase.test_loadcomment2()
    MyTestCase.test_loadcomment3()
    MyTestCase.test_loaddata()
    MyTestCase.test_loaddata2()
    MyTestCase.test_loaddata3()






