import numpy as np

from EVA import Energy_Corrections
from EVA.app import get_app, get_config
import pytest
from EVA.loaddata import load_run

params = {
    # m, c
    "GE1": [2.0, 1],
    "GE2": [2.13, 1.12],
    "GE3": [2.02, 1.01],
    "GE4": [2.034, 1.034]
}

class TestEnergyCorrection:
    @pytest.fixture(autouse=True)
    def setup(self, qtbot):
        # loading database and sample data
        app = get_app()

        run_num = 2630
        app.config["general"]["run_num"] = str(run_num)
        data, flags = load_run(run_num)

        print([dataset.x[100] for dataset in data.raw])
        app.loaded_run = data

    def energy_correction(self, run, target_detectors, m, c):
        config = get_config()
        detectors = config["general"]["all_detectors"].split(" ")

        # Toggle energy correction only for target detectors
        for detector in detectors:
            if detector in target_detectors:
                config[detector]["use_energy_correction"] = "yes"
            else:
                config[detector]["use_energy_correction"] = "no"

        for i, target_detector in enumerate(target_detectors):
            # Set energy correction parameters in config
            config[target_detector]["e_corr_gradient"] = str(m[i])
            config[target_detector]["e_corr_offset"] = str(c[i])

        # Do energy correction on raw data
        run.raw_e_corr = Energy_Corrections.Energy_Corrections(run.raw)

        return run


    def reference_energy_correction(self, dataset, m, c):
        # Manual energy calibration
        return dataset.x * m + c

    def test_energy_correction_GE1_only(self):
        # Load run from file
        run = get_app().loaded_run

        # Create test parameters
        m = [2]
        c = [1]

        # Manually apply energy calibration to run
        dataset = run.raw[0]  # Get Dataset on index 0 corresponding to GE1
        expected = self.reference_energy_correction(dataset, m, c)

        # Do energy correction on run
        run = self.energy_correction(run=run, target_detectors=["GE1"], m=m, c=c)
        result = run.raw_e_corr[0].x

        assert np.array_equal(expected, result), "Energy correction failed for GE1"

    def test_energy_correction_GE2_only(self):
        # Load run from file
        run = get_app().loaded_run

        # Create test parameters
        m = [3]
        c = [2]

        # Manually apply energy calibration to run
        dataset = run.raw[1]  # Get Dataset on index 1 corresponding to GE2
        expected = self.reference_energy_correction(dataset, m, c)

        # Do energy correction on run
        run = self.energy_correction(run=run, target_detectors=["GE2"], m=m, c=c)
        result = run.raw_e_corr[1].x

        assert np.array_equal(expected, result), "Energy correction failed for GE2"

    def test_energy_correction_GE3_only(self):
        # Load run from file
        run = get_app().loaded_run

        # Create test parameters
        m = [1.5]
        c = [2]

        # Manually apply energy calibration to run
        dataset = run.raw[2]  # Get Dataset on index 2 corresponding to GE3
        expected = self.reference_energy_correction(dataset, m, c)

        # Do energy correction on run
        run = self.energy_correction(run=run, target_detectors=["GE3"], m=m, c=c)
        result = run.raw_e_corr[2].x

        assert np.array_equal(expected, result), "Energy correction failed for GE3"

    def test_energy_correction_GE4_only(self):
        # Load run from file
        run = get_app().loaded_run

        # Create test parameters
        m = [4]
        c = [1.5]

        # Manually apply energy calibration to run
        dataset = run.raw[3]  # Get Dataset on index 3 corresponding to GE4
        expected = self.reference_energy_correction(dataset, m, c)

        # Do energy correction on run
        run = self.energy_correction(run=run, target_detectors=["GE4"], m=m, c=c)
        result = run.raw_e_corr[3].x

        assert np.array_equal(expected, result), "Energy correction failed for GE4"

    def test_energy_correction_all_detectors(self):
        # Load run from file
        run = get_app().loaded_run

        # Create test parameters
        m = [2, 3, 4, 5]
        c = [1, 2, 3, 4]

        # Manually apply energy calibration to each dataset
        expected = []
        for i in range(len(m)):
            dataset = run.raw[i]
            expected.append(self.reference_energy_correction(dataset, m[i], c[i]))

        # Do energy correction on run
        run = self.energy_correction(run=run, target_detectors=["GE1", "GE2", "GE3", "GE4"], m=m, c=c)

        # assert if energy correction is equal to manual correction for each dataset
        is_equal = [np.array_equal(dataset.x, expected[i]) for i, dataset in enumerate(run.raw_e_corr)]

        assert all(is_equal), "Energy correction failed for all detectors"