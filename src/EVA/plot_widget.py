import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QStyle
)

matplotlib.use("QtAgg")


class PlotWidget(FigureCanvasQTAgg):
    def __init__(self, fig=None, axs=None):
        super(FigureCanvasQTAgg, self).__init__(fig)
        self.axs = axs

    def update_plot(self, fig=None, axs=None):
        if fig is not None:
            self.figure = fig

        if axs is not None:
            self.axs = axs

        self.draw()
