import unittest
from EVA import loadcomment, globals


class LoadComment(unittest.TestCase):
    '''def test_something(self):
        #self.assertEqual(True, False)  # add assertion here
        print('hello')'''
    def test_loadcomment(self):
        #print('loadcomment test')
        globals.workingdirectory= './TestData/'
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
        globals.workingdirectory= './TestData/'
        RunNum=999
        flag, rtnstr = loadcomment.loadcomment(RunNum)
        self.assertEqual(flag, 0, 'did return flag')
        self.assertEqual(rtnstr,[" ", " ", " ", " "],
                         'didnt load comment file')

    def test_loadcomment3(self):
        #print('loadcomment3 test')
        globals.workingdirectory= './'
        RunNum=2631
        flag,rtnstr = loadcomment.loadcomment(RunNum)
        self.assertEqual(flag, 0, 'did return flag')
        self.assertEqual(rtnstr,[" ", " ", " ", " "],
                         'didnt load commnet file')
