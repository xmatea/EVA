import numpy as np
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QErrorMessage
from pytestqt.plugin import qtbot
from matplotlib.backend_bases import MouseEvent, MouseButton

from EVA.MultiPlotWindow import MultiPlotWindow
from EVA.loaddata import loaddata
from EVA.LoadDatabaseFile import loadDatabaseFile
from EVA.loadgamma import loadgamma
import Tests.GUI.test_util_gui as util


class TestMultiPlotWindow:
    @pytest.fixture(autouse=True)
    def setup(self):
        # loading database and sample data
        loadDatabaseFile()
        loadgamma()
        loaddata(2630)

    def test_multiplot_single_run(self, qtbot):
        widget = QWidget()
        window = MultiPlotWindow(widget)
        qtbot.addWidget(window)

        # test plotting a single run
        window.RunListTable.setItem(0, 0, QTableWidgetItem("3063"))  # start
        qtbot.mouseClick(window.plot_multi, Qt.MouseButton.LeftButton)

        print(window.plot.axs[0].lines)
        print(window.plot.axs[1].lines)

        assert len(window.plot.axs[0].lines) == 1, "incorrect number of runs were plotted"
        assert len(window.plot.axs[1].lines) == 1, "incorrect number of runs were plotted"

        # test plotting multiple with a start / stop

    def test_multiplot_multiple_runs(self, qtbot):
        widget = QWidget()
        window = MultiPlotWindow(widget)
        qtbot.addWidget(window)

        # test plotting a single run
        window.RunListTable.setItem(0, 0, QTableWidgetItem("3063"))
        window.RunListTable.setItem(1, 0, QTableWidgetItem("3050"))
        qtbot.mouseClick(window.plot_multi, Qt.MouseButton.LeftButton)

        print(window.plot.axs[0].lines)
        print(window.plot.axs[1].lines)

        assert len(window.plot.axs[0].lines) == 2, "incorrect number of runs were plotted"
        assert len(window.plot.axs[1].lines) == 2, "incorrect number of runs were plotted"

    def test_multiplot_with_simple_step(self, qtbot):
        widget = QWidget()
        window = MultiPlotWindow(widget)
        qtbot.addWidget(window)

        window.RunListTable.setItem(0, 0, QTableWidgetItem("3063"))  # start
        window.RunListTable.setItem(0, 1, QTableWidgetItem("3070"))  # stop
        window.RunListTable.setItem(0, 2, QTableWidgetItem("1"))  # step

        # click button to load multi run
        qtbot.mouseClick(window.plot_multi, Qt.MouseButton.LeftButton)
        print(window.plot.axs[0].lines)
        print(window.plot.axs[1].lines)

        # check that both axes contain 8 lines
        assert len(window.plot.axs[0].lines) == 8, \
            "incorrect number of runs were plotted"
        assert len(window.plot.axs[1].lines) == 8, \
            "incorrect number of runs were plotted"
    def test_multiplot_with_step_overflow(self, qtbot):
        widget = QWidget()
        window = MultiPlotWindow(widget)
        qtbot.addWidget(window)

        window.RunListTable.setItem(0, 0, QTableWidgetItem("3063"))  # start
        window.RunListTable.setItem(0, 1, QTableWidgetItem("3070"))  # stop
        window.RunListTable.setItem(0, 2, QTableWidgetItem("2"))  # step

        # click button to load multi run
        qtbot.mouseClick(window.plot_multi, Qt.MouseButton.LeftButton)
        print(window.plot.axs[0].lines)
        print(window.plot.axs[1].lines)

        # check that both axes contain 4 lines (3063, 3065, 3067, 3069)
        assert len(window.plot.axs[0].lines) == 4, \
            "incorrect number of runs were plotted"
        assert len(window.plot.axs[1].lines) == 4, \
            "incorrect number of runs were plotted"

    def test_multiplot_no_runs_entered(self, qtbot):
        widget = QWidget()
        window = MultiPlotWindow(widget)
        qtbot.addWidget(window)

        # click load without any data
        qtbot.mouseClick(window.plot_multi, Qt.MouseButton.LeftButton)
        print(window.plot.axs[0].lines)

        assert len(window.plot.axs[0].lines) == 0 and len(window.plot.axs[1].lines) == 0, \
            "incorrect number of runs were loaded"

    def test_multiplot_invalid_run_entered(self, qtbot):
        widget = QWidget()
        window = MultiPlotWindow(widget)
        qtbot.addWidget(window)

        window.RunListTable.setItem(0, 0, QTableWidgetItem("3063"))  # start
        window.RunListTable.setItem(0, 1, QTableWidgetItem("3070"))  # stop
        window.RunListTable.setItem(0, 2, QTableWidgetItem("1"))  # step

        qtbot.mouseClick(window.plot_multi, Qt.MouseButton.LeftButton)

        # try to load invalid run number A
        window.RunListTable.setItem(0, 0, QTableWidgetItem("A"))
        qtbot.mouseClick(window.plot_multi, Qt.MouseButton.LeftButton)

        print(window.plot.axs[0].lines)

        assert len(window.plot.axs[0].lines) == 0 and len(window.plot.axs[1].lines) == 0, \
            "incorrect number of runs were loaded"
