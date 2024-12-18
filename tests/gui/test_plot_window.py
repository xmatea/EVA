import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from pytestqt.plugin import qtbot
from matplotlib.backend_bases import MouseButton

from EVA.widgets.plot_analysis.plot_window import PlotWindow
from EVA.core.app import get_app, get_config

import tests.gui.test_util_gui as util

muon_plot_lines_tests = [[551.8, 48], [189.9, 30], [44.4, 22]]
gamma_plot_lines_tests = [[189.9, 124], [551.8, 626], [44.4, 198]]

class TestPlotWindow:
    # will be executed once before tests are run
    @pytest.fixture(autouse=True)
    def setup(self):
        # loading database and sample data
        app = get_app()
        app.set_loaded_run(2630)

    # test if the expected data is displayed in gamma table when clicking a specific peak in the figure
    @pytest.mark.parametrize("peak, position", [("44Sc", 189.9), ("93Zr", 65.6)])
    def test_clickpeaks_gammas(self, qtbot, peak, position):
        widget = QWidget()
        window = PlotWindow(widget)
        qtbot.addWidget(window)
        widget.showMaximized()
        qtbot.wait(500)

        event = util.trigger_figure_click_event(window.plot.canvas, xdata=position, ydata=0,
                                      ax=window.plot.canvas.axs[1], button=MouseButton.RIGHT)
        # call on_click
        PlotWindow.on_click(window, event)
        qtbot.wait(500)

        table_res = window.clickpeaks.table_gamma.item(0, 0).text()
        get_app().reset()

        assert table_res is not None, "gamma table empty on click"
        assert table_res == peak, \
            "data displayed at position 0,0 in gamma table did not match the expected value"

    # test if the expected data is displayed in muon table when clicking a specific peak in the figure
    @pytest.mark.parametrize("peak, position", [("Cl", 193.4), ("Ti", 932.0)])
    def test_clickpeaks_muon(self, qtbot, peak, position):
        widget = QWidget()
        window = PlotWindow(widget)
        qtbot.addWidget(window)
        widget.showMaximized()
        qtbot.wait(500)

        # simulate click event
        event = util.trigger_figure_click_event(window.plot.canvas, xdata=position, ydata=0,
                                      ax=window.plot.canvas.axs[1], button=MouseButton.LEFT)
        # call on_click
        PlotWindow.on_click(window, event)
        qtbot.wait(500)

        table_res = window.clickpeaks.table_muon.item(0, 0).text()
        get_app().reset()

        assert table_res == peak, \
            "data displayed at position 0,0 in muon table on figure click did not match the expected value"

    @pytest.mark.parametrize("tests", gamma_plot_lines_tests)
    def test_plot_and_remove_lines_gammas(self, qtbot, tests):
        widget = QWidget()
        window = PlotWindow(widget)
        qtbot.addWidget(window)
        widget.showMaximized()
        qtbot.wait(500)

        # first element in tuple is which energy to search, second element in tuple is how many lines will be plotted
        # when clicking the first element in the table after searching that energy.

        # simulate click event
        event = util.trigger_figure_click_event(window.plot.canvas, xdata=tests[0], ydata=0,
                                                ax=window.plot.canvas.axs[1], button=MouseButton.RIGHT)

        PlotWindow.on_click(window, event)
        qtbot.wait(250)

        # Click on source in gamma table to plot vertical lines on figure
        gamma_table_item = window.clickpeaks.table_gamma.item(0, 0)
        gamma_table_rect = window.clickpeaks.table_gamma.visualItemRect(gamma_table_item)

        qtbot.mouseClick(window.clickpeaks.table_gamma.viewport(), Qt.MouseButton.LeftButton,
                     pos=gamma_table_rect.center())
        qtbot.wait(250)

        # check that lines were plotted

        assert len(list(window.plot.canvas.axs[1].lines)) > 1, "no lines were plotted"
        assert len(list(window.plot.canvas.axs[1].lines)) == tests[1], "not all lines were plotted"

        # Click on source in remove plot lines table to remove vertical line
        remove_table_item = window.clickpeaks.table_plotted_lines.item(0, 1)
        remove_table_rect = window.clickpeaks.table_plotted_lines.visualItemRect(remove_table_item)

        qtbot.mouseClick(window.clickpeaks.table_plotted_lines.viewport(), Qt.MouseButton.LeftButton,
                     pos=remove_table_rect.center())
        qtbot.wait(500)

        get_app().reset()
        assert len(list(window.plot.canvas.axs[1].lines)) == 1, "Failed to remove all plot lines"

    @pytest.mark.parametrize("tests", muon_plot_lines_tests)
    def test_plot_and_remove_lines_muonic_xrays(self, qtbot, tests):
        widget = QWidget()
        window = PlotWindow(widget)
        qtbot.addWidget(window)
        widget.showMaximized()
        qtbot.wait(500)

        # first element in tuple is which energy to search, second element in tuple is how many lines will be plotted
        # when clicking the first element in the table after searching that energy.
        table = window.clickpeaks.table_muon

        # simulate left click on figure
        event = util.trigger_figure_click_event(window.plot.canvas, xdata=tests[0], ydata=0,
                                                ax=window.plot.canvas.axs[1], button=MouseButton.LEFT)

        PlotWindow.on_click(window, event)
        qtbot.wait(250)
        # Click on source in table to plot vertical lines on figure
        table_item = table.item(0, 0)
        table_rect = table.visualItemRect(table_item)
        qtbot.mouseClick(table.viewport(), Qt.MouseButton.LeftButton,
                         pos=table_rect.center())
        qtbot.wait(250)

        # check that lines were plotted
        print(f"number of lines plotted for energy {tests[0]} - {len(list(window.plot.canvas.axs[1].lines))}")
        assert len(list(window.plot.canvas.axs[1].lines)) > 1, "no lines were plotted"
        assert len(list(window.plot.canvas.axs[1].lines)) == tests[1], "not all lines were plotted"

        # Click on source in remove plot lines table to remove vertical line
        remove_table_item = window.clickpeaks.table_plotted_lines.item(0, 0)
        remove_table_rect = window.clickpeaks.table_plotted_lines.visualItemRect(remove_table_item)

        qtbot.mouseClick(window.clickpeaks.table_plotted_lines.viewport(), Qt.MouseButton.LeftButton,
                         pos=remove_table_rect.center())
        qtbot.wait(250)

        get_app().reset()
        assert len(list(window.plot.canvas.axs[1].lines)) == 1, "Failed to remove all plot lines"

    # TODO: Make this work properly
    """
    def test_find_peaks_plotting_on_button_click(self, qtbot):
        config = get_config()
        app = get_app()
        app.use_legacy_muon_db()

        config["GE1"]["show_plot"] = "yes"
        config["GE2"]["show_plot"] = "no"
        config["GE3"]["show_plot"] = "yes"
        config["GE4"]["show_plot"] = "no"

        peaks_ax0 = [(47.5, 116),
                (66.5, 652),
                (72.5, 151),
                (75.5, 201),
                (84.5, 134),
                (102.5, 203),
                (121.5, 312),
                (131.5, 309),
                (146.5, 135),
                (179.5, 101),
                (190.5, 575),
                (199.5,  88),
                (202.5,  92),
                (252.5,  70),
                (281.5,  65),
                (286.5,  97),
                (364.5,  65),
                (395.5,  51),
                (405.5,  47),
                (519.5,  59),
                (596.5,  44),
                (643.5,  43),
                (653.5,  40),
                (931.5, 195),
                (1189.5,  27)]

        peaks_ax1 = [(71.1875, 25), (96.6875, 83), (120.938, 97)]

        widget = QWidget()
        window = PlotWindow(widget)
        qtbot.addWidget(window)

        # click on peak fitting button - ONLY TESTS SCIPY FIND PEAKS METHOD
        qtbot.mouseClick(window.findpeaks.find_peaks_button, Qt.MouseButton.LeftButton)

        data_ax0 = window.plot.canvas.axs[0].collections[1].get_offsets().data
        data_ax1 = window.plot.canvas.axs[1].collections[1].get_offsets().data

        print(data_ax0)

        # check if the expected points were scattered on the figure
        assert len(peaks_ax0) == len(data_ax0)
        assert len(peaks_ax1) == len(data_ax1)
        assert all([elem[0] == peaks_ax0[i][0] for i, elem in enumerate(data_ax0)]), \
            "Marker positions on figure after peakfit did not match expected results"
        assert all([elem[0] == peaks_ax1[i][0] for i, elem in enumerate(data_ax1)]), \
            "Marker positions on figure after peakfit did not match expected results"
    """