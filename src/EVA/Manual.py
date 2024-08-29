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

from EVA import globals

class ManualWindow(QWidget):
    def __init__(self, parent=None):
        super(ManualWindow, self).__init__(parent)

        self.setWindowTitle("Manual")
        self.setMinimumSize(700, 650)

        self.htmlstr = self.loadManual("EVA/manual.html")
        self.page = QTextBrowser(self)
        self.page.setOpenLinks(True)

        self.page.setHtml(self.htmlstr)
        self.page.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.page)
        self.show()

    def loadManual(self, path):
        with open(path, "r", encoding="utf-8") as file:
            manual = "".join(file.readlines())

        file.close()
        return manual
