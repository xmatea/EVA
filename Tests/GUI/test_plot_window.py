import numpy as np
import pytest
from PyQt6.QtCore import Qt
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

    # test if the expected data is displayed in gamma table when clicking a specific peak in the figure
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

    # test if the expected data is displayed in muon table when clicking a specific peak in the figure
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


    def test_plot_and_remove_lines_gammas(self, qtbot):
        widget = QWidget()
        window = PlotWindow(widget)
        qtbot.addWidget(window)
        widget.showMaximized()

        qtbot.wait(50)

        # first element in tuple is which energy to search, second element in tuple is how many lines will be plotted
        # when clicking the first element in the table after searching that energy.
        tests = [(189.9, 124), (551.8, 626), (44.4, 198)]

        for test in tests:
            # click on
            self.trigger_peak_click_event(window, xdata=test[0], ydata=0,
                                          ax=window.sc.axs[1], button=MouseButton.RIGHT)
            # Click on source in gamma table to plot vertical lines on figure
            gamma_table_item = window.clickpeaks.table_gamma.item(0, 0)
            gamma_table_rect = window.clickpeaks.table_gamma.visualItemRect(gamma_table_item)

            qtbot.mouseClick(window.clickpeaks.table_gamma.viewport(), Qt.MouseButton.LeftButton,
                             pos=gamma_table_rect.center())

            # check that lines were plotted
            print(window.sc.axs[1].lines)
            assert len(list(window.sc.axs[1].lines)) > 1, "no lines were plotted"
            assert len(list(window.sc.axs[1].lines)) == test[1], "not all lines were plotted"

            qtbot.wait(50)

            # Click on source in remove plot lines table to remove vertical line
            remove_table_item = window.clickpeaks.table_plotted_lines.item(0, 1)
            remove_table_rect = window.clickpeaks.table_plotted_lines.visualItemRect(remove_table_item)

            qtbot.mouseClick(window.clickpeaks.table_plotted_lines.viewport(), Qt.MouseButton.LeftButton,
                             pos=remove_table_rect.center())
            qtbot.wait(50)

            assert len(list(window.sc.axs[1].lines)) == 1, "Failed to remove all plot lines"

    def test_plot_and_remove_lines_muonic_xrays(self, qtbot):
        widget = QWidget()
        window = PlotWindow(widget)
        qtbot.addWidget(window)
        widget.showMaximized()

        qtbot.wait(50)

        # first element in tuple is which energy to search, second element in tuple is how many lines will be plotted
        # when clicking the first element in the table after searching that energy.
        tests = [(189.9, 60), (551.8, 41), (44.4, 29)]
        table = window.clickpeaks.table_muon

        for test in tests:
            # simulate left click on figure
            self.trigger_peak_click_event(window, xdata=test[0], ydata=0,
                                          ax=window.sc.axs[1], button=MouseButton.LEFT)

            # Click on source in table to plot vertical lines on figure
            table_item = table.item(0, 0)
            table_rect = table.visualItemRect(table_item)
            qtbot.mouseClick(table.viewport(), Qt.MouseButton.LeftButton,
                             pos=table_rect.center())

            # check that lines were plotted
            print("number of lines", len(window.sc.axs[1].lines))
            assert len(list(window.sc.axs[1].lines)) > 1, "no lines were plotted"
            assert len(list(window.sc.axs[1].lines)) == test[1], "not all lines were plotted"

            qtbot.wait(50)

            # Click on source in remove plot lines table to remove vertical line
            remove_table_item = window.clickpeaks.table_plotted_lines.item(0, 0)
            remove_table_rect = window.clickpeaks.table_plotted_lines.visualItemRect(remove_table_item)

            qtbot.mouseClick(window.clickpeaks.table_plotted_lines.viewport(), Qt.MouseButton.LeftButton,
                             pos=remove_table_rect.center())

            qtbot.wait(50)

            assert len(list(window.sc.axs[1].lines)) == 1, "Failed to remove all plot lines"
