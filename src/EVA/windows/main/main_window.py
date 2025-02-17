import logging
import sys
import os

from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication, QMessageBox
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QColor, QIcon

from EVA.windows.main.main_view import MainView
from EVA.windows.main.main_model import MainModel
from EVA.windows.main.main_presenter import MainPresenter
from EVA.core.app import get_config
from EVA.util.path_handler import get_path

logger = logging.getLogger(__name__)

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Elemental Analysis")
        self.setMinimumSize(QSize(650, 300))
        self.view = MainView(self)
        self.model = MainModel()
        self.presenter = MainPresenter(self.view, self.model)
        self.setCentralWidget(self.view)

    def closeEvent(self, event):
        #close window cleanly

        logger.debug("Has config been modified? %s", get_config().is_changed())
        if not get_config().is_changed(): # quit immediately if no changes have been made
            event.accept()
            QApplication.quit()
            return

        # Show save prompt window if any changes has been made to the config file
        quit_msg = "Would you like to save your changes?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Yes:
            get_config().save_config()
            logger.debug("User replied yes to close prompt.")
            event.accept()
            QApplication.quit()

        elif reply == QMessageBox.StandardButton.No:
            logger.debug("User replied no to close prompt.")
            event.accept()
            QApplication.quit()

        else:
            event.ignore()
            return
