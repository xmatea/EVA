import numpy as np
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from pytestqt.plugin import qtbot


from EVA.MultiPlotWindow import MultiPlotWindow
from EVA import app

channels = {
    "GE1": "2099",
    "GE2": "3099",
    "GE3": "4099",
    "GE4": "5099"
}


TIME_DELAY = 500

class TestMultiPlotWindow:
    # this will run once before all other tests in the class
    @pytest.fixture(autouse=True)
    def setup(self):
        config = app.get_config()

        # set up test conditions
        config["general"]["normalisation"] = "none"
        config["GE1"]["show_plot"] = "yes"
        config["GE2"]["show_plot"] = "no"
        config["GE3"]["show_plot"] = "yes"
        config["GE4"]["show_plot"] = "no"

    # utility function to load data manually to compare with loaded data
    def get_data(self, run_list, detectors):
        data = []
        for i, run in enumerate(run_list):
            dets = []
            for detector in detectors:
                try:
                    file = f"./TestData/ral0{run}.rooth{channels[detector]}.dat"
                    dets.append(np.loadtxt(file, delimiter=" "))
                except FileNotFoundError:
                    pass
            data.append(dets)
        return data

    def test_multiplot_single_run(self, qtbot):
        widget = QWidget()
        window = MultiPlotWindow(widget)
        qtbot.addWidget(window)
        widget.show()
        qtbot.wait(TIME_DELAY)

        # test plotting a single run
        window.RunListTable.setItem(0, 0, QTableWidgetItem("3063"))
        qtbot.wait(TIME_DELAY)

        qtbot.mouseClick(window.plot_multi, Qt.MouseButton.LeftButton)
        qtbot.wait(int(TIME_DELAY*1.5))

        # load data manually and assert that plotted data matches the expected
        run_list = ["3063"]
        target_data = self.get_data(run_list, ["GE1", "GE3"])

        for i in range(len(run_list)):
            assert all(window.plot.canvas.axs[0].lines[i].get_ydata() == target_data[i][0][:, 1]), \
                "incorrect data was loaded"
            assert all(window.plot.canvas.axs[1].lines[i].get_ydata() == target_data[i][1][:, 1]), \
                "incorrect data was loaded"


    def test_multiplot_multiple_runs(self, qtbot):
        widget = QWidget()
        window = MultiPlotWindow(widget)
        qtbot.addWidget(window)
        widget.show()
        qtbot.wait(TIME_DELAY)

        # test plotting two non-consecutive runs
        window.RunListTable.setItem(0, 0, QTableWidgetItem("3063"))
        window.RunListTable.setItem(1, 0, QTableWidgetItem("3050"))
        qtbot.wait(TIME_DELAY)

        qtbot.mouseClick(window.plot_multi, Qt.MouseButton.LeftButton)
        qtbot.wait(int(TIME_DELAY*1.5))

        assert len(window.plot.canvas.axs[0].lines) == 2, "incorrect number of runs were plotted"
        assert len(window.plot.canvas.axs[1].lines) == 2, "incorrect number of runs were plotted"

        # load data manually and assert that plotted data matches the expected
        run_list = ["3063", "3050"]

        target_data = self.get_data(run_list, ["GE1", "GE3"])
        for i in range(len(run_list)):
            assert all(window.plot.canvas.axs[0].lines[i].get_ydata() == target_data[i][0][:, 1]), \
                "incorrect data was loaded"
            assert all(window.plot.canvas.axs[1].lines[i].get_ydata() == target_data[i][1][:, 1]), \
                "incorrect data was loaded"

    def test_multiplot_with_simple_step(self, qtbot):
        widget = QWidget()
        window = MultiPlotWindow(widget)
        qtbot.addWidget(window)
        widget.show()
        qtbot.wait(TIME_DELAY)

        window.RunListTable.setItem(0, 0, QTableWidgetItem("3063"))  # start
        window.RunListTable.setItem(0, 1, QTableWidgetItem("3068"))  # stop
        window.RunListTable.setItem(0, 2, QTableWidgetItem("1"))  # step

        window.RunListTable.setItem(1, 0, QTableWidgetItem("3070"))  # start
        window.RunListTable.setItem(1, 1, QTableWidgetItem("3074"))  # stop
        window.RunListTable.setItem(1, 2, QTableWidgetItem("1"))  # step
        qtbot.wait(TIME_DELAY)

        # click button to load multi run
        qtbot.mouseClick(window.plot_multi, Qt.MouseButton.LeftButton)
        qtbot.wait(int(TIME_DELAY*1.5))
        print(window.plot.canvas.axs[0].lines)
        print(window.plot.canvas.axs[1].lines)

        # check that both subplots contain 11 lines: 3063-3074 excluding 3069 because it is missing from testdata
        assert len(window.plot.canvas.axs[0].lines) == 11, \
            "incorrect number of runs were plotted"
        assert len(window.plot.canvas.axs[1].lines) == 11, \
            "incorrect number of runs were plotted"

        # load data manually and assert that plotted data matches the expected
        run_list = ["3063", "3064", "3065", "3066", "3067", "3068", "3070", "3071", "3072", "3073", "3074"]

        target_data = self.get_data(run_list, ["GE1", "GE3"])


        for i in range(len(run_list)):
            assert all(window.plot.canvas.axs[0].lines[i].get_ydata() == target_data[i][0][:, 1]), \
                "incorrect data was loaded"
            assert all(window.plot.canvas.axs[1].lines[i].get_ydata() == target_data[i][1][:, 1]), \
                "incorrect data was loaded"

    def test_multiplot_with_step_overflow(self, qtbot):
        widget = QWidget()
        window = MultiPlotWindow(widget)
        qtbot.addWidget(window)
        widget.show()
        qtbot.wait(TIME_DELAY)

        window.RunListTable.setItem(0, 0, QTableWidgetItem("3063"))  # start
        window.RunListTable.setItem(0, 1, QTableWidgetItem("3068"))  # stop
        window.RunListTable.setItem(0, 2, QTableWidgetItem("2"))  # step
        qtbot.wait(TIME_DELAY)

        # click button to load multi run
        qtbot.mouseClick(window.plot_multi, Qt.MouseButton.LeftButton)
        qtbot.wait(int(TIME_DELAY*1.5))

        # check that both axes contain 3 lines (3063, 3065, 3067)
        assert len(window.plot.canvas.axs[0].lines) == 3, \
            "incorrect number of runs were plotted"
        assert len(window.plot.canvas.axs[1].lines) == 3, \
            "incorrect number of runs were plotted"

        # load data manually and assert that plotted data matches the expected
        run_list = ["3063", "3065", "3067"]

        target_data = self.get_data(run_list, ["GE1", "GE3"])
        for i in range(len(run_list)):
            assert all(window.plot.canvas.axs[0].lines[i].get_ydata() == target_data[i][0][:, 1]), \
                "incorrect data was loaded"
            assert all(window.plot.canvas.axs[1].lines[i].get_ydata() == target_data[i][1][:, 1]), \
                "incorrect data was loaded"

    def test_multiplot_no_runs_entered(self, qtbot):
        widget = QWidget()
        window = MultiPlotWindow(widget)
        qtbot.addWidget(window)
        widget.show()
        qtbot.wait(TIME_DELAY)

        # click load without any data
        qtbot.mouseClick(window.plot_multi, Qt.MouseButton.LeftButton)
        qtbot.wait(int(TIME_DELAY*1.5))

        assert window.plot.canvas.axs is None, "incorrect number of runs were loaded"

    def test_multiplot_invalid_run_entered(self, qtbot):
        widget = QWidget()
        window = MultiPlotWindow(widget)
        qtbot.addWidget(window)
        widget.show()
        qtbot.wait(TIME_DELAY)

        # try to load invalid run number 'A'
        window.RunListTable.setItem(0, 0, QTableWidgetItem("A"))
        qtbot.wait(TIME_DELAY)
        qtbot.mouseClick(window.plot_multi, Qt.MouseButton.LeftButton)
        qtbot.wait(int(TIME_DELAY*1.5))

        assert window.plot.canvas.axs is None, "incorrect number of runs were loaded"
