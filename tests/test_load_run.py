import pytest
import numpy as np
from EVA.classes.app import get_app
from pytestqt.plugin import qapp

testdir = "test_data/"

# Run containing all data, run with one detector missing, invalid run
run_num_list = [2630, 3064, 0]

# Positional list - if file does not exist for a detector, add empty string
filenames_list = [
    ["ral02630.rooth2099.dat", "ral02630.rooth3099.dat", "ral02630.rooth4099.dat", "ral02630.rooth5099.dat", "", "", "", ""],
    ["ral03064.rooth2099.dat", "ral03064.rooth3099.dat", "ral03064.rooth4099.dat", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""]
]

class TestLoadRun:
    def manual_load(self, filename):
        if filename == "":
            return [], [] # return blank arrays if data is missing for the detector

        path = f"{testdir}{filename}"
        xdata, ydata = np.loadtxt(path, delimiter=" ", unpack=True)
        return xdata, ydata

    @pytest.mark.parametrize("run_num, filenames", list(zip(run_num_list, filenames_list)))
    def test_load_run(self, qapp, run_num, filenames):
        app = get_app()
        app.set_loaded_run(run_num)

        # Check that app.loaded_run is None if no detector data was loaded (invalid run number)
        if all([filename == "" for filename in filenames]):
            assert app.loaded_run is None, "Invalid run was specified but run is not None"
        else:
            for i, dataset in enumerate(app.loaded_run.raw):
                xdata, ydata = self.manual_load(filenames[i])
                print(dataset.x)
                print(dataset.y)
                assert np.array_equal(dataset.x, xdata) and np.array_equal(dataset.y, ydata)
