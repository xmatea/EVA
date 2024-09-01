import numpy as np
import pytest
from PyQt6.QtWidgets import QWidget
from pytestqt.plugin import qtbot
from matplotlib.backend_bases import MouseEvent, MouseButton

from EVA.Plot_Window import PlotWindow
from EVA.loaddata import loaddata
from EVA.LoadDatabaseFile import loadDatabaseFile
from EVA.loadgamma import loadgamma


class TestPlotWindow:
    # will be executed once before tests are run
    @pytest.fixture(autouse=True)
    def setup(self):
        # loading database and sample data
        loadDatabaseFile()
        loadgamma()
        loaddata(2630)

    # simulate a mouse click event in figure at specified location
    def trigger_peak_click_event(self, window, xdata, ydata, button, ax):
        canvas = window.sc

        event = MouseEvent("", canvas, x=0, y=0, button=button)
        event.xdata = np.float64(xdata)
        event.ydata = np.float64(ydata)
        event.inaxes = ax

        # call on_click
        PlotWindow.on_click(window, event)

    def test_clickpeaks_gammas(self, qtbot):
        widget = QWidget()
        window = PlotWindow(widget)
        qtbot.addWidget(window)
        window.show()

        tests = [("44Sc", 189.9), ("93Zr", 65.6)]
        for test in tests:
            self.trigger_peak_click_event(window, xdata=test[1], ydata=0,
                                          ax=window.sc.axs[1], button=MouseButton.RIGHT)
            table_res = window.clickpeaks.table_gamma.item(0, 0).text()
            assert table_res == test[0], \
                "data displayed at position 0,0 in gamma table did not match the expected value"

    def test_clickpeaks_muon(self, qtbot):
        widget = QWidget()
        window = PlotWindow(widget)
        qtbot.addWidget(window)
        window.show()

        tests = [("Cs", 193.4), ("Ho", 911.7)]
        for test in tests:
            self.trigger_peak_click_event(window, xdata=test[1], ydata=0,
                                          ax=window.sc.axs[1], button=MouseButton.LEFT)
            table_res = window.clickpeaks.table_muon.item(0, 0).text()
            print(table_res)
            assert table_res == test[0], \
                "data displayed at position 0,0 in muon table on figure click did not match the expected value"
