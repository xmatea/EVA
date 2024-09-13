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

class TestPeakFitWindow:
    # TODO add tests after making peakfit work for any data
    def test_table_data_on_plot_click(self):
        pass

    def test_peak_fit_plotting_on_button_click(self):
        pass