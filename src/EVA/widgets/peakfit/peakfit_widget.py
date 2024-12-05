from PyQt6.QtWidgets import QWidget, QHBoxLayout

from EVA.widgets.peakfit.peakfit_presenter import PeakFitPresenter
from EVA.widgets.peakfit.peakfit_view import PeakFitView


class PeakFitWidget(QWidget):
    def __init__(self, detector):
        """ Assemble the view and the presenter for the PeakFit widget."""
        super().__init__()
        self.view = PeakFitView(self, detector)
        self.presenter = PeakFitPresenter(self.view)


        # Using a layout for this is excessive, but for some reason just parenting the view doesn't
        # force the PlotWidget to resize to fit the window, while using a layout does...?

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
