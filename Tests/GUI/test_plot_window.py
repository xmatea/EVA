import numpy as np
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from pytestqt.plugin import qtbot
from matplotlib.backend_bases import MouseButton

from EVA.Plot_Window import PlotWindow
from EVA.loaddata import loaddata
from EVA.LoadDatabaseFile import loadDatabaseFile
from EVA.loadgamma import loadgamma

import Tests.GUI.test_util_gui as util


class TestPlotWindow:
    # will be executed once before tests are run
    @pytest.fixture(autouse=True)
    def setup(self):
        # loading database and sample data
        loadDatabaseFile()
        loadgamma()
        loaddata(2630)

    # test if the expected data is displayed in gamma table when clicking a specific peak in the figure
    def test_clickpeaks_gammas(self, qtbot):
        widget = QWidget()
        window = PlotWindow(widget)
        qtbot.addWidget(window)
        window.show()

        tests = [("44Sc", 189.9), ("93Zr", 65.6)]
        for test in tests:
            event = util.trigger_figure_click_event(window.sc, xdata=test[1], ydata=0,
                                          ax=window.sc.axs[1], button=MouseButton.RIGHT)
            # call on_click
            PlotWindow.on_click(window, event)

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
            # simulate click event
            event = util.trigger_figure_click_event(window.sc, xdata=test[1], ydata=0,
                                          ax=window.sc.axs[1], button=MouseButton.LEFT)
            # call on_click
            PlotWindow.on_click(window, event)

            table_res = window.clickpeaks.table_muon.item(0, 0).text()
            print(table_res)
            assert table_res == test[0], \
                "data displayed at position 0,0 in muon table on figure click did not match the expected value"


    def test_plot_and_remove_lines(self, qtbot):
        widget = QWidget()
        window = PlotWindow(widget)
        qtbot.addWidget(window)
        #widget.showMaximized()

        #qtbot.wait(1000)
        print(window.sc.axs[1].lines)

        # simulate click event
        event = util.trigger_figure_click_event(window.sc, xdata=189.9, ydata=0,
                                      ax=window.sc.axs[1], button=MouseButton.RIGHT)

        PlotWindow.on_click(window, event)

        # Click on source in gamma table to plot vertical lines on figure
        gamma_table_item = window.clickpeaks.table_gamma.item(0, 0)
        gamma_table_rect = window.clickpeaks.table_gamma.visualItemRect(gamma_table_item)

        qtbot.mouseClick(window.clickpeaks.table_gamma.viewport(), Qt.MouseButton.LeftButton,
                         pos=gamma_table_rect.center())

        # check that lines were plotted
        print(window.sc.axs[1].lines)
        assert len(list(window.sc.axs[1].lines)) > 1, "no lines were plotted"
        assert len(list(window.sc.axs[1].lines)) == 124, "not all lines were plotted"

        #qtbot.wait(1000)

        # Click on source in remove plot lines table to remove vertical line
        remove_table_item = window.clickpeaks.table_plotted_lines.item(0, 1)
        remove_table_rect = window.clickpeaks.table_plotted_lines.visualItemRect(remove_table_item)

        qtbot.mouseClick(window.clickpeaks.table_plotted_lines.viewport(), Qt.MouseButton.LeftButton,
                         pos=remove_table_rect.center())

        #qtbot.wait(1000)

        # Check that all lines were hidden (except for first line which is the plotted data)
        all_hidden = True
        for line in window.sc.axs[1].lines[1:]:
            if line._visible:
                all_hidden = False

        assert all_hidden, "Failed to remove all plot lines"
