import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

matplotlib.use("QtAgg")

class FigureCanvas(FigureCanvasQTAgg):
    def __init__(self, fig=None, axs=None):
        super().__init__(fig)
        self.axs = axs

class PlotWidget(QWidget):
    def __init__(self, fig=None, axs=None):
        super().__init__()

        self.canvas = FigureCanvas(fig=fig, axs=axs)
        self.layout = QVBoxLayout()

        if fig is None:
            self.navbar = None
        else:
            self.navbar = NavigationToolbar2QT(self.canvas)

        self.layout.addWidget(self.navbar, Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def update_plot(self, fig=None, axs=None):
        if axs is not None:
            self.canvas.axs = axs
            self.canvas.draw()

        if fig is not None:
            self.canvas.figure = fig

            """
            To ensure the navigation bar is re-linked to the new figure, and that the figure is resized to the fit the
            size of the widget, the navbar and canvas is removed from the layout, deleted, then re-initialised and
            re-added to widget.
            """

            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()

            if self.navbar is not None:
                self.layout.removeWidget(self.navbar)
                self.navbar.deleteLater()

            self.navbar = NavigationToolbar2QT(self.canvas)
            self.canvas = FigureCanvas(fig=self.canvas.figure, axs=self.canvas.axs)

            self.layout.addWidget(self.navbar)
            self.layout.addWidget(self.canvas)
