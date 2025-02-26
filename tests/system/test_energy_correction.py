import numpy as np
from EVA.core.app import get_app
import pytest
from pytestqt.plugin import qapp

from EVA.core.data_loading import load_data
from EVA.core.app import get_config

params = [[2.0, 1],
            [2.13, 1.12],
            [2.02, 1.01],
            [2.034, 1.034]]

# Which detectors to use for each test
test_detectors = [["GE1"],
                        ["GE2"],
                        ["GE3"],
                        ["GE4"],
                        ["GE1", "GE2", "GE3", "GE4"],
                        ["GE1", "GE3"],
                        ["GE2", "GE4"]]

class TestEnergyCorrection:
    @pytest.mark.parametrize("e_corr_which", test_detectors)
    def test_energy_correction(self, e_corr_which, qapp):
        run, _ = load_data.load_run("2630", get_config())
        get_app().reset()

        # energy correction done by EVA
        run.set_energy_correction(params, e_corr_which)

        # Manual energy correction
        raw = run.get_raw() # get a copy of raw data

        for i, dataset in enumerate(raw):
            if dataset.detector in e_corr_which:
                corrected = raw[i].x * params[i][0] + params[i][1]
            else:
                corrected = raw[i].x

            assert np.array_equal(corrected, run.data[i].x), (f"energy correction failed when correcting "
                                                                   f"{" and ".join(e_corr_which)}")