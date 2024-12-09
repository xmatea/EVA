from PyQt6.QtWidgets import QWidget, QHBoxLayout

from EVA.widgets.muonic_xray_simulation.model_spectra_presenter import ModelSpectraPresenter
from EVA.widgets.muonic_xray_simulation.model_spectra_view import ModelSpectraView


class ModelSpectraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.view = ModelSpectraView()
        self.presenter = ModelSpectraPresenter(self.view)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)