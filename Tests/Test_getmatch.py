import unittest
from EVA import LoadDatabaseFile as ldf, getmatch, globals
import numpy as np


class get_match(unittest.TestCase):
    def test_getmatch_gammas(self):
        #print('testing get match')
        globals.muon_database = "legacy"
        ldf.loadDatabaseFile()
        default_peaks = [330.9, 296.5, 92.6, 1253.7, 330.7]
        default_sigma = [0.45] * len(default_peaks)
        input_data = list(zip(default_peaks, default_sigma))
        good_res=[[{'element': 'Cu', 'energy': 330.9, 'error': 0, 'peak_centre': 330.9, 'transition': 'L(3d->2p)', 'diff': 0}, {'element': 'Mg', 'energy': 296.5, 'error': 0, 'peak_centre': 296.5, 'transition': 'K(2p->1s)', 'diff': 0}, {'element': 'Fe', 'energy': 92.6, 'error': 0, 'peak_centre': 92.6, 'transition': 'M(4f->3d)', 'diff': 0}, {'element': 'Fe', 'energy': 1253.7, 'error': 0, 'peak_centre': 1253.7, 'transition': 'K(2p1/2->1s1/2)', 'diff': 0}, {'element': 'Se', 'energy': 296.3, 'error': 0.45, 'peak_centre': 296.5, 'transition': 'M(7f->3d)', 'diff': 0.19999999999998863}, {'element': 'Cu', 'energy': 330.9, 'error': 0.45, 'peak_centre': 330.7, 'transition': 'L(3d->2p)', 'diff': 0.19999999999998863}, {'element': 'Mn', 'energy': 331.2, 'error': 0.45, 'peak_centre': 330.9, 'transition': 'L(4d->2p)', 'diff': 0.30000000000001137}, {'element': 'Sn', 'energy': 331.2, 'error': 0.45, 'peak_centre': 330.9, 'transition': 'N(8g->4f)', 'diff': 0.30000000000001137}, {'element': 'Mg', 'energy': 93.0, 'error': 0.45, 'peak_centre': 92.6, 'transition': 'L(7d->2p)', 'diff': 0.4000000000000057}, {'element': 'In', 'energy': 331.3, 'error': 0.45, 'peak_centre': 330.9, 'transition': 'M(4f->3d)', 'diff': 0.4000000000000341}, {'element': 'Ni', 'energy': 93.1, 'error': 0.9, 'peak_centre': 92.6, 'transition': 'N(7g->4f)', 'diff': 0.5}, {'element': 'Mn', 'energy': 331.2, 'error': 0.9, 'peak_centre': 330.7, 'transition': 'L(4d->2p)', 'diff': 0.5}, {'element': 'Sn', 'energy': 331.2, 'error': 0.9, 'peak_centre': 330.7, 'transition': 'N(8g->4f)', 'diff': 0.5}, {'element': 'Ce', 'energy': 331.5, 'error': 0.9, 'peak_centre': 330.9, 'transition': 'N(6g->4f)', 'diff': 0.6000000000000227}, {'element': 'In', 'energy': 331.3, 'error': 0.9, 'peak_centre': 330.7, 'transition': 'M(4f->3d)', 'diff': 0.6000000000000227}, {'element': 'Er', 'energy': 295.8, 'error': 0.9, 'peak_centre': 296.5, 'transition': 'N(5g->4f)', 'diff': 0.6999999999999886}, {'element': 'Na', 'energy': 297.2, 'error': 0.9, 'peak_centre': 296.5, 'transition': 'K(3p->1s)', 'diff': 0.6999999999999886}, {'element': 'Ta', 'energy': 295.8, 'error': 0.9, 'peak_centre': 296.5, 'transition': 'O(7h->5g)', 'diff': 0.6999999999999886}, {'element': 'K', 'energy': 93.3, 'error': 0.9, 'peak_centre': 92.6, 'transition': 'M(7f->3d)', 'diff': 0.7000000000000028}, {'element': 'Hf', 'energy': 331.6, 'error': 0.9, 'peak_centre': 330.9, 'transition': 'N(5g->4f)', 'diff': 0.7000000000000455}, {'element': 'V', 'energy': 331.6, 'error': 0.9, 'peak_centre': 330.9, 'transition': 'L(6d->2p)', 'diff': 0.7000000000000455}, {'element': 'Ce', 'energy': 331.5, 'error': 0.9, 'peak_centre': 330.7, 'transition': 'N(6g->4f)', 'diff': 0.8000000000000114}]]
        res, res1, res2 = getmatch.get_matches(input_data)

        self.assertEqual(res, good_res, 'Failed get_match')

    def test_getmatch_muon(self):
        # manually reset the database and load the mudirac data instead
        globals.muon_database = "mudirac"

        ldf.loadDatabaseFile()
        default_peaks = [330.9, 296.5, 92.6, 1253.7, 330.7]
        default_sigma = [0.45] * len(default_peaks)

        input_data = list(zip(default_peaks, default_sigma))
        target_res = ['65Cu', '63Cu', '54Fe', '124Sn', '24Mg', '25Mg', '56Fe', '122Sn', '57Fe', '120Sn', '58Fe', '118Sn',
                  '117Sn', '116Sn', '24Mg', '115Sn', '114Sn', '26Mg', '112Sn', '63Cu', '58Ni', '65Cu', '60Ni', '61Ni',
                  '62Ni', '64Ni', '24Mg', '25Mg', '26Mg', '55Mn', '25Mg', '124Sn', '122Sn', '120Sn', '118Sn', '117Sn',
                  '116Sn', '26Mg', '115Sn', '114Sn', '112Sn', '142Ce', '140Ce', '138Ce', '136Ce', '133Cs', '55Mn',
                  '112Sn', '114Sn', '115Sn', '116Sn', '117Sn', '118Sn', '120Sn', '122Sn', '124Sn', '142Ce', '140Ce',
                  '138Ce', '136Ce', '113In', '115In', '41K', '40K', '39K', '174Hf', '180Hf', '58Fe', '82Se', '80Se',
                  '120Te', '78Se', '122Te', '124Te', '125Te', '126Te', '128Te', '77Se', '130Te', '76Se', '74Se',
                  '113In', '115In', '174Hf', '180Hf', '51V']

        res, res1, res2 = getmatch.get_matches(input_data)

        for i, x in enumerate(res[0]):
            self.assertEqual(x["element"], target_res[i], msg="Failed to get match for muonic xrays")

        # set database back to legacy in case it breaks something
        globals.muon_database = "legacy"
