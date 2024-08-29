import unittest
from EVA import globals, LoadDatabaseFile as ldf


class LoadJason(unittest.TestCase):
    def test_loadjason(self):
        ldf.loadDatabaseFile()
        self.assertEqual(len(globals.peak_data), 3, 'Failed  loadjason')

