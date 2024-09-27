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
import Tests.GUI.test_util_gui as util

class TestPeakFitWindow:
    # TODO add tests after making peakfit work for any data
    @pytest.fixture(autouse=True)
    def setup(self):
        # loading database and sample data
        loadDatabaseFile()
        loadgamma()
        loaddata(2630)

    def test_peak_fit_plotting_on_button_click(self, qtbot):
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

        data_ax0 = window.sc.axs[0].collections[1].get_offsets().data
        data_ax1 = window.sc.axs[1].collections[1].get_offsets().data

        # check if the expected points were scattered on the figure
        assert all([elem[0] == peaks_ax0[i][0] for i, elem in enumerate(data_ax0)]), \
            "Marker positions on figure after peakfit did not match expected results"
        assert all([elem[0] == peaks_ax1[i][0] for i, elem in enumerate(data_ax1)]), \
            "Marker positions on figure after peakfit did not match expected results"
