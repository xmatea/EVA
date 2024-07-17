import unittest

import getmatch

import loadgamma as lg


class MyTestCase(unittest.TestCase):

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
