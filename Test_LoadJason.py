import unittest
import LoadDatabaseFile as ldf

import globals




class LoadJason(unittest.TestCase):
    def test_loadjason(self):
        ldf.loadDatabaseFile()
        self.assertEqual(len(globals.peak_data), 3, 'Failed  loadjason')

