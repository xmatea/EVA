import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidgetAction,
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QMenuBar,
    QMenu,
    QHBoxLayout,
    QLineEdit,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtGui import QPalette, QColor, QCloseEvent
import sys
import loaddata
import loadcomment
import globals


class PlotWindow(QWidget):
    """
        This "window" is a QWidget. If it has no parent, it
        will appear as a free-floating window as we want.
        """


    def __init__(self):
        super().__init__()
        '''layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)'''

        wPlot = QWidget()
        wPlot.resize(1200, 600)
        wPlot.setWindowTitle("Plot Window")
