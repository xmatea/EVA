import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

matplotlib.use("QtAgg")

"""
    PlotWidget inherits from FigureCanvasQTAgg which allows it to be embedded into Qt, but it has limited functionality.
    To make it easier to work, it also inherits from QWidget.
"""


class PlotWidget(FigureCanvasQTAgg, QWidget):
    def __init__(self, fig=None, axs=None, plt=None, *args, **kwargs):
        super(FigureCanvasQTAgg, self).__init__(fig)
        super(QWidget).__init__(*args, **kwargs)

        self.fig = fig
        self.axs = axs
        self.plt = plt

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def update_plot(self, plt=None, axs=None, fig=None):
        if fig is not None:
            self.fig = fig

        if axs is not None:
            self.axs = axs

        if plt is not None:
            self.plt = plt

        self.draw()
