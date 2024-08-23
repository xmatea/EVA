from PyQt6.QtWidgets import (
    QGridLayout,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QTextBrowser,
    QWidget,
    QSizePolicy
)

from PyQt6.QtCore import Qt, QSize

import globals

class ManualWindow(QWidget):
    def __init__(self, parent=None):
        super(ManualWindow, self).__init__(parent)

        if globals.scn_res == 1:
            self.resize(1200, 1100)
            self.setMinimumSize(1200, 1100)
        elif globals.scn_res == 2:
            self.resize(800, 900)
            self.setMinimumSize(800, 1000)
        else:
            self.resize(1200, 1100)
            self.setMinimumSize(1200, 1100)

        self.setWindowTitle("Manual")
        self.setMaximumHeight(1000)

        self.htmlstr = self.loadManual("manual.html")
        self.page = QTextBrowser(self)
        self.page.setOpenLinks(True)

        self.page.setHtml(self.htmlstr)
        self.page.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.page)
        self.show()

    def loadManual(self, path):
        with open(path, "r") as file:
            manual = "".join(file.readlines())

        file.close()
        return manual
