import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
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
    QTableWidget,
    QTableWidgetItem,
)
from PyQt5.QtGui import QPalette, QColor, QCloseEvent
import sys

import MultiPlot
import loaddata
import loadcomment
import globals
import GenReadList
import ReadMultiRun


class MultiPlotWindow(QWidget):
    """
        This "window" is a QWidget. If it has no parent, it
        will appear as a free-floating window as we want.
        """


    def __init__(self, parent = None):
        super(MultiPlotWindow,self).__init__(parent)

        self.resize(1200, 1100)
        self.setMinimumSize(1200, 1100)
        self.setWindowTitle("Multi-Plot Window ")

        plot_multi = QPushButton(self)
        plot_multi.setText('Load and Plot Multi Spectra')
        plot_multi.move(100,100)
        plot_multi.clicked.connect(
            lambda: self.loadandplot())

        lab_multi_offset = QLabel(self)
        lab_multi_offset.setText('Offset')
        lab_multi_offset.move(550,115)

        self.val_multi_offset = QLineEdit(self)
        self.val_multi_offset.setText('0.0')
        self.val_multi_offset.move(650, 110)


        self.RunListTable = QTableWidget(self)
        self.RunListTable.setColumnCount(3)
        self.RunListTable.move(100,200)
        self.RunListTable.setMinimumSize(800,700)
        self.RunListTable.setRowCount(50)
        self.RunListTable.setHorizontalHeaderLabels(['Start', 'End', 'Step'])

        for i in range(3):
            for j in range(50):
                print(i,j)
                self.RunListTable.setItem(j,i,QTableWidgetItem(''))

        self.show()

    def loadandplot(self):
        print('hello')
        line = []

        #read table from GUI

        for i in range(50):
            try:
                start = int(self.RunListTable.item(i,0).text())
            except:
                start = 0
            print('start', start)
            try:
                end = int(self.RunListTable.item(i,1).text())
                print('end',end)
            except:
                end = 0
            print('end', end)
            try:
                step = int(self.RunListTable.item(i,2).text())
            except:
                step = 0
            line.append([start,end,step])

        print('line')
        print(line)
        RunList = GenReadList.GenReadList(line)
        print('RunList', RunList)
        offset = float(self.val_multi_offset.text())
        print('offset', offset)

        datax_GE1, datay_GE1, datax_GE2, datay_GE2, datax_GE3, datay_GE3, datax_GE4, datay_GE4\
            = ReadMultiRun.ReadMultiRun(RunList)

        MultiPlot.MultiPlot(datax_GE1, datay_GE1, datax_GE2, datay_GE2, datax_GE3, datay_GE3, datax_GE4, datay_GE4,
                            RunList,offset)



