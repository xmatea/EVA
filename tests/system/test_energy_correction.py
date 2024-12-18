import numpy as np
from EVA.core.app import get_app
import pytest
from pytestqt.plugin import qapp

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
    def test_energy_correction(self, qapp, e_corr_which):
        app = get_app()
        app.set_loaded_run(2630)
        run = get_app().loaded_run
        app.reset()

        # energy correction done by EVA
        run.set_energy_correction(params, e_corr_which)

        for i, dataset in enumerate(run.raw):
            if dataset.detector in e_corr_which:
                corrected = run.raw[i].x * params[i][0] + params[i][1]
            else:
                corrected = run.raw[i].x

            assert np.array_equal(corrected, run.data[i].x), (f"energy correction failed when correcting "
                                                                   f"{" and ".join(e_corr_which)}")