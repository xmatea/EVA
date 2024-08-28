import unittest
import globals
import loadgamma as lg


class MyTestCase(unittest.TestCase):
    '''def test_something(self):
        #self.assertEqual(True, False)  # add assertion here
        print('hello')'''
    def test_gammaload(self):
        lg.loadgamma()
        length = sum([len(sub_list) for sub_list in globals.Full_Gammas])
        #print('length', length)
        self.assertEqual(length,274570,'load gamma failed')

    def test_gammaload2(self):
        lg.loadgamma()
        self.assertEqual(len(globals.Full_Gammas), 119, 'load gamma failed')
