import os
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QTextBrowser,
    QWidget,
)

from PyQt6.QtCore import Qt
from EVA.util.path_handler import get_path

class ManualWindow(QWidget):
    def __init__(self, parent=None):
        super(ManualWindow, self).__init__(parent)
        self.setWindowTitle("Manual")
        self.setMinimumSize(700, 650)

        self.page = QTextBrowser(self)
        self.page.setOpenLinks(True)
        self.page.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.page)

        self.path = get_path("./src/EVA/resources/manual/manual.html")

        try:
            self.htmlstr = self.load_manual(self.path)
            self.page.setHtml(self.htmlstr)
        except FileNotFoundError:
            self.page.setText("Oops! Failed to load manual!")

    def load_manual(self, path):
        with open(path, "r", encoding="utf-8") as file:
            manual = "".join(file.readlines())

        file.close()
        return manual
