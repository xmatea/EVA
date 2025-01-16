import logging
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from EVA.widgets.srim.trim_model import TrimModel
from EVA.widgets.srim.trim_presenter import TrimPresenter
from EVA.widgets.srim.trim_view import TrimView

logger = logging.getLogger(__name__)

class TrimWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("TRIM Simulations")
        self.setMinimumSize(1100, 600)
        self.view = TrimView()
        self.model = TrimModel()
        self.presenter = TrimPresenter(self.view, self.model)

        layout = QHBoxLayout()
        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)