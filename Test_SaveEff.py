import unittest
import globals
import Eff_Window


class MyTestCase(unittest.TestCase):
    def test_saveeffparaGE1(self):
        Eff_Window.Correction_Eff.save_GE_Eff_settings(self, "GE1", 100, 101, 102, 103, 104)

        self.assertEqual(globals.Eff_Corr_GE1_P0, 100, 'Save Eff Parameters P0 Error')
        self.assertEqual(globals.Eff_Corr_GE1_P1, 101, 'Save Eff Parameters P1 Error')
        self.assertEqual(globals.Eff_Corr_GE1_P2, 102, 'Save Eff Parameters P2 Error')
        self.assertEqual(globals.Eff_Corr_GE1_P3, 103, 'Save Eff Parameters P3 Error')
        self.assertEqual(globals.Eff_Corr_GE1_P4, 104, 'Save Eff Parameters P4 Error')

    def test_saveeffparaGE2(self):
        Eff_Window.Correction_Eff.save_GE_Eff_settings(self, "GE2", 100, 101, 102, 103, 104)

        self.assertEqual(globals.Eff_Corr_GE2_P0, 100, 'Save Eff Parameters P0 Error')
        self.assertEqual(globals.Eff_Corr_GE2_P1, 101, 'Save Eff Parameters P1 Error')
        self.assertEqual(globals.Eff_Corr_GE2_P2, 102, 'Save Eff Parameters P2 Error')
        self.assertEqual(globals.Eff_Corr_GE2_P3, 103, 'Save Eff Parameters P3 Error')
        self.assertEqual(globals.Eff_Corr_GE2_P4, 104, 'Save Eff Parameters P4 Error')

    def test_saveeffparaGE3(self):
        Eff_Window.Correction_Eff.save_GE_Eff_settings(self, "GE3", 100, 101, 102, 103, 104)

        self.assertEqual(globals.Eff_Corr_GE3_P0, 100, 'Save Eff Parameters P0 Error')
        self.assertEqual(globals.Eff_Corr_GE3_P1, 101, 'Save Eff Parameters P1 Error')
        self.assertEqual(globals.Eff_Corr_GE3_P2, 102, 'Save Eff Parameters P2 Error')
        self.assertEqual(globals.Eff_Corr_GE3_P3, 103, 'Save Eff Parameters P3 Error')
        self.assertEqual(globals.Eff_Corr_GE3_P4, 104, 'Save Eff Parameters P4 Error')

    def test_saveeffparaGE4(self):
        Eff_Window.Correction_Eff.save_GE_Eff_settings(self, "GE4", 100, 101, 102, 103, 104)

        self.assertEqual(globals.Eff_Corr_GE4_P0, 100, 'Save Eff Parameters P0 Error')
        self.assertEqual(globals.Eff_Corr_GE4_P1, 101, 'Save Eff Parameters P1 Error')
        self.assertEqual(globals.Eff_Corr_GE4_P2, 102, 'Save Eff Parameters P2 Error')
        self.assertEqual(globals.Eff_Corr_GE4_P3, 103, 'Save Eff Parameters P3 Error')
        self.assertEqual(globals.Eff_Corr_GE4_P4, 104, 'Save Eff Parameters P4 Error')
