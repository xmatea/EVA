from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
)

import MultiPlot
import GenReadList
import ReadMultiRun

class MultiPlotWindow(QWidget):
    """
        This window is the GUI for the multiplot window

        """


    def __init__(self, parent = None):
        super(MultiPlotWindow,self).__init__(parent)

        self.resize(1200, 1100)
        self.setMinimumSize(1200, 1100)
        self.setWindowTitle("Multi-Plot Window ")

        # sets up button
        plot_multi = QPushButton(self)
        plot_multi.setText('Load and Plot Multi Spectra')
        plot_multi.move(100,100)
        plot_multi.clicked.connect(
            lambda: self.loadandplot())

        # label for offset
        lab_multi_offset = QLabel(self)
        lab_multi_offset.setText('Offset')
        lab_multi_offset.move(550,115)

        # input for the value of the y-axis offset
        self.val_multi_offset = QLineEdit(self)
        self.val_multi_offset.setText('0.0')
        self.val_multi_offset.move(650, 110)

        # makes the table for the list of run numbers to plot
        self.RunListTable = QTableWidget(self)
        self.RunListTable.setColumnCount(3)
        self.RunListTable.move(100,200)
        self.RunListTable.setMinimumSize(800,700)
        self.RunListTable.setRowCount(50)
        self.RunListTable.setHorizontalHeaderLabels(['Start', 'End', 'Step'])


        # sets each point in the table to a blank
        for i in range(3):
            for j in range(50):

                self.RunListTable.setItem(j,i,QTableWidgetItem(''))

        self.show()

    def loadandplot(self):
        #print('hello')
        line = []

        #read table from GUI

        for i in range(50):
            try:
                start = int(self.RunListTable.item(i,0).text())
            except:
                start = 0
            #print('start', start)
            try:
                end = int(self.RunListTable.item(i,1).text())
                #print('end',end)
            except:
                end = 0
            #print('end', end)
            try:
                step = int(self.RunListTable.item(i,2).text())
            except:
                step = 0
            line.append([start,end,step])

        #print('line')
        #print(line)
        # generates a list of runs to load and plot
        RunList = GenReadList.GenReadList(line)
        #print('RunList', RunList)
        # reads offset from GUI
        offset = float(self.val_multi_offset.text())
        #print('offset', offset)

        # reads data and returns as each detector and as an array

        datax_GE1, datay_GE1, datax_GE2, datay_GE2, datax_GE3, datay_GE3, datax_GE4, datay_GE4\
            = ReadMultiRun.ReadMultiRun(RunList)

        # plots multiple runs from the runlist and with a y offset

        MultiPlot.MultiPlot(datax_GE1, datay_GE1, datax_GE2, datay_GE2, datax_GE3, datay_GE3, datax_GE4, datay_GE4,
                            RunList, offset)



